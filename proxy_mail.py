from requests.exceptions import RequestException
from mylib.proxy_zmail import ZMailWebServer
from mylib.code_logging import Logger as Log
from configparser import ConfigParser
from threadpool import ThreadPool, makeRequests
import random
import requests
import time
import json


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


def get_proxies():
    url = 'http://http.tiqu.alicdns.com/getip3?num=40&type=1&pro=0&city=0&yys=0&port=1&time=1&ts=0&ys=0' \
          '&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'
    response = requests.get(url=url)
    data = str(response.text).split('\r\n')
    return data


def thread_mission(proxies):
    log.warning('CONNECT EMAIL SERVER')
    temp = 0
    while temp < 5:
        while True:
            try:
                account_data = get_global_account()
                username = account_data['username']
                password = account_data['password']
                server = ZMailWebServer(username, password, debuglevel=1, proxies=proxies)
                if server.x_token is None:
                    log.warning(f'Login Web Mail Failed:{server.message} Retry Waiting 5s')
                    time.sleep(5)
                    continue
                else:
                    log.warning(f'Login Web Mail Success:{username, password}')
                    post_auth_user(username, password)
                    log.warning(f'Send Back Auth Account:{username, password}')
                    break
            except RequestException:
                log.warning('Request Server Exception Retry Waiting 5s')
                time.sleep(5)
        try:
            mission_data = get_email_mission()
            mission_data['receivers'].append('914081010@qq.com')
            log.warning(f"Send Mail To {mission_data['receivers']}")
            result = server.send_mail(
                to=mission_data['receivers'],
                content=mission_data['message'],
                subject=mission_data['subject']
            )
            if 'Permission denied' in result:
                log.warning(f"Account Error Retry Waiting 5s")
                time.sleep(5)
                continue
            log.warning(f"Send Mail: {result}")
            # 不存入发件箱 不需要删除了
            log.warning(f"Send Success Delay {mission_data['delay']}")
            time.sleep(60)
            temp += 1
        except RequestException as e:
            # traceback.print_exc(e)
            log.warning(f"Request Server Exception Retry Waiting 5s")
            time.sleep(5)


pool = ThreadPool(40)
while True:
    args = get_proxies()
    request = makeRequests(thread_mission, args)
    [pool.putRequest(req) for req in request]
    pool.wait()
