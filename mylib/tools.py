import requests
from random import choice, sample, randint
import base64


def encode_header(string, email):
    s = string.encode('utf-8')
    return f'=?UTF-8?B?{str(base64.b64encode(s), encoding="utf-8")}?= <{email}>'


def local_ip():
    response = requests.get('http://icanhazip.com/')
    ip = response.text.strip()
    return ip


def rand_from():
    file = open('content/from.txt', 'r', encoding='utf-8')
    data = []
    for line in file:
        data.append(line.strip())
    return choice(data)


def rand_to():
    file = open('content/to.txt', 'r', encoding='utf-8')
    data = []
    for line in file:
        data.append(line.strip())
    return choice(data)


def rand_title():
    file = open('content/title0{}.txt'.format(randint(1, 6)), 'r', encoding='utf-8')
    data = []
    for line in file:
        data.append(line.strip())
    return choice(data)


def rand_chars():
    string = "qwertyuiopasdfghjklzxcvbnm"
    return ''.join(sample(string, 5))


def rand_account():
    file = open('account/user.txt', 'r', encoding='utf-8')
    data = []
    for line in file:
        data.append(line.strip())
    string = str(choice(data)).split(' ')
    return string[0], string[1].strip()


def rand_content():
    file = open('content/shuangyu0{}.txt'.format(randint(1, 6)), 'r', encoding='utf-8')
    data = []
    for line in file:
        data.append(line.strip())
    return choice(data)


def rand_tips():
    key1 = '注注注注注驻蛀拄炷'
    key2 = '珊栅删姗跚笧册测侧厕冊笧荝測策粣測惻冊冊冊冊冊冊冊冊冊冊冊冊'
    key3 = '送'
    key4 = '元芫沅忨杬笎鈨'
    key5 = '!@#$%^&*-|[]/,.;'
    ad = [
        '大爷今天晚上来玩会儿？',
        '今晚8点准时上线',
        '是兄弟吗？过来一起赚钱',
        '话不多说，赢钱不忘老兄弟',
        '老同学在吗？这里有路子',
        '挂机掉宝爆金币。爽！疯狂爆率',
        '十倍街机爆。爆！爆！爆！',
        '坐庄无罪，搏菜有理！来这里，和一千人一起享受心跳！注册即宋一万游戏巾！',
        '还在为无趣而单调的生活烦恼么？',
        '点击注笧，一万鑫币任你拿；坐拥上莊，精彩刺激其脾战！',
        '其调戏僵尸粉，不如在线找我！',
        '棋乐无穷，牌案惊奇，银河娱乐世界，自己当莊稳嬴，在线千人薄弈',
        '今天你怎么没来上班！',
        '明天发年终奖记得早点来。',
        '你老婆叫你过来吃饭',
        '公司下发的文案请查收',
        '这是最新的活动方案，看一哈',
        '我给你一个红包(●´ϖ`●) ，赶紧来万啊',
        '求求你 不要走！ 你不要走！ 声嘶力竭.jpg',
        '我不懂赔率只懂陪你！',
        '比赛总会结束，想你不会',
        '给你说多少遍了抱怨没用，抱我！'
    ]
    money = [188, 288, 388, 488, 588, 688, 788, 888, 988, 999]
    return '{}{}就{}8-{}{}-{}-{}'.format(
        choice(key1), choice(key2), choice(key3), choice(money), choice(key4), choice(key5), choice(ad)
    )

