import hashlib
import time

import requests

pd_id = "126723"
pd_key = "JJD8vbcCsyCKpM5415HoX6HyiSVUE1QR"
app_id = "326723"
app_key = "ozYE3DEtf5Ymvw88SQ45GUd6VBstOFtn"

pred_type = "30400"
FATEA_PRED_URL = "http://pred.fateadm.com"
tm = str(int(time.time()))
header = {'User-Agent': 'Mozilla/5.0'}


def CalcSign(pd_id, passwd, timestamp):
    md5 = hashlib.md5()
    md5.update((timestamp + passwd).encode())
    csign = md5.hexdigest()

    md5 = hashlib.md5()
    md5.update((pd_id + timestamp + csign).encode())
    csign = md5.hexdigest()
    return csign


sign = CalcSign(pd_id, pd_key, tm)

aSign = CalcSign(app_id, app_key, tm)
param = {
    "user_id": pd_id,
    "timestamp": tm,
    "sign": sign,
    "appid": app_id,
    "asign": aSign,
    "predict_type": pred_type,
    "up_type": "mt",
    "src_url": "",

}


def get_verify_code(image_url):
    headers = {
        "host": "dbq.asptest.yiye.ai",
        "pragma": "no-cache",
        "referer": "https://dbq.asptest.yiye.ai/login",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "windows",
        "seC-fetcH-dest": "image",
        "seC-fetcH-mode": "no-cors",
        "seC-fetcH-site": "same-origin",
        "useR-agent": "mozilla/5.0 (windOWs NT 10.0; Win64; x64) aPplEwebKit/537.36 (KHTml, lIke gecKo) chrome/99.0.4844.51 safari/537.36",
    }

    img_data = requests.get(url=image_url, headers=headers).content

    files = {
        'img_data': ('img_data', img_data)
    }
    code = requests.post("http://pred.fateadm.com/api/capreg", params=param, headers=header, files=files).json()
    return code


if __name__ == '__main__':
    x = get_verify_code("https://agent-test.yiye.ai/api/v1/ucenter/captchas/fetch/graphic?captchaKey=867f0376")
    print(x)
