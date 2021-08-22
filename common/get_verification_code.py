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
    img_data = requests.get(image_url).content

    files = {
        'img_data': ('img_data', img_data)
    }
    code = requests.post("http://pred.fateadm.com/api/capreg", params=param, headers=header, files=files).json()
    return code


if __name__ == '__main__':
    x = get_verify_code("https://agent-test.yiye.ai/api/v1/ucenter/captchas/fetch/graphic?captchaKey=867f0376")
    print(x)
