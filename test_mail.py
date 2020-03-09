from requests.exceptions import RequestException
from mylib.proxy_zmail import ZMailWebServer
from mylib.code_logging import Logger as Log
from configparser import ConfigParser
from threadpool import ThreadPool, makeRequests
from mylib.create_ad_img import create_yh_ad_img
import uuid
import random
import requests
import time
import json

login_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Host': 'mailv.zmail300.cn',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'https://mailv.zmail300.cn/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.88 Safari/537.36',
}

log = Log('send_email.log').get_log()


def get_email_mission():
    c = ConfigParser()
    c.read(f'config.ini', encoding='utf-8')
    host = c.get('server', 'server_host')
    response = requests.get(f'http://{host}/email/', timeout=2)
    temp = json.dumps(response.json(), ensure_ascii=False)
    return json.loads(temp)


def get_global_account():
    c = ConfigParser()
    c.read(f'config.ini', encoding='utf-8')
    host = c.get('server', 'server_host')
    response = requests.get(f'http://{host}/account/')
    return response.json()


def post_auth_user(u, p):
    c = ConfigParser()
    c.read(f'config.ini', encoding='utf-8')
    host = c.get('server', 'server_host')
    requests.get(f'http://{host}/auth_account/?username={u}&password={p}')
    return


def get_proxies(num):
    url = f'http://http.tiqu.alicdns.com/getip3?num=1&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&' \
          f'cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'
    response = requests.get(url=url)
    data = str(response.text).strip().split('\r\n')
    print(len(data))
    return data


def test_proxy(proxies):
    t = 0
    while t < 5:
        try:
            requests.get(
                'https://mailv.zmail300.cn/webmail/login.php?msg=login',
                headers=login_headers,
                proxies={'https': f'https://{proxies}'},
                timeout=2
            )
            break
        except RequestException as e:
            t += 1
    if t < 4:
        return True
    else:
        return False


def thread_mission(proxies):
    log.warning(f'CONNECT EMAIL SERVER WITH {proxies}')
    temp = 0
    if test_proxy(proxies) is False:
        log.warning(f'CONNECT PROXY ERROR {proxies}')
        return
    while temp < 5:
        while True:
            try:
                account_data = get_global_account()
                username = account_data['username']
                password = account_data['password']
                server = ZMailWebServer(username, password, debuglevel=1, proxies=proxies)
                if server.x_token is None:
                    log.warning(f'{temp}-{proxies}-Login Web Mail Failed:{server.message} Retry Waiting 5s')
                    time.sleep(5)
                    continue
                else:
                    log.warning(f'{temp}-{proxies}-Login Web Mail Success:{username, password}')
                    post_auth_user(username, password)
                    log.warning(f'{temp}-{proxies}-Send Back Auth Account:{username, password}')
                    break
            except RequestException:
                if test_proxy(proxies) is False:
                    log.warning(f'CONNECT PROXY ERROR {proxies}')
                    return
                log.warning(f'{temp}-{proxies}-Request Server Exception Retry Waiting 5s')
                temp += 1
                time.sleep(1)
        try:
            mission_data = get_email_mission()
            mission_data['receivers'].append('914081010@qq.com')
            image = create_yh_ad_img(f'{uuid.uuid4().__str__()}.jpg')
            log.warning(f"{temp}-{proxies}-CREATE IMG SUCCESS:{image}")
            image_url = server.post_img(image)
            log.warning(f"{temp}-{proxies}-POST IMG {image_url}")
            template = open('templates/type_1.html', 'r', encoding='utf-8').read()
            template = template.replace('image_url', image_url)
            log.warning(f"{temp}-{proxies}-Send Mail To {mission_data['receivers']}")
            result = server.send_mail(
                to=mission_data['receivers'],
                # content=template,
                content='i love you',
                subject=mission_data['from'],
                # content=mission_data['message'],
                # subject=mission_data['subject']
            )
            if 'Permission denied' in result:
                log.warning(f"{temp}-{proxies}-Account Error Retry Waiting 5s")
                time.sleep(5)
                continue
            # 不存入发件箱 不需要删除了
            log.warning(f"{temp}-{proxies}-Send Success:{result} Delay: {mission_data['delay']}")
            time.sleep(int(mission_data['delay']))
            temp += 1
        except RequestException as e:
            # traceback.print_exc(e)
            if test_proxy(proxies) is False:
                log.warning(f'CONNECT PROXY ERROR {proxies}')
                return
            temp += 1
            log.warning(f"{temp}-{proxies}-Request Server Exception Retry Waiting 5s")
            time.sleep(1)


proxy = get_proxies(1)
thread_mission(proxy[0])
