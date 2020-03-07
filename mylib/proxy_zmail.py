import requests
import re
import hashlib
from bs4 import BeautifulSoup


# 登录请求头
login_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Host': 'mailv.zmail300.cn',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'https://mailv.zmail300.cn/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.88 Safari/537.36',
}
# 邮件请求头
email_headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'mailv.zmail300.cn',
    'Origin': 'https://mailv.zmail300.cn',
    'Referer': 'https://mailv.zmail300.cn/webmail/index.php',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.88 Safari/537.36',
}
# 邮件数据格式
email_data = {
    'method': 'send',
    'content': '',
    'text': '',
    'subject': '',
    'to': '',
    'cc': '',
    'bcc': '',
    'mail_name': '',
    'json_name': '',
    'send_type': 'is_draft',
    'is_reply':  '',
    'is_fwd': '',
    'priority': 'false',
    'composeSend': 'false',
    'composeText': 'false',
    'composeReceipt': 'false',
    'composeSingle': 'false',
    'composeTime': 'false',
    'composeTrack': 'false',
    'hasPlaceholder': 'false',
    'tplName':  '',
    'msg_id':  '',
    'draftMailName': '',
    'loadStr': '发送中...',
    'encrypted_pwd': '',
}


def add_salt_md5_password(password_str, salt):
    md5_password = hashlib.md5(bytes(password_str, encoding='utf-8')).hexdigest()
    md5_password_salt = hashlib.md5(bytes(md5_password + salt, encoding='utf-8')).hexdigest()
    return md5_password_salt


class ZMailWebServer:
    debuglevel = 0

    def __init__(self, username, password, proxies, debuglevel):
        self.debuglevel = debuglevel
        self.username = username
        self.password = password
        self.session = requests.session()
        self.proxies = proxies
        self.salt = self.get_salt()
        self.x_token, self.message = self.login_web_mail()
        self.remove_target = ''
        self.subject = ''

    def login_web_mail(self):
        data = {
                'account': self.username,
                'password': add_salt_md5_password(self.password, self.salt),
                'vcode': '',
                'remember_me': 1,
                'login_lang': ''
            }
        response = self.session.post(
            'https://mailv.zmail300.cn/webmail/web/php/user/login.php',
            headers=login_headers,
            data=data,
            proxies=self.proxies
        )
        context = response.text
        soup = BeautifulSoup(context, 'html.parser')
        message_box = soup.find(id='msg_container')
        try:
            if message_box:
                message = str(message_box.string).strip()
                if self.debuglevel == 1:
                    print(None, message)
                return None, message
            else:
                token = re.findall(r'"x-token":"(.*?)"', context, flags=0)[0]
                if self.debuglevel == 1:
                    print(token, None)
                return token, None
        except IndexError:
            return None, '找不到token'

    def get_salt(self):
        response = self.session.get(
            'https://mailv.zmail300.cn/webmail/login.php?msg=login',
            headers=login_headers,
            proxies=self.proxies
        )
        context = response.text
        salt = re.findall(r'__code__ = "(.*?)"', context, flags=0)[0]
        return salt

    def send_mail(self, to, subject='', content=''):
        self.subject = subject
        bcc_string = ''
        if isinstance(to, list):
            receiver = to[0]
            temp = 0
            for line in to:
                if temp > 0:
                    bcc_string = bcc_string + ',' + line
                temp += 1
        else:
            receiver = to
        data = email_data
        bcc_string = bcc_string.strip(',')
        data['to'] = f'{receiver} <{receiver}>'
        data['bcc'] = bcc_string
        data['subject'] = subject
        data['text'] = subject
        data['content'] = content
        header = email_headers
        header['X-Token'] = self.x_token
        response = self.session.post(
            'https://mailv.zmail300.cn/webmail/web/php/user/mail/compose.php',
            headers=header,
            data=data,
            proxies=self.proxies
        )
        if self.debuglevel == 1:
            print(data)
            print(response.status_code, response.text)
        return response.text
