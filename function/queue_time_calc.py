from PIL import Image
import numpy as np
import shutil
import os
import cv2


# フォルダーを空で作成
def empty_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)


# 画像の縦分割
def image_vertical_split(img, split_num, save_folder):
    
    # 画像ファイル読み込み
    img = Image.open(img)
    
    # 空フォルダ作成
    empty_folder(save_folder)

    # 画像をNumPy配列に変換
    image_array = np.array(img)

    # 縦に15分割
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

        # 画像を分割
        split_image = image_array[v_start:v_end, :, :]
        split_images.append(Image.fromarray(split_image))

        v_ratio += v_split_size


    # 画像を保存
    for i, img in enumerate(split_images):
        img.save(f"./img/split_img/queue_v_split_{i}.jpg")

# 黒のピクセル数に応じて人数をカウント
def count_black_pixels(image_path, threshold=100):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    height, width = img.shape

    # 端から黒ピクセルをカウント(100ごとに1人)
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

def main():

    save_folder_path = './img/split_img'    # 保存先フォルダパス
    binary_img_path = './img/binary_gauss_gray_queue_gpt.jpg'    # 二値化された画像パス
    all_people_count = 0    # 行列の人数
    threshold = 1000        # ピクセルごとのしきい値

    image_vertical_split(binary_img_path, 100, save_folder_path)    # 画像の縦分割

    # queue_v_split_(4~8)の人数を計算
    for i in range(4, 9):

        split_image_path = f'./img/split_img/queue_v_split_{i}.jpg'
        all_people_count += count_black_pixels(split_image_path, threshold)

        threshold *= 2  # 人の大きさに合うしきい値を設定

    # 総人数
    print(all_people_count)

if __name__ == "__main__":
    main()