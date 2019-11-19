import urllib
import urllib.request
import os
import sys
import cv2
import numpy as np
import time
from argparse import ArgumentParser
from selenium import webdriver
from cv_core.detector.face_inference import FaceLocationDetector

parser = ArgumentParser()
parser.add_argument('name')

args = parser.parse_args()

name = args.name

img_limit = 100

save_path = 'images/' + name


def main():
    chromeDriver = '/Users/yi/webDriverTool/chromedriver'

    url = 'https://www.google.com/search?q={}&safe=strict&sxsrf=ACYBGNQPXgVksbwaaplNpk7muG_E8OT-Mg:1571638753728&source=lnms&tbm=isch&sa=X&ved=0ahUKEwiOgYbN2qzlAhVSHKYKHTolC78Q_AUIEigB&biw=1403&bih=717'.format(
        name)

    driver = webdriver.Chrome(chromeDriver)

    driver.maximize_window()

    detector = FaceLocationDetector()

    img_url_dic = {}

    driver.get(url)

    # roll the screen
    pos = 0
    num = 0
    for i in range(100):
        pos += i * 100
        js = "document.documentElement.scrollTop=%d" % pos
        driver.execute_script(js)
        time.sleep(1)

        for element in driver.find_elements_by_tag_name('img'):
            try:
                img_url = element.get_attribute('src')

                if img_url != None and not img_url in img_url_dic:
                    img_url_dic[img_url] = ''
                    resp = urllib.request.urlopen(img_url)

                    image = np.asarray(bytearray(resp.read()), dtype="uint8")
                    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

                    if image is not None:

                        face_locs = detector.predict(image)
                        if len(face_locs) != 1:
                            continue

                        num += 1

                        if not os.path.exists(save_path):
                            os.mkdir(save_path)

                        urllib.request.urlretrieve(
                            img_url,
                            os.path.join(save_path,
                                         '000000_{}.jpg'.format(num)))

                        print(num)

                        if num >= img_limit:
                            sys.exit()

            except OSError:
                print('OSError!')
                print(pos)
                break


if __name__ == '__main__':

    main()