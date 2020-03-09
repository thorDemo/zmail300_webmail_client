import os
from PIL import Image

for top, dirs, non_dirs in os.walk('E:/mmjpg/yummy/'):
    for item in non_dirs:
        img_path = os.path.join(top, item)
        try:
            image = Image.open(img_path)
            width, height = image.size
            if width == 800 and height == 1200:
                print(img_path, width, height)
                image.save(f'../static/{item}')
        except OSError:
            continue