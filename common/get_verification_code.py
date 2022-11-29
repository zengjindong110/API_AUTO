import base64
import hashlib
import json
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


def get_verify_code(files):
    code = requests.post("http://pred.fateadm.com/api/capreg", params=param, headers=header, files=files).json()
    return code


def md5(data):
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()


class VerificationCode(object):
    def __init__(self):
        self.jd_AppKey = "d1b127b57e7763a13aa69a7396baccdc"
        self.jd_SecretKey = "8cf3e7ae5265cf5f5aca2dd45df1c3f2"
        self.timestamp = int(time.time() * 1000)

    def jd_code(self):
        jd_url = "https://aiapi.jd.com/jdai/ocr_universal_v2"
        headers = {"Content-Type": "application/json"}
        jd_url = jd_url + self.jd_AppKey + str(self.timestamp) + md5(self.jd_SecretKey + str(self.timestamp))
        responds = requests.post(url=jd_url, headers=headers, data={
            "imageUrl": "https://c-ssl.duitang.com/uploads/item/202005/23/20200523172615_aUNVY.thumb.1000_0.jpeg"})
        return responds


class TuJian(object):

    # 一、图片文字类型(默认 3 数英混合)：
    # 1 : 纯数字
    # 1001：纯数字2
    # 2 : 纯英文
    # 1002：纯英文2
    # 3 : 数英混合
    # 1003：数英混合2
    #  4 : 闪动GIF
    # 7 : 无感学习(独家)
    # 11 : 计算题
    # 1005:  快速计算题
    # 16 : 汉字
    # 32 : 通用文字识别(证件、单据)
    # 66:  问答题
    # 49 :recaptcha图片识别
    # 二、图片旋转角度类型：
    # 29 :  旋转类型
    #
    # 三、图片坐标点选类型：
    # 19 :  1个坐标
    # 20 :  3个坐标
    # 21 :  3 ~ 5个坐标
    # 22 :  5 ~ 8个坐标
    # 27 :  1 ~ 4个坐标
    # 48 : 轨迹类型
    #
    # 四、缺口识别
    # 18 : 缺口识别（需要2张图 一张目标图一张缺口图）
    # 33 : 单缺口识别（返回X轴坐标 只需要1张图）
    # 五、拼图识别
    # 53：拼图识别
    def base64_api(self, uname, pwd, img, typeid):
        with open(img, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            b64 = base64_data.decode()

        data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
        result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
        if result['success']:
            return result["data"]["result"]
        else:
            return result["message"]
        return ""


if __name__ == '__main__':
    TT = TuJian()
    result = TT.base64_api(uname='admin', pwd='abc123', img=r"C:\Users\Administrator\Downloads\graphic.png", typeid=1)

    print(result)
