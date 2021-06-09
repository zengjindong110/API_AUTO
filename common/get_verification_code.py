# coding=gbk


import hashlib
import time
import json
import requests

pd_id = "126723"  # 用户中心页可以查询到pd信息
pd_key = "JJD8vbcCsyCKpM5415HoX6HyiSVUE1QR"
app_id = "326723"  # 开发者分成用的账号，在开发者中心可以查询到
app_key = "ozYE3DEtf5Ymvw88SQ45GUd6VBstOFtn"
# 识别类型，
# 具体类型可以查看官方网站的价格页选择具体的类型，不清楚类型的，可以咨询客服
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
    x = get_verify_code("https://order.lbdj.com/lbdj/web/user/loginverify?v=0.6836869490327788&u=yKHDtuP2")
    print(x)
