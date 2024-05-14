import cv2
import os
import time
from datetime import datetime
import subprocess
import requests
import json

def capture_image(folder_path, file_prefix):
    # カメラの初期化
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("カメラを開くことができませんでした")
        return

    # フレームをキャプチャ
    ret, frame = cap.read()

    if ret:
        # 現在の時刻を取得してファイル名を作成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{file_prefix}.jpg"
        file_path = os.path.join(folder_path, file_name)

        # 画像を保存
        cv2.imwrite(file_path, frame)
        print(f"画像を保存しました: {file_path}")
    else:
        print("フレームをキャプチャできませんでした")

    # カメラを解放
    cap.release()

def main():
    folder_path = "/Users/qingjiu/kyodai/m1/project/yolov5/data/images"  # 例: "/path/to/save/images"
    file_prefix = "webcam_image"
    file_path = os.path.join(folder_path, file_prefix + ".jpg")

    # JSON 文件路径
    json_file_path = "/Users/qingjiu/kyodai/m1/project/yolov5/runs/counting_data.json"
    


    # フォルダが存在しない場合は作成
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    while True:
        # 画像をキャプチャして保存
        capture_image(folder_path, file_prefix)

        #分析
        command = f"python /Users/qingjiu/kyodai/m1/project/yolov5/detect.py --source {file_path}"
        subprocess.run(command, shell=True)

        #jsonを送る
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        first_dict = data[0]
        
        url = 'https://shockdawnbackend.onrender.com/real_data/line'
        response = requests.post(url, json=first_dict)

        print(response.text)


        # 60秒待機
        time.sleep(10)



if __name__ == "__main__":
    main()