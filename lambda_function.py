import boto3
from decimal import Decimal
import json
import urllib.request
import urllib.parse
import urllib.error
import base64

print('Loading function')

rekognition = boto3.client('rekognition')


# --------------- Helper Functions to call Rekognition APIs ------------------


def call_rekognition(img_byte):
    '''
    Amazon Rekognitionを叩く
    '''
    response = rekognition.detect_faces(Image={'Bytes':img_byte}, Attributes=['ALL'])
    return response

# --------------- Main handler ------------------


def lambda_handler(event, context):
    '''
    APIでPOSTされたデータはハンドラで設定されたこの関数のeventで取得できる
    '''
    print("Received event: " + json.dumps(event, indent=2))

    try:
        img_b64 = event["Image"] # この"Image"は任意．APIの設計次第
        # JSONがByte形式を送信できなかったので一度文字列にして送られてくる．
        # Byteに変換してRekognitionを叩く
        img_byte = base64.b64decode(img_b64.encode("utf8"))
        response = call_rekognition(img_byte)
        return response
    except Exception as e:
        print(e)
        raise e