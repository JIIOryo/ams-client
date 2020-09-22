import datetime
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.config import get_camera_config
from service.camera import take_pictures

"""
cronによって毎分実行される
その分にタイマーが設定されているカメラの撮影リクエストを送信する
python3 cameras.py
"""

def main():
    now = datetime.datetime.now()
    hour, minute = now.hour, now.minute
    cameras = get_camera_config()

    target_camera_ids = []

    # 全てのカメラをチェック
    for camera in cameras:
        # timerがなかったら次へ
        if 'timer' not in camera:
            continue

        timers = camera['timer']

        # 対象のカメラが今写真を取るべきかチェック
        for timer in timers:
            if timer['hour'] == hour and timer['minute'] == minute:
                target_camera_ids.append(camera['camera_id'])
                continue
    
    take_pictures(target_camera_ids)

if __name__ == '__main__':
    main()
