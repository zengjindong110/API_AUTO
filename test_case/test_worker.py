# coding=gbk


import unittest
import warnings
import config
from common.assert_data import *
from common.get_request_data import *
from common.request_api import RequestApi
from common.work_common import *


class TestWorkerOrder(unittest.TestCase):
    args = get_request_data("/lbdj/web/saveOrder")

    def tearDown(self):  # 每个用例运行之后运行的
        key_list.clear()

    @classmethod
    def tearDownClass(cls):  # 在所有用例都执行完之后运行的
        warnings.simplefilter('ignore', ResourceWarning)

    def test_jiaju_anzhuang_yikoujia(self):  # 函数名要以test开头，否则不会被执行
        """家居安装一口价师傅安装"""

        order = get_order("140", "anz")  # 查询订单家居安一口价--悬赏装品类
        self.assertNotEqual(order["id"], "error", msg=order)
        order_id = order["id"]
        order_sn = order["orderNum"]
        reserve_HomeCheck(order)

        InstallCheckData = get_request_data("/lbdj/app/order/AddOrderInstallCheckApiRequest")[0]  # 获取装前检测的请求参数

        InstallCheckReq = json.loads(InstallCheckData["data"])
        InstallCheckReq["orderId"] = order_id
        InstallCheckRes = RequestApi.worker_requests(InstallCheckData["method"], InstallCheckData["uri"],
                                                     InstallCheckReq)  # 装前检测

        self.assertTrue(assert_key(InstallCheckData["assert"], InstallCheckRes.text), msg="预期的key与实际的key不一样")

        UploadDoneImageData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest")[0]  # 获取完工请求参数
        UploadDoneImageReq = json.loads(UploadDoneImageData["data"])
        UploadDoneImageReq["orderId"] = order_id
        UploadDoneImageReq["finishImages"][0]["goodName"] = my_order_info(order_id, order_sn)["goodsName"]
        UploadDoneImageRes = RequestApi.worker_requests(UploadDoneImageData["method"], UploadDoneImageData["uri"],
                                                        UploadDoneImageReq)  # 上传完工图
        self.assertTrue(assert_key(UploadDoneImageData["assert"], UploadDoneImageRes.text), msg="预期的key与实际的key不一样")

        DoneImageReq = {"orderId": order_id, "type": 3,
                        "images": "[\"writing/20201029/0D3D8E2DC02B4AF3D15FF7E1A009413B.png\"]", "videoAddress": ""}
        RequestApi.worker_requests("post", "/lbdj/app/order/AppUploadDoneImageApiRequest",
                                   DoneImageReq)  # 电子签收单确认
        """type: 图片类型：1.完工图/完工视频 2.好评返现图 3.签收图"""
        respond = ServiceDone(order)
        self.assertEqual(respond["msg"], "成功", msg=respond)

    def test_weiyu_anzhuang_yikoujia(self):
        """卫浴——安装——一口价 师傅安装"""

        order = get_order("202", "anz")  # 查询订单卫浴安装一口价--悬赏装品类
        self.assertNotEqual(order["id"], "error", msg=order)

        reserve_HomeCheck(order)

        order_id = order["id"]
        order_sn = order["orderNum"]

        AddPunchingData = get_request_data("/lbdj/app/order/AppAddPunchingApiRequest")[0]  # 查询打孔证明请求参数
        AddPunchingReq = json.loads(AddPunchingData["data"])
        AddPunchingReq["orderId"] = order_id
        AddPunchingReq["orderSn"] = order_sn
        AddPunchingRes = RequestApi.worker_requests(AddPunchingData["method"], AddPunchingData["uri"],
                                                    AddPunchingReq)  # 请求打孔证明接口
        self.assertTrue(assert_key(AddPunchingData["assert"], AddPunchingRes.text), msg="预期的key与实际的key不一样")

        SaveCheckConfirmData = get_request_data("/lbdj/app/order/AppSaveCheckConfirmOrderRecordApiRequest")[
            0]  # 保存订单装后验收确认项数据
        SaveCheckConfirmReq = json.loads(SaveCheckConfirmData["data"])
        SaveCheckConfirmReq["orderId"] = order_id

        SaveCheckConfirmRes = RequestApi.worker_requests(SaveCheckConfirmData["method"], SaveCheckConfirmData["uri"],
                                                         SaveCheckConfirmReq)  # 请求订单装后验收接口
        self.assertTrue(assert_key(SaveCheckConfirmData["assert"], SaveCheckConfirmRes.text), msg="预期的key与实际的key不一样")

        UploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "卫浴一口价上传完工图")[
            0]  # 查询卫浴一口价上传完工图请求参数
        UploadDoneReq = json.loads(UploadDoneData["data"])
        UploadDoneReq["orderId"] = order_id
        UploadDoneReq["finishImages"][0]["goodName"] = my_order_info(order_id, order_sn)["goodsName"]
        UploadDoneRes = RequestApi.worker_requests(UploadDoneData["method"], UploadDoneData["uri"],
                                                   UploadDoneReq)  # 请求卫浴一口价上传完工图接口
        self.assertTrue(assert_key(UploadDoneData["assert"], UploadDoneRes.text), msg="预期的key与实际的key不一样")

        signUploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "卫浴一口价上传签收图")[
            0]  # 查询卫浴一口价上传签收图请求参数
        signUploadDoneReq = json.loads(signUploadDoneData["data"])
        signUploadDoneReq["orderId"] = order_id

        signUploadDoneRes = RequestApi.worker_requests(signUploadDoneData["method"], signUploadDoneData["uri"],
                                                       signUploadDoneReq)  # 请求卫浴一口价上传签收图接口
        self.assertTrue(assert_key(signUploadDoneData["assert"], signUploadDoneRes.text), msg="预期的key与实际的key不一样")
        respond = ServiceDone(order)
        self.assertEqual(respond["msg"], "成功", msg=respond)

    def test_liangyijia_anzhuang_yikoujia(self):
        """晾衣架安装一口价或者自定义一口价订单"""
        order = get_order("139", "anz")  # 查询晾衣架安装一口价--悬赏装品类订单
        self.assertNotEqual(order["id"], "error", msg=order)
        reserve_HomeCheck(order)
        order_id = order["id"]
        order_sn = order["orderNum"]
        InstallCheckData = get_request_data("/lbdj/app/order/AddOrderInstallCheckApiRequest", "晾衣架装前检测")[
            0]  # 获取晾衣架装前检测的请求数据
        InstallCheckReq = json.loads(InstallCheckData["data"])
        InstallCheckReq["orderId"] = order_id

        InstallCheckRes = RequestApi.worker_requests(InstallCheckData["method"], InstallCheckData["uri"],
                                                     InstallCheckReq)  # 请求晾衣架装前检测接口
        self.assertTrue(assert_key(InstallCheckData["assert"], InstallCheckRes.text), msg="预期的key与实际的key不一样")

        PunchingData = get_request_data("/lbdj/app/order/AppAddPunchingApiRequest", "晾衣架打孔证明")[
            0]  # 获取晾衣架装前检测的请求数据
        PunchingReq = json.loads(PunchingData["data"])
        PunchingReq["orderId"] = order_id

        PunchingRes = RequestApi.worker_requests(PunchingData["method"], PunchingData["uri"],
                                                 PunchingReq)  # 请求晾衣架打孔证明接口
        self.assertTrue(assert_key(PunchingData["assert"], PunchingRes.text), msg="预期的key与实际的key不一样")

        UploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "晾衣架完工图")[
            0]  # 查询卫浴一口价上传完工图请求参数
        UploadDoneReq = json.loads(UploadDoneData["data"])
        UploadDoneReq["orderId"] = order_id
        UploadDoneReq["finishImages"][0]["goodName"] = my_order_info(order_id, order_sn)["goodsName"]
        UploadDoneRes = RequestApi.worker_requests(UploadDoneData["method"], UploadDoneData["uri"],
                                                   UploadDoneReq)  # 请求卫浴一口价上传完工图接口
        self.assertTrue(assert_key(UploadDoneData["assert"], UploadDoneRes.text), msg="预期的key与实际的key不一样")

        signUploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "晾衣架签收图")[
            0]  # 查询晾衣架一口价上传签收图请求参数
        signUploadDoneReq = json.loads(signUploadDoneData["data"])
        signUploadDoneReq["orderId"] = order_id
        signUploadDoneRes = RequestApi.worker_requests(signUploadDoneData["method"], signUploadDoneData["uri"],
                                                       signUploadDoneReq)  # 请求晾衣架一口价上传签收图接口
        self.assertTrue(assert_key(signUploadDoneData["assert"], signUploadDoneRes.text), msg="预期的key与实际的key不一样")
        respond = ServiceDone(order)
        self.assertEqual(respond["msg"], "成功", msg=respond)

    def test_chuanglian_anzhuang_yikoujia(self):
        """窗帘量尺安装一口价（自定义一口价）订单"""
        order = get_order("136", "anz")  # 查询窗帘安装一口价--悬赏装品类订单
        self.assertNotEqual(order["id"], "error", msg=order)
        reserve_HomeCheck(order)
        order_id = order["id"]
        order_sn = order["orderNum"]
        PunchingData = get_request_data("/lbdj/app/order/AppAddPunchingApiRequest", "窗帘一口价上传打孔证明")[
            0]  # 获取晾衣架装前检测的请求数据
        PunchingReq = json.loads(PunchingData["data"])
        PunchingReq["orderId"] = order_id

        PunchingRes = RequestApi.worker_requests(PunchingData["method"], PunchingData["uri"],
                                                 PunchingReq)  # 请求窗帘一口价上传完工图接口
        self.assertTrue(assert_key(PunchingData["assert"], PunchingRes.text), msg="预期的key与实际的key不一样")
        UploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "窗帘一口价上传完工图")[
            0]  # 查询窗帘一口价上传完工图请求参数
        UploadDoneReq = json.loads(UploadDoneData["data"])
        UploadDoneReq["orderId"] = order_id
        UploadDoneReq["finishImages"][0]["goodName"] = my_order_info(order_id, order_sn)["goodsName"]
        UploadDoneRes = RequestApi.worker_requests(UploadDoneData["method"], UploadDoneData["uri"],
                                                   UploadDoneReq)  # 请求窗帘一口价上传完工图接口
        self.assertTrue(assert_key(UploadDoneData["assert"], UploadDoneRes.text), msg="预期的key与实际的key不一样")

        signUploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "窗帘一口价上传签收单")[
            0]  # 查询窗帘一口价上传签收单请求参数
        signUploadDoneReq = json.loads(signUploadDoneData["data"])
        signUploadDoneReq["orderId"] = order_id
        signUploadDoneRes = RequestApi.worker_requests(signUploadDoneData["method"], signUploadDoneData["uri"],
                                                       signUploadDoneReq)  # 请求窗帘一口价上传签收单接口
        self.assertTrue(assert_key(signUploadDoneData["assert"], signUploadDoneRes.text), msg="预期的key与实际的key不一样")

        respond = ServiceDone(order)
        self.assertEqual(respond["msg"], "成功", msg=respond)

    def test_suolei_anzhuang_yikoujia(self):
        """锁类安装一口价师傅"""
        order = get_order("149", "anz")  # 查询锁类安装一口价--悬赏装品类订单
        self.assertNotEqual(order["id"], "error", msg=order)
        reserve_HomeCheck(order)
        order_id = order["id"]
        order_sn = order["orderNum"]
        InstallCheckData = get_request_data("/lbdj/app/order/AddOrderInstallCheckApiRequest", "锁类装前检测")[
            0]  # 获取锁类装前检测的请求数据
        InstallCheckReq = json.loads(InstallCheckData["data"])
        InstallCheckReq["orderId"] = order_id

        InstallCheckRes = RequestApi.worker_requests(InstallCheckData["method"], InstallCheckData["uri"],
                                                     InstallCheckReq)  # 请求锁类装前检测接口
        self.assertTrue(assert_key(InstallCheckData["assert"], InstallCheckRes.text), msg="预期的key与实际的key不一样")

        UploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "锁类完工图")[
            0]  # 查询锁类完工图一口价上传完工图请求参数
        UploadDoneReq = json.loads(UploadDoneData["data"])
        UploadDoneReq["orderId"] = order_id
        UploadDoneReq["finishImages"][0]["goodName"] = my_order_info(order_id, order_sn)["goodsName"]
        UploadDoneRes = RequestApi.worker_requests(UploadDoneData["method"], UploadDoneData["uri"],
                                                   UploadDoneReq)  # 请求锁类完工图一口价上传完工图接口
        self.assertTrue(assert_key(UploadDoneData["assert"], UploadDoneRes.text), msg="预期的key与实际的key不一样")

        signUploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "锁类签收图")[
            0]  # 查询锁类签收图一口价上传签收图请求参数
        signUploadDoneReq = json.loads(signUploadDoneData["data"])
        signUploadDoneReq["orderId"] = order_id
        signUploadDoneRes = RequestApi.worker_requests(signUploadDoneData["method"], signUploadDoneData["uri"],
                                                       signUploadDoneReq)  # 请求锁类签收图一口价上传签收图接口
        self.assertTrue(assert_key(signUploadDoneData["assert"], signUploadDoneRes.text), msg="预期的key与实际的key不一样")
        respond = ServiceDone(order)
        self.assertEqual(respond["msg"], "成功", msg=respond)

    def test_dengju_anzhuang_yikoujia(self):
        """灯具类安装一口价师傅"""
        order = get_order("138", "anz")  # 查询灯具安装一口价--悬赏装品类订单
        self.assertNotEqual(order["id"], "error", msg=order)
        reserve_HomeCheck(order)
        order_id = order["id"]
        order_sn = order["orderNum"]
        InstallCheckData = get_request_data("/lbdj/app/order/AddOrderInstallCheckApiRequest", "灯具装前检测")[
            0]  # 获取灯具装前检测的请求数据
        InstallCheckReq = json.loads(InstallCheckData["data"])
        InstallCheckReq["orderId"] = order_id

        InstallCheckRes = RequestApi.worker_requests(InstallCheckData["method"], InstallCheckData["uri"],
                                                     InstallCheckReq)  # 请求灯具装前检测接口
        self.assertTrue(assert_key(InstallCheckData["assert"], InstallCheckRes.text), msg="预期的key与实际的key不一样")

        UploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "灯具完工图")[
            0]  # 查询灯具完工图一口价上传完工图请求参数
        UploadDoneReq = json.loads(UploadDoneData["data"])
        UploadDoneReq["orderId"] = order_id
        UploadDoneReq["finishImages"][0]["goodName"] = my_order_info(order_id, order_sn)["goodsName"]
        UploadDoneRes = RequestApi.worker_requests(UploadDoneData["method"], UploadDoneData["uri"],
                                                   UploadDoneReq)  # 请求灯具完工图一口价上传完工图接口
        self.assertTrue(assert_key(UploadDoneData["assert"], UploadDoneRes.text), msg="预期的key与实际的key不一样")

        signUploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "灯具签收图")[
            0]  # 查询灯具签收图一口价上传签收图请求参数
        signUploadDoneReq = json.loads(signUploadDoneData["data"])
        signUploadDoneReq["orderId"] = order_id
        signUploadDoneRes = RequestApi.worker_requests(signUploadDoneData["method"], signUploadDoneData["uri"],
                                                       signUploadDoneReq)  # 请求灯具签收图一口价上传签收图接口
        self.assertTrue(assert_key(signUploadDoneData["assert"], signUploadDoneRes.text), msg="预期的key与实际的key不一样")
        respond = ServiceDone(order)
        self.assertEqual(respond["msg"], "成功", msg=respond)

    def test_jingshuiqi_anzhuang_yikoujia(self):
        pass

    def test_jiadian_anzhuang_baojia(self):
        """家电安装师傅"""
        order = get_order("148", "anz")  # 查询家电安装一口价--悬赏装品类订单
        self.assertNotEqual(order["id"], "error", msg=order)
        reserve_HomeCheck(order)
        order_id = order["id"]
        order_sn = order["orderNum"]
        UploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "家电安装一口价完工图")[
            0]  # 查询家电安装一口价完工图上传完工图请求参数

        UploadDoneReq = json.loads(UploadDoneData["data"])
        UploadDoneReq["orderId"] = order_id
        UploadDoneReq["finishImages"][0]["goodName"] = my_order_info(order_id, order_sn)["goodsName"]
        UploadDoneRes = RequestApi.worker_requests(UploadDoneData["method"], UploadDoneData["uri"],
                                                   UploadDoneReq)  # 请求家电安装一口价完工图上传完工图接口
        self.assertTrue(assert_key(UploadDoneData["assert"], UploadDoneRes.text), msg="预期的key与实际的key不一样")

        signUploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "家电安装一口价签收图")[
            0]  # 查询家电安装一口价签收图上传签收图请求参数
        signUploadDoneReq = json.loads(signUploadDoneData["data"])
        signUploadDoneReq["orderId"] = order_id
        signUploadDoneRes = RequestApi.worker_requests(signUploadDoneData["method"], signUploadDoneData["uri"],
                                                       signUploadDoneReq)  # 请求家电安装一口价签收图上传签收图接口
        self.assertTrue(assert_key(signUploadDoneData["assert"], signUploadDoneRes.text), msg="预期的key与实际的key不一样")
        respond = ServiceDone(order)
        self.assertEqual(respond["msg"], "成功", msg=respond)

    def test_diban_anzhuang_yikoujia(self):
        """地板安装师傅"""
        order = get_order("141", "anz")  # 查询地板类安装一口价--悬赏装品类订单
        self.assertNotEqual(order["id"], "error", msg=order)
        reserve_HomeCheck(order)
        order_id = order["id"]
        order_sn = order["orderNum"]
        UploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "地板安装一口价完工图")[
            0]  # 查询地板安装一口价完工图上传完工图请求参数

        UploadDoneReq = json.loads(UploadDoneData["data"])
        UploadDoneReq["orderId"] = order_id
        UploadDoneReq["finishImages"][0]["goodName"] = my_order_info(order_id, order_sn)["goodsName"]
        UploadDoneRes = RequestApi.worker_requests(UploadDoneData["method"], UploadDoneData["uri"],
                                                   UploadDoneReq)  # 请求地板安装一口价完工图上传完工图接口
        self.assertTrue(assert_key(UploadDoneData["assert"], UploadDoneRes.text), msg="预期的key与实际的key不一样")

        signUploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "地板安装一口价签收图")[
            0]  # 查询地板安装一口价签收图上传签收图请求参数
        signUploadDoneReq = json.loads(signUploadDoneData["data"])
        signUploadDoneReq["orderId"] = order_id
        signUploadDoneRes = RequestApi.worker_requests(signUploadDoneData["method"], signUploadDoneData["uri"],
                                                       signUploadDoneReq)  # 请求地板安装一口价签收图上传签收图接口
        self.assertTrue(assert_key(signUploadDoneData["assert"], signUploadDoneRes.text), msg="预期的key与实际的key不一样")
        respond = ServiceDone(order)
        self.assertEqual(respond["msg"], "成功", msg=respond)

    def test_menlei_anzhuang_yikoujia(self):
        """门类一口价安装"""
        order = get_order("143", "anz")  # 查询门类安装一口价--悬赏装品类订单
        self.assertNotEqual(order["id"], "error", msg=order)
        reserve_HomeCheck(order)
        order_id = order["id"]
        order_sn = order["orderNum"]
        UploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "门类安装一口价完工图")[
            0]  # 查询门类安装一口价完工图上传完工图请求参数

        UploadDoneReq = json.loads(UploadDoneData["data"])
        UploadDoneReq["orderId"] = order_id
        UploadDoneReq["finishImages"][0]["goodName"] = my_order_info(order_id, order_sn)["goodsName"]
        UploadDoneRes = RequestApi.worker_requests(UploadDoneData["method"], UploadDoneData["uri"],
                                                   UploadDoneReq)  # 请求门类安装一口价完工图上传完工图接口
        self.assertTrue(assert_key(UploadDoneData["assert"], UploadDoneRes.text), msg="预期的key与实际的key不一样")

        signUploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "门类安装一口价签收图")[
            0]  # 查询门类安装一口价签收图上传签收图请求参数
        signUploadDoneReq = json.loads(signUploadDoneData["data"])
        signUploadDoneReq["orderId"] = order_id
        signUploadDoneRes = RequestApi.worker_requests(signUploadDoneData["method"], signUploadDoneData["uri"],
                                                       signUploadDoneReq)  # 请求门类安装一口价签收图上传签收图接口
        self.assertTrue(assert_key(signUploadDoneData["assert"], signUploadDoneRes.text), msg="预期的key与实际的key不一样")
        respond = ServiceDone(order)
        self.assertEqual(respond["msg"], "成功", msg=respond)

    def test_qiangzhi_anzhuang_yikoujia(self):
        """墙纸安装一口价师傅"""

        order = get_order("142", "anz")  # 查询墙纸安装一口价--悬赏装品类订单
        self.assertNotEqual(order["id"], "error", msg=order)
        reserve_HomeCheck(order)
        order_id = order["id"]
        order_sn = order["orderNum"]
        UploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "墙纸安装一口价完工图")[
            0]  # 查询墙纸安装一口价完工图上传完工图请求参数

        UploadDoneReq = json.loads(UploadDoneData["data"])
        UploadDoneReq["orderId"] = order_id
        UploadDoneReq["finishImages"][0]["goodName"] = my_order_info(order_id, order_sn)["goodsName"]
        UploadDoneRes = RequestApi.worker_requests(UploadDoneData["method"], UploadDoneData["uri"],
                                                   UploadDoneReq)  # 请求墙纸安装一口价完工图上传完工图接口
        self.assertTrue(assert_key(UploadDoneData["assert"], UploadDoneRes.text), msg="预期的key与实际的key不一样")

        signUploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "墙纸安装一口价签收图")[
            0]  # 查询墙纸安装一口价签收图传签收图请求参数
        signUploadDoneReq = json.loads(signUploadDoneData["data"])
        signUploadDoneReq["orderId"] = order_id
        signUploadDoneRes = RequestApi.worker_requests(signUploadDoneData["method"], signUploadDoneData["uri"],
                                                       signUploadDoneReq)  # 请求墙纸安装一口价签收图上传签收图接口
        self.assertTrue(assert_key(signUploadDoneData["assert"], signUploadDoneRes.text), msg="预期的key与实际的key不一样")
        respond = ServiceDone(order)
        self.assertEqual(respond["msg"], "成功", msg=respond)

    def test_worker_baojia(self):
        """师傅订单报价"""

        ApiRequestData = json.loads(
            get_request_data("/lbdj/app/order/AppGrabOrderHallApiRequest", "查看师傅报价订单")[0]["data"])
        ApiRequestData["token"] = config.worker_environment["test"]["token"]
        wait_baojia = RequestApi.worker_requests("post", "/lbdj/app/order/AppGrabOrderHallApiRequest",
                                                 ApiRequestData).json()
        order_id = wait_baojia["data"][0]["id"]

        GrabOrderData = get_request_data("/lbdj/app/order/AppGrabOrderApiRequest", "师傅报价")[0]
        GrabOrderReq = json.loads(GrabOrderData["data"])
        GrabOrderReq["id"] = order_id
        GrabOrderRes = RequestApi.worker_requests(GrabOrderData["method"], GrabOrderData["uri"], GrabOrderReq)
        self.assertTrue(assert_key(GrabOrderData["assert"], GrabOrderRes.text), msg="预期的key与实际的key不一样")

    def test_get_zhipai_dingdan(self):
        """获取指派订单"""
        # wait_baojia = RequestApi.worker_requests("post", "/lbdj/app/order/AppGrabOrderHallApiRequest", data).json()
        # order_id = wait_baojia["data"][0]["id"]

        GrabOrderData = get_request_data("/lbdj/app/order/AppGrabOrderHallApiRequest", "获取指派订单")[0]
        GrabOrderReq = json.loads(GrabOrderData["data"])

        GrabOrderReq["token"] = config.worker_environment["test"]["token"]

        GrabOrderRes = RequestApi.worker_requests(GrabOrderData["method"], GrabOrderData["uri"],
                                                  GrabOrderReq)
        if GrabOrderRes.json()["data"] == []:
            self.assertEqual(GrabOrderRes.text, '{"isSuccess":true,"code":"200","msg":"成功","data":[]}',
                             msg=GrabOrderRes.text)
        else:
            self.assertTrue(assert_key(GrabOrderData["assert"], GrabOrderRes.text), msg="预期的key与实际的key不一样")


if __name__ == '__main__':
    # reserve_HomeCheck()
    # unittest.main()
    # print(get_order("140", "anz", 0))
    suit = unittest.TestSuite()
    suit.addTest(TestWorkerOrder("test_worker_baojia"))
    runner = unittest.TextTestRunner()
    runner.run(suit)
