import json
import base64

import requests
from PIL import ImageGrab
import cv2
import numpy as np


def get_image_bytes(filename):
    '''
    filenameの画像をbyte変換する
    '''
    # スケールの設定
    scale_factor = .15

    frame = cv2.imread(filename)
    height, width, channels = frame.shape
    frame = cv2.resize(frame,(int(width/2),int(height/2)),interpolation = cv2.INTER_AREA)

    # フレームをキャプチャ取得
    height, width, channels = frame.shape
    frame = cv2.resize(frame,(int(width/2),int(height/2)),interpolation = cv2.INTER_AREA)

    # jpgに変換 画像ファイルをインターネットを介してAPIで送信するのでサイズを小さくしておく
    small = cv2.resize(frame, (int(width * scale_factor), int(height * scale_factor)))
    ret, buf = cv2.imencode('.jpg', small)

    return buf.tobytes()

def aws_post(img_bytes):
    # byteのままではPOSTできないのでstringに変換
    bytes_str = base64.b64encode(img_bytes).decode()
	  
    URL = "APIエンドポイント"
    headers = {
      'Content-Type': 'application/json',
      'x-api-key': 'APIキー',
    }
    data = {'Image':bytes_str}

    response = requests.post(url=URL, data=json.dumps(data), headers=headers)
    return response

if __name__ == "__main__":
    img_bytes = get_image_bytes("ファイル名")
    response = aws_post(img_bytes)
    print(response.json())