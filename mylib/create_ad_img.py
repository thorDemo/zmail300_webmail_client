# -*- coding:utf-8 -*-
import requests
from urllib3 import encode_multipart_formdata
from mylib.tools import rand_chars_num
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import os
from random import choice
import uuid


class MyGaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"

    def __init__(self, radius=2, bounds=None):
        self.radius = radius
        self.bounds = bounds

    def filter(self, image):
        if self.bounds:
            clips = image.crop(self.bounds).gaussian_blur(self.radius)
            image.paste(clips, self.bounds)
            return image
        else:
            return image.gaussian_blur(self.radius)


def add_text_to_img(image, text, text_y, font, color):
    rgba_image = image.convert('RGBA')
    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)
    text_size_x, text_size_y = image_draw.textsize(text, font=font)
    # 设置文本文字位置
    width, height = image.size
    text_xy = ((width - text_size_x) / 2, text_y)
    # 设置文本颜色和透明度
    image_draw.text(text_xy, text, font=font, fill=color)
    image_with_text = Image.alpha_composite(rgba_image, text_overlay)
    return image_with_text


def create_yh_ad_img(temp_name):
    image_items = []
    for top, dirs, non_dirs in os.walk('static'):
        for item in non_dirs:
            img_path = os.path.join(top, item)
            image_items.append(img_path)
    girls = choice(image_items)
    image = Image.open(girls)
    image = image.filter(MyGaussianBlur(radius=10))
    font = ImageFont.truetype('font/1.ttf', 100)
    image = add_text_to_img(image, '银河娱乐城邀请注册', 20, font, '#e0c782')
    logo = Image.open('logo.png')
    image.paste(logo, (300, 130), logo)
    font = ImageFont.truetype('font/2.ttf', 40)
    image = add_text_to_img(image, '快邀请您的好友与您一起加入我们吧', 200, font, '#000')
    font = ImageFont.truetype('font/2.ttf', 40)
    image = add_text_to_img(image, '注册网址:', 280, font, '#000')
    font = ImageFont.truetype('font/BRUX.otf', 100)
    image = add_text_to_img(image, 'yinhe123.com', 350, font, '#ffff00')
    font = ImageFont.truetype('font/PingFang-Heavy-2.ttf', 20)
    image = add_text_to_img(image, '【最新】①捕鱼7天乐②限时登陆免费领取③万人争霸赢话费④GPK年年有鱼金', 520, font, '#000')
    image = add_text_to_img(image, '【1】注册三重礼：注册送8，APP下载送18，绑定手机靓号再送11331！', 560, font, '#000')
    image = add_text_to_img(image, '【2】时时返水：电子棋牌捕鱼，投注1元+，即可时时返水3.0%，', 600, font, '#000')
    image = add_text_to_img(image, '【3】全新代理：佣金日日结，老板天天做。100%稳赚 0投资 0风险。', 640, font, '#000')
    image = add_text_to_img(image, '【4】会员账号=永久价值：等级越高礼金更高，更有周周俸禄、月月俸禄送不停！', 680, font, '#000')
    image = add_text_to_img(image, f'ID: {uuid.uuid4()}'.__str__(), 740, font, '#000')
    image = image.resize((500, 750), Image.ANTIALIAS)
    result = Image.new('RGB', image.size, (255, 255, 255))
    result.paste(image, (0, 0), image)
    result.save(f'temp/{temp_name}')
    return temp_name
