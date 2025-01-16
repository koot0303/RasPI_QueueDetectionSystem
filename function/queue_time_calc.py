from PIL import Image
import numpy as np
import shutil
import os
import cv2


# メイン処理
def main():

    save_folder_path = './img/split_img'    # 保存先フォルダパス
    binary_img_path = './img/queue_detected.jpg'    # 二値化された画像パス
    all_people_count = 0    # 行列の人数
    threshold = 5000        # ピクセルごとのしきい値

    image_vertical_split(binary_img_path, 100, save_folder_path)    # 画像の縦分割

    # queue_v_split_(4~8)の人数を計算
    # ※ 0~3,9はノイズが大きいので省略
    for i in range(4, 9):

        split_image_path = f'./img/split_img/queue_v_split_{i}.jpg'
        all_people_count += count_black_pixels(split_image_path, threshold)

        threshold *= 2  # 人の大きさに合うしきい値を設定

    # 総人数
    print(all_people_count, "人")


# フォルダを空で作成
def empty_folder(folder_path):

    """
    empty_folder : フォルダを空で作成
    Input   : 作成するフォルダパス
    Output  : フォルダパスの空フォルダ

    argument

    folder_path(string) : フォルダパス
    """

    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)


# 画像の縦分割
def image_vertical_split(img, split_num=10, save_folder='./img'):
    
    """
    image_vertical_split : 画像の縦分割
    Input   : 画像パス、分割の最小比率、保存先フォルダのパス
    Output  : 分割された画像
    
    argument

    img(string)     : 画像のパス
    split_num(int)  : 分割の最小比率(100なら最小の分割は100分割のサイズになる)
    save_folder(string) : 保存先フォルダのパス
    """

    # 画像ファイル読み込み
    img = Image.open(img)
    
    # 空フォルダ作成
    empty_folder(save_folder)

    # 画像をNumPy配列に変換
    image_array = np.array(img)

    # 分割の前処理
    image_height, _, _ = image_array.shape
    v_split_size = image_height // split_num # 縦に分割するサイズ
    split_images = []           # 分割された画像を格納するリスト

    v_end = 0   # 分割ごとのの最下ピクセル
    v_ratio = 1 # 増加比率

    # 分割処理
    for i in range(v_split_size):
        # 分割するサイズを計算
        v_start = v_end
        v_end = (i + 1) * v_ratio

        # 分割の最下ピクセル数が画像の高さを超えたら
        if v_end > image_height:
            break

        # 画像を分割
        split_image = image_array[v_start:v_end, :, :]
        split_images.append(Image.fromarray(split_image))

        v_ratio += v_split_size # 分割サイズ分、毎回比率を大きくする

    # 画像を保存
    for i, img in enumerate(split_images):
        img.save(f"./img/split_img/queue_v_split_{i}.jpg")

# 黒のピクセル数に応じて人数をカウント
def count_black_pixels(image_path, threshold=100):

    """
    count_black_pixels : 画像の黒ピクセル数に応じて人数をカウント
    Input   : 画像パス、しきい値
    Output  : 人数

    argument

    image_path(string)  : 画像パス 
    threshold(int)      : しきい値(nピクセルごとに1人とカウントする)
    
    ※ しきい値の算出方法
    スプリットごとに頭の数を数えてしきい値を調整。一致したしきい値を設定する。
    """

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    height, width = img.shape

    # 端から黒ピクセルをカウント( threshold ごとに1人)
    people_count = 0
    black_pixel_count = 0
    for i in range(width):
        for j in range(height):
            if img[j, i] == 0:
                black_pixel_count += 1
                if black_pixel_count>= threshold:
                    people_count += 1              # 人数カウント追加
                    black_pixel_count = 0   # ピクセルカウントリセット

    return people_count


# メイン処理
if __name__ == "__main__":
    main()