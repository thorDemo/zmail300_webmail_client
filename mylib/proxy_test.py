import requests
session = requests.session()
data = session.get('http://http.tiqu.alicdns.com/getip3?num=1&type=1&pro=0&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4')
proxy = {'https': f'https://{str(data.text).strip()}'}
print(proxy)
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
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
# r = session.get('https://mailv.zmail300.cn/webmail/login.php?msg=login', proxies=proxy, headers=headers, verify=False)
r = requests.get('https://mailv.zmail300.cn/webmail/login.php?msg=login', headers=email_headers, verify=False)
# r = session.get('http://mailv.zmail300.cn', proxies=proxy, headers=headers, verify=False)
print(r.text)