import cv2
import os
import time
from datetime import datetime
import subprocess
import requests
import json
import cv2
from datetime import datetime, timedelta

def extract_frames(video_path, output_folder, interval=10):
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # 获取视频帧率
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Frames per second: {fps}")

    # 计算每隔多少帧进行截取
    frame_interval = int(fps * interval)

    frame_count = 0
    frame_time = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            
            output_filename = f"{output_folder}/frame_at_{frame_time}s.jpg"
            if not os.path.exists(output_folder):
                 os.makedirs(output_folder)
            cv2.imwrite(output_filename, frame)
            print(f"Saved frame at {frame_time} seconds: {output_filename}")
            frame_time += 10

        frame_count += 1

    cap.release()
    print("Done extracting frames.")


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
    # folder_path = "/Users/qingjiu/kyodai/m1/project/yolov5/data/images"  # 例: "/path/to/save/images"
    # file_prefix = "webcam_image"
    # file_path = os.path.join(folder_path, file_prefix + ".jpg")


    ###########CHANGE HERE！！！！！！！！！########
    #read file
    # video_path = '/Users/qingjiu/kyodai/m1/project/yolov5/data/demo/cafe1.MOV'
    video_path = '/Users/qingjiu/kyodai/m1/project/yolov5/data/demo/cafe2.MOV'
    output_folder = '/Users/qingjiu/kyodai/m1/project/yolov5/data/demo/video_image'
    extract_frames(video_path, output_folder, interval=10)

    # JSON 文件路径
    json_file_path = "/Users/qingjiu/kyodai/m1/project/yolov5/runs/counting_data.json"
    


    # # フォルダが存在しない場合は作成
    # if not os.path.exists(folder_path):
    #     os.makedirs(folder_path)

    #to process on the time
    frame_time = 0


    ###########CHANGE HERE！！！！！！！！！########
    #time set
    # custom_time = datetime(2023, 5, 20, 11, 37, 00)
    custom_time = datetime(2023, 5, 20, 12, 11, 00)

    for _ in range(7):
        # 画像をキャプチャして保存
        # capture_image(folder_path, file_prefix)

        #分析
        command = f"python /Users/qingjiu/kyodai/m1/project/yolov5/detect.py --source {output_folder}/frame_at_{frame_time}s.jpg"
        subprocess.run(command, shell=True)

        #interval is 10 second
        frame_time += 10

        #jsonを送る
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        first_dict = data[0]

        
        print(first_dict)
        first_dict["timestamp"] = custom_time

        #turn the timestamp into string to make sure post successfully
        pass_dict = first_dict
        pass_dict['timestamp'] = pass_dict['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        

        url = 'https://shockdawnbackend.onrender.com/real_data/line'
        response = requests.post(url, json=pass_dict)

        print(response.text)

        #increase the time of timestamp in json file
        custom_time += timedelta(seconds=10)
        # 10秒待機
        time.sleep(7)




if __name__ == "__main__":
    main()