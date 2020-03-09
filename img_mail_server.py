import base64
import requests

file = open('E:/mmjpg/yummy/000aadac42be46b38399b2e04c8df95b.jpg', 'rb')
base64_data=base64.b64encode(file.read())
code = base64_data.decode()
img_data = 'data:image/jpeg;base64,%s' % code
data = {
    'upload': img_data,
    'ckCsrfToken': ''
}
response = requests.post(
    'https://mailv.zmail300.cn/webmail/web/php/user/mail/upload.php?type=img',
    data=data
)

