import cv2
import numpy as np


# # 画像の幅と高さを表示
# image_height, image_width = img.shape[0], img.shape[1]
# print('width: ', image_width)
# print('height: ', image_height)


# メイン関数
def main():
    # 画像読み込み
    image_name = "./queue_gpt.jpg"
    img = cv2.imread(image_name)

    # カメラ異常検知
    camera_exception(img)

    # 画像をグレースケール化
    image_name = gray_scale(image_name, img)
    img = cv2.imread(image_name)

    # 画像をガウスぼかし化
    image_name = gauss_blur(image_name, img)
    img = cv2.imread(image_name)

    # 画像を二値化
    binarization(image_name, img)


# カメラの異常検知
def camera_exception(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # 異常の場合
    if np.median(v) < 10 or np.median(v) > 245:
        return 1
    
    # 正常の場合
    else:
        return 0


# グレースケール画像を保存
def gray_scale(image_name, img):

    gray_image_name = "./gray_" + image_name[2:]
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(gray_image_name, gray_image)

    return gray_image_name


# ノイズ除去
def gauss_blur(image_name, img):

    gauss_image_name = "./gauss_" + image_name[2:]
    gauss_image = cv2.GaussianBlur(img, (17, 17), 11)
    cv2.imwrite(gauss_image_name, gauss_image)

    return gauss_image_name


# 二値化
def binarization(image_name, img):

    binary_image_name = "./binary_" + image_name[2:]
    ret, binary_image = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
    cv2.imwrite(binary_image_name, binary_image)


# メイン処理
if __name__ == "__main__":
    main()