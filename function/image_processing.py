import cv2
import numpy as np


# # 画像の幅と高さを表示
# image_height, image_width = img.shape[0], img.shape[1]
# print('width: ', image_width)
# print('height: ', image_height)


# メイン関数
def main():
    # 画像読み込み
    image_path = "./img/queue_gpt.jpg"

    # カメラ異常検知
    if camera_exception(image_path):
        print("画像に異常があります。行列が検知できません。")
    else:
        print("画像に異常はありません。行列を検知します。")

        # 画像をグレースケール化
        image_path = gray_scale(image_path)

        # 画像をガウスぼかし化
        image_path = gauss_blur(image_path)

        # 画像を二値化
        binarization(image_path)


# カメラの異常検知
def camera_exception(image_path):

    """
    camera_exception : カメラの異常検知
    Input   : 画像パス
    Output  : 0 (正常な場合) or 1 (異常な場合)
    
    argument

    image_path(string)  : 画像パス
    """

    # 異常な場合
    if brightness_check(image_path):
        print("輝度")
        return 1
    
    elif resolution_check(image_path, 1944, 2592):
        print("解像度")
        return 1

    # 正常な場合
    else:
        return 0


# 輝度チェック
def brightness_check(image_path):

    """
    brightness_check : 輝度チェック
    Input   : 画像パス
    Output  : 0 (正常な場合) or 1 (異常な場合)

    argument

    image_path  : 画像パス
    """

    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # 異常の場合
    if np.median(v) < 10 or np.median(v) > 245:
        return 1
    
    # 正常の場合
    else:
        return 0


# 解像度チェック
def resolution_check(image_path, check_height, check_width):

    """
    brightness_check : 解像度チェック
    Input   : 画像パス
    Output  : 0 (正常な場合) or 1 (異常な場合)

    argument

    image_path  : 画像パス
    check_height    : チェックする画像の高さ
    check_width     : チェックする画像の幅
    """

    img = cv2.imread(image_path)
    height, width = img.shape[:2]

    # 異常の場合
    if height != check_height or width != check_width:
        return 1
    
    # 正常の場合
    else:
        return 0


# グレースケール画像を保存
def gray_scale(image_path):

    """
    gray_scale : グレースケール画像を保存
    Input   : 画像パス
    Output  : グレースケール画像

    argument

    image_path  : 画像パス
    """

    img = cv2.imread(image_path)

    gray_image_name = "./img/gray_" + image_path[6:]
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(gray_image_name, gray_image)

    return gray_image_name


# ノイズ除去
def gauss_blur(image_path):

    """
    gauss_blur : ノイズ除去後の画像を保存
    Input   : 画像パス
    Output  : ノイズ除去後の画像

    argument

    image_path  : 画像パス
    """

    img = cv2.imread(image_path)

    gauss_image_name = "./img/gauss_" + image_path[6:]
    gauss_image = cv2.GaussianBlur(img, (17, 17), 11)
    cv2.imwrite(gauss_image_name, gauss_image)

    return gauss_image_name


# 二値化
def binarization(image_path):

    """
    gray_scale : 二値化画像を保存
    Input   : 画像パス
    Output  : 二値化画像(./img/queue_detected.jpg)

    argument

    image_path  : 画像パス
    """

    img = cv2.imread(image_path)

    binary_image_name = "./img/queue_detected.jpg"
    ret, binary_image = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
    cv2.imwrite(binary_image_name, binary_image)


# メイン処理
if __name__ == "__main__":
    main()