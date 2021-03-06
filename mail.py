from requests.exceptions import RequestException
from mylib.proxy_zmail import ZMailWebServer
from mylib.code_logging import Logger as Log
from configparser import ConfigParser
from mylib.create_ad_img import create_yh_ad_img
import random
import requests
import time
import json
import os

log = Log('send_email.log').get_log()


def get_email_mission():
    c = ConfigParser()
    # c.read(f'/root/zmail300_webmail_client/config.ini', encoding='utf-8')
    c.read(f'config.ini', encoding='utf-8')
    host = c.get('server', 'server_host')
    response = requests.get(f'http://{host}/email/', timeout=2)
    temp = json.dumps(response.json(), ensure_ascii=False)
    return json.loads(temp)


def get_global_account():
    c = ConfigParser()
    # c.read(f'/root/zmail300_webmail_client/config.ini', encoding='utf-8')
    c.read(f'config.ini', encoding='utf-8')
    host = c.get('server', 'server_host')
    response = requests.get(f'http://{host}/account/')
    return response.json()


def post_auth_user(u, p):
    c = ConfigParser()
    # c.read(f'/root/zmail300_webmail_client/config.ini', encoding='utf-8')
    c.read(f'config.ini', encoding='utf-8')
    host = c.get('server', 'server_host')
    requests.get(f'http://{host}/auth_account/?username={u}&password={p}')
    return


if __name__ == '__main__':
    log.warning(f'working dir: {os.getcwd()}')
    log.warning('CONNECT EMAIL SERVER')
    while True:
        while True:
            try:
                account_data = get_global_account()
                username = account_data['username']
                password = account_data['password']
                log.warning(f'Request New Account:{username},{password}')
                conf = ConfigParser()
                conf.read(f'config.ini', encoding='utf-8')
                debuglevel = int(conf.get('server', 'debuglevel'))
                server = ZMailWebServer(username, password, debuglevel=debuglevel, proxies='58.218.92.170:7943')
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
            time.sleep(int(mission_data['delay']))
        except RequestException as e:
            # traceback.print_exc(e)
            log.warning(f"Request Server Exception Retry Waiting 5s")
            time.sleep(5)
