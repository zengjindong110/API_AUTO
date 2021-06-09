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

    def tearDown(self):  # ÿ����������֮�����е�
        key_list.clear()

    @classmethod
    def tearDownClass(cls):  # ������������ִ����֮�����е�
        warnings.simplefilter('ignore', ResourceWarning)

    def test_jiaju_anzhuang_yikoujia(self):  # ������Ҫ��test��ͷ�����򲻻ᱻִ��
        """�ҾӰ�װһ�ڼ�ʦ����װ"""

        order = get_order("140", "anz")  # ��ѯ�����ҾӰ�һ�ڼ�--����װƷ��
        self.assertNotEqual(order["id"], "error", msg=order)
        order_id = order["id"]
        order_sn = order["orderNum"]
        reserve_HomeCheck(order)

        InstallCheckData = get_request_data("/lbdj/app/order/AddOrderInstallCheckApiRequest")[0]  # ��ȡװǰ�����������

        InstallCheckReq = json.loads(InstallCheckData["data"])
        InstallCheckReq["orderId"] = order_id
        InstallCheckRes = RequestApi.worker_requests(InstallCheckData["method"], InstallCheckData["uri"],
                                                     InstallCheckReq)  # װǰ���

        self.assertTrue(assert_key(InstallCheckData["assert"], InstallCheckRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")

        UploadDoneImageData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest")[0]  # ��ȡ�깤�������
        UploadDoneImageReq = json.loads(UploadDoneImageData["data"])
        UploadDoneImageReq["orderId"] = order_id
        UploadDoneImageReq["finishImages"][0]["goodName"] = my_order_info(order_id, order_sn)["goodsName"]
        UploadDoneImageRes = RequestApi.worker_requests(UploadDoneImageData["method"], UploadDoneImageData["uri"],
                                                        UploadDoneImageReq)  # �ϴ��깤ͼ
        self.assertTrue(assert_key(UploadDoneImageData["assert"], UploadDoneImageRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")

        DoneImageReq = {"orderId": order_id, "type": 3,
                        "images": "[\"writing/20201029/0D3D8E2DC02B4AF3D15FF7E1A009413B.png\"]", "videoAddress": ""}
        RequestApi.worker_requests("post", "/lbdj/app/order/AppUploadDoneImageApiRequest",
                                   DoneImageReq)  # ����ǩ�յ�ȷ��
        """type: ͼƬ���ͣ�1.�깤ͼ/�깤��Ƶ 2.��������ͼ 3.ǩ��ͼ"""
        respond = ServiceDone(order)
        self.assertEqual(respond["msg"], "�ɹ�", msg=respond)

    def test_weiyu_anzhuang_yikoujia(self):
        """��ԡ������װ����һ�ڼ� ʦ����װ"""

        order = get_order("202", "anz")  # ��ѯ������ԡ��װһ�ڼ�--����װƷ��
        self.assertNotEqual(order["id"], "error", msg=order)

        reserve_HomeCheck(order)

        order_id = order["id"]
        order_sn = order["orderNum"]

        AddPunchingData = get_request_data("/lbdj/app/order/AppAddPunchingApiRequest")[0]  # ��ѯ���֤���������
        AddPunchingReq = json.loads(AddPunchingData["data"])
        AddPunchingReq["orderId"] = order_id
        AddPunchingReq["orderSn"] = order_sn
        AddPunchingRes = RequestApi.worker_requests(AddPunchingData["method"], AddPunchingData["uri"],
                                                    AddPunchingReq)  # ������֤���ӿ�
        self.assertTrue(assert_key(AddPunchingData["assert"], AddPunchingRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")

        SaveCheckConfirmData = get_request_data("/lbdj/app/order/AppSaveCheckConfirmOrderRecordApiRequest")[
            0]  # ���涩��װ������ȷ��������
        SaveCheckConfirmReq = json.loads(SaveCheckConfirmData["data"])
        SaveCheckConfirmReq["orderId"] = order_id

        SaveCheckConfirmRes = RequestApi.worker_requests(SaveCheckConfirmData["method"], SaveCheckConfirmData["uri"],
                                                         SaveCheckConfirmReq)  # ���󶩵�װ�����սӿ�
        self.assertTrue(assert_key(SaveCheckConfirmData["assert"], SaveCheckConfirmRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")

        UploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "��ԡһ�ڼ��ϴ��깤ͼ")[
            0]  # ��ѯ��ԡһ�ڼ��ϴ��깤ͼ�������
        UploadDoneReq = json.loads(UploadDoneData["data"])
        UploadDoneReq["orderId"] = order_id
        UploadDoneReq["finishImages"][0]["goodName"] = my_order_info(order_id, order_sn)["goodsName"]
        UploadDoneRes = RequestApi.worker_requests(UploadDoneData["method"], UploadDoneData["uri"],
                                                   UploadDoneReq)  # ������ԡһ�ڼ��ϴ��깤ͼ�ӿ�
        self.assertTrue(assert_key(UploadDoneData["assert"], UploadDoneRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")

        signUploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "��ԡһ�ڼ��ϴ�ǩ��ͼ")[
            0]  # ��ѯ��ԡһ�ڼ��ϴ�ǩ��ͼ�������
        signUploadDoneReq = json.loads(signUploadDoneData["data"])
        signUploadDoneReq["orderId"] = order_id

        signUploadDoneRes = RequestApi.worker_requests(signUploadDoneData["method"], signUploadDoneData["uri"],
                                                       signUploadDoneReq)  # ������ԡһ�ڼ��ϴ�ǩ��ͼ�ӿ�
        self.assertTrue(assert_key(signUploadDoneData["assert"], signUploadDoneRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")
        respond = ServiceDone(order)
        self.assertEqual(respond["msg"], "�ɹ�", msg=respond)

    def test_liangyijia_anzhuang_yikoujia(self):
        """���¼ܰ�װһ�ڼۻ����Զ���һ�ڼ۶���"""
        order = get_order("139", "anz")  # ��ѯ���¼ܰ�װһ�ڼ�--����װƷ�ඩ��
        self.assertNotEqual(order["id"], "error", msg=order)
        reserve_HomeCheck(order)
        order_id = order["id"]
        order_sn = order["orderNum"]
        InstallCheckData = get_request_data("/lbdj/app/order/AddOrderInstallCheckApiRequest", "���¼�װǰ���")[
            0]  # ��ȡ���¼�װǰ������������
        InstallCheckReq = json.loads(InstallCheckData["data"])
        InstallCheckReq["orderId"] = order_id

        InstallCheckRes = RequestApi.worker_requests(InstallCheckData["method"], InstallCheckData["uri"],
                                                     InstallCheckReq)  # �������¼�װǰ���ӿ�
        self.assertTrue(assert_key(InstallCheckData["assert"], InstallCheckRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")

        PunchingData = get_request_data("/lbdj/app/order/AppAddPunchingApiRequest", "���¼ܴ��֤��")[
            0]  # ��ȡ���¼�װǰ������������
        PunchingReq = json.loads(PunchingData["data"])
        PunchingReq["orderId"] = order_id

        PunchingRes = RequestApi.worker_requests(PunchingData["method"], PunchingData["uri"],
                                                 PunchingReq)  # �������¼ܴ��֤���ӿ�
        self.assertTrue(assert_key(PunchingData["assert"], PunchingRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")

        UploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "���¼��깤ͼ")[
            0]  # ��ѯ��ԡһ�ڼ��ϴ��깤ͼ�������
        UploadDoneReq = json.loads(UploadDoneData["data"])
        UploadDoneReq["orderId"] = order_id
        UploadDoneReq["finishImages"][0]["goodName"] = my_order_info(order_id, order_sn)["goodsName"]
        UploadDoneRes = RequestApi.worker_requests(UploadDoneData["method"], UploadDoneData["uri"],
                                                   UploadDoneReq)  # ������ԡһ�ڼ��ϴ��깤ͼ�ӿ�
        self.assertTrue(assert_key(UploadDoneData["assert"], UploadDoneRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")

        signUploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "���¼�ǩ��ͼ")[
            0]  # ��ѯ���¼�һ�ڼ��ϴ�ǩ��ͼ�������
        signUploadDoneReq = json.loads(signUploadDoneData["data"])
        signUploadDoneReq["orderId"] = order_id
        signUploadDoneRes = RequestApi.worker_requests(signUploadDoneData["method"], signUploadDoneData["uri"],
                                                       signUploadDoneReq)  # �������¼�һ�ڼ��ϴ�ǩ��ͼ�ӿ�
        self.assertTrue(assert_key(signUploadDoneData["assert"], signUploadDoneRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")
        respond = ServiceDone(order)
        self.assertEqual(respond["msg"], "�ɹ�", msg=respond)

    def test_chuanglian_anzhuang_yikoujia(self):
        """�������߰�װһ�ڼۣ��Զ���һ�ڼۣ�����"""
        order = get_order("136", "anz")  # ��ѯ������װһ�ڼ�--����װƷ�ඩ��
        self.assertNotEqual(order["id"], "error", msg=order)
        reserve_HomeCheck(order)
        order_id = order["id"]
        order_sn = order["orderNum"]
        PunchingData = get_request_data("/lbdj/app/order/AppAddPunchingApiRequest", "����һ�ڼ��ϴ����֤��")[
            0]  # ��ȡ���¼�װǰ������������
        PunchingReq = json.loads(PunchingData["data"])
        PunchingReq["orderId"] = order_id

        PunchingRes = RequestApi.worker_requests(PunchingData["method"], PunchingData["uri"],
                                                 PunchingReq)  # ������һ�ڼ��ϴ��깤ͼ�ӿ�
        self.assertTrue(assert_key(PunchingData["assert"], PunchingRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")
        UploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "����һ�ڼ��ϴ��깤ͼ")[
            0]  # ��ѯ����һ�ڼ��ϴ��깤ͼ�������
        UploadDoneReq = json.loads(UploadDoneData["data"])
        UploadDoneReq["orderId"] = order_id
        UploadDoneReq["finishImages"][0]["goodName"] = my_order_info(order_id, order_sn)["goodsName"]
        UploadDoneRes = RequestApi.worker_requests(UploadDoneData["method"], UploadDoneData["uri"],
                                                   UploadDoneReq)  # ������һ�ڼ��ϴ��깤ͼ�ӿ�
        self.assertTrue(assert_key(UploadDoneData["assert"], UploadDoneRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")

        signUploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "����һ�ڼ��ϴ�ǩ�յ�")[
            0]  # ��ѯ����һ�ڼ��ϴ�ǩ�յ��������
        signUploadDoneReq = json.loads(signUploadDoneData["data"])
        signUploadDoneReq["orderId"] = order_id
        signUploadDoneRes = RequestApi.worker_requests(signUploadDoneData["method"], signUploadDoneData["uri"],
                                                       signUploadDoneReq)  # ������һ�ڼ��ϴ�ǩ�յ��ӿ�
        self.assertTrue(assert_key(signUploadDoneData["assert"], signUploadDoneRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")

        respond = ServiceDone(order)
        self.assertEqual(respond["msg"], "�ɹ�", msg=respond)

    def test_suolei_anzhuang_yikoujia(self):
        """���లװһ�ڼ�ʦ��"""
        order = get_order("149", "anz")  # ��ѯ���లװһ�ڼ�--����װƷ�ඩ��
        self.assertNotEqual(order["id"], "error", msg=order)
        reserve_HomeCheck(order)
        order_id = order["id"]
        order_sn = order["orderNum"]
        InstallCheckData = get_request_data("/lbdj/app/order/AddOrderInstallCheckApiRequest", "����װǰ���")[
            0]  # ��ȡ����װǰ������������
        InstallCheckReq = json.loads(InstallCheckData["data"])
        InstallCheckReq["orderId"] = order_id

        InstallCheckRes = RequestApi.worker_requests(InstallCheckData["method"], InstallCheckData["uri"],
                                                     InstallCheckReq)  # ��������װǰ���ӿ�
        self.assertTrue(assert_key(InstallCheckData["assert"], InstallCheckRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")

        UploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "�����깤ͼ")[
            0]  # ��ѯ�����깤ͼһ�ڼ��ϴ��깤ͼ�������
        UploadDoneReq = json.loads(UploadDoneData["data"])
        UploadDoneReq["orderId"] = order_id
        UploadDoneReq["finishImages"][0]["goodName"] = my_order_info(order_id, order_sn)["goodsName"]
        UploadDoneRes = RequestApi.worker_requests(UploadDoneData["method"], UploadDoneData["uri"],
                                                   UploadDoneReq)  # ���������깤ͼһ�ڼ��ϴ��깤ͼ�ӿ�
        self.assertTrue(assert_key(UploadDoneData["assert"], UploadDoneRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")

        signUploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "����ǩ��ͼ")[
            0]  # ��ѯ����ǩ��ͼһ�ڼ��ϴ�ǩ��ͼ�������
        signUploadDoneReq = json.loads(signUploadDoneData["data"])
        signUploadDoneReq["orderId"] = order_id
        signUploadDoneRes = RequestApi.worker_requests(signUploadDoneData["method"], signUploadDoneData["uri"],
                                                       signUploadDoneReq)  # ��������ǩ��ͼһ�ڼ��ϴ�ǩ��ͼ�ӿ�
        self.assertTrue(assert_key(signUploadDoneData["assert"], signUploadDoneRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")
        respond = ServiceDone(order)
        self.assertEqual(respond["msg"], "�ɹ�", msg=respond)

    def test_dengju_anzhuang_yikoujia(self):
        """�ƾ��లװһ�ڼ�ʦ��"""
        order = get_order("138", "anz")  # ��ѯ�ƾ߰�װһ�ڼ�--����װƷ�ඩ��
        self.assertNotEqual(order["id"], "error", msg=order)
        reserve_HomeCheck(order)
        order_id = order["id"]
        order_sn = order["orderNum"]
        InstallCheckData = get_request_data("/lbdj/app/order/AddOrderInstallCheckApiRequest", "�ƾ�װǰ���")[
            0]  # ��ȡ�ƾ�װǰ������������
        InstallCheckReq = json.loads(InstallCheckData["data"])
        InstallCheckReq["orderId"] = order_id

        InstallCheckRes = RequestApi.worker_requests(InstallCheckData["method"], InstallCheckData["uri"],
                                                     InstallCheckReq)  # ����ƾ�װǰ���ӿ�
        self.assertTrue(assert_key(InstallCheckData["assert"], InstallCheckRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")

        UploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "�ƾ��깤ͼ")[
            0]  # ��ѯ�ƾ��깤ͼһ�ڼ��ϴ��깤ͼ�������
        UploadDoneReq = json.loads(UploadDoneData["data"])
        UploadDoneReq["orderId"] = order_id
        UploadDoneReq["finishImages"][0]["goodName"] = my_order_info(order_id, order_sn)["goodsName"]
        UploadDoneRes = RequestApi.worker_requests(UploadDoneData["method"], UploadDoneData["uri"],
                                                   UploadDoneReq)  # ����ƾ��깤ͼһ�ڼ��ϴ��깤ͼ�ӿ�
        self.assertTrue(assert_key(UploadDoneData["assert"], UploadDoneRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")

        signUploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "�ƾ�ǩ��ͼ")[
            0]  # ��ѯ�ƾ�ǩ��ͼһ�ڼ��ϴ�ǩ��ͼ�������
        signUploadDoneReq = json.loads(signUploadDoneData["data"])
        signUploadDoneReq["orderId"] = order_id
        signUploadDoneRes = RequestApi.worker_requests(signUploadDoneData["method"], signUploadDoneData["uri"],
                                                       signUploadDoneReq)  # ����ƾ�ǩ��ͼһ�ڼ��ϴ�ǩ��ͼ�ӿ�
        self.assertTrue(assert_key(signUploadDoneData["assert"], signUploadDoneRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")
        respond = ServiceDone(order)
        self.assertEqual(respond["msg"], "�ɹ�", msg=respond)

    def test_jingshuiqi_anzhuang_yikoujia(self):
        pass

    def test_jiadian_anzhuang_baojia(self):
        """�ҵ簲װʦ��"""
        order = get_order("148", "anz")  # ��ѯ�ҵ簲װһ�ڼ�--����װƷ�ඩ��
        self.assertNotEqual(order["id"], "error", msg=order)
        reserve_HomeCheck(order)
        order_id = order["id"]
        order_sn = order["orderNum"]
        UploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "�ҵ簲װһ�ڼ��깤ͼ")[
            0]  # ��ѯ�ҵ簲װһ�ڼ��깤ͼ�ϴ��깤ͼ�������

        UploadDoneReq = json.loads(UploadDoneData["data"])
        UploadDoneReq["orderId"] = order_id
        UploadDoneReq["finishImages"][0]["goodName"] = my_order_info(order_id, order_sn)["goodsName"]
        UploadDoneRes = RequestApi.worker_requests(UploadDoneData["method"], UploadDoneData["uri"],
                                                   UploadDoneReq)  # ����ҵ簲װһ�ڼ��깤ͼ�ϴ��깤ͼ�ӿ�
        self.assertTrue(assert_key(UploadDoneData["assert"], UploadDoneRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")

        signUploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "�ҵ簲װһ�ڼ�ǩ��ͼ")[
            0]  # ��ѯ�ҵ簲װһ�ڼ�ǩ��ͼ�ϴ�ǩ��ͼ�������
        signUploadDoneReq = json.loads(signUploadDoneData["data"])
        signUploadDoneReq["orderId"] = order_id
        signUploadDoneRes = RequestApi.worker_requests(signUploadDoneData["method"], signUploadDoneData["uri"],
                                                       signUploadDoneReq)  # ����ҵ簲װһ�ڼ�ǩ��ͼ�ϴ�ǩ��ͼ�ӿ�
        self.assertTrue(assert_key(signUploadDoneData["assert"], signUploadDoneRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")
        respond = ServiceDone(order)
        self.assertEqual(respond["msg"], "�ɹ�", msg=respond)

    def test_diban_anzhuang_yikoujia(self):
        """�ذ尲װʦ��"""
        order = get_order("141", "anz")  # ��ѯ�ذ��లװһ�ڼ�--����װƷ�ඩ��
        self.assertNotEqual(order["id"], "error", msg=order)
        reserve_HomeCheck(order)
        order_id = order["id"]
        order_sn = order["orderNum"]
        UploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "�ذ尲װһ�ڼ��깤ͼ")[
            0]  # ��ѯ�ذ尲װһ�ڼ��깤ͼ�ϴ��깤ͼ�������

        UploadDoneReq = json.loads(UploadDoneData["data"])
        UploadDoneReq["orderId"] = order_id
        UploadDoneReq["finishImages"][0]["goodName"] = my_order_info(order_id, order_sn)["goodsName"]
        UploadDoneRes = RequestApi.worker_requests(UploadDoneData["method"], UploadDoneData["uri"],
                                                   UploadDoneReq)  # ����ذ尲װһ�ڼ��깤ͼ�ϴ��깤ͼ�ӿ�
        self.assertTrue(assert_key(UploadDoneData["assert"], UploadDoneRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")

        signUploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "�ذ尲װһ�ڼ�ǩ��ͼ")[
            0]  # ��ѯ�ذ尲װһ�ڼ�ǩ��ͼ�ϴ�ǩ��ͼ�������
        signUploadDoneReq = json.loads(signUploadDoneData["data"])
        signUploadDoneReq["orderId"] = order_id
        signUploadDoneRes = RequestApi.worker_requests(signUploadDoneData["method"], signUploadDoneData["uri"],
                                                       signUploadDoneReq)  # ����ذ尲װһ�ڼ�ǩ��ͼ�ϴ�ǩ��ͼ�ӿ�
        self.assertTrue(assert_key(signUploadDoneData["assert"], signUploadDoneRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")
        respond = ServiceDone(order)
        self.assertEqual(respond["msg"], "�ɹ�", msg=respond)

    def test_menlei_anzhuang_yikoujia(self):
        """����һ�ڼ۰�װ"""
        order = get_order("143", "anz")  # ��ѯ���లװһ�ڼ�--����װƷ�ඩ��
        self.assertNotEqual(order["id"], "error", msg=order)
        reserve_HomeCheck(order)
        order_id = order["id"]
        order_sn = order["orderNum"]
        UploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "���లװһ�ڼ��깤ͼ")[
            0]  # ��ѯ���లװһ�ڼ��깤ͼ�ϴ��깤ͼ�������

        UploadDoneReq = json.loads(UploadDoneData["data"])
        UploadDoneReq["orderId"] = order_id
        UploadDoneReq["finishImages"][0]["goodName"] = my_order_info(order_id, order_sn)["goodsName"]
        UploadDoneRes = RequestApi.worker_requests(UploadDoneData["method"], UploadDoneData["uri"],
                                                   UploadDoneReq)  # �������లװһ�ڼ��깤ͼ�ϴ��깤ͼ�ӿ�
        self.assertTrue(assert_key(UploadDoneData["assert"], UploadDoneRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")

        signUploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "���లװһ�ڼ�ǩ��ͼ")[
            0]  # ��ѯ���లװһ�ڼ�ǩ��ͼ�ϴ�ǩ��ͼ�������
        signUploadDoneReq = json.loads(signUploadDoneData["data"])
        signUploadDoneReq["orderId"] = order_id
        signUploadDoneRes = RequestApi.worker_requests(signUploadDoneData["method"], signUploadDoneData["uri"],
                                                       signUploadDoneReq)  # �������లװһ�ڼ�ǩ��ͼ�ϴ�ǩ��ͼ�ӿ�
        self.assertTrue(assert_key(signUploadDoneData["assert"], signUploadDoneRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")
        respond = ServiceDone(order)
        self.assertEqual(respond["msg"], "�ɹ�", msg=respond)

    def test_qiangzhi_anzhuang_yikoujia(self):
        """ǽֽ��װһ�ڼ�ʦ��"""

        order = get_order("142", "anz")  # ��ѯǽֽ��װһ�ڼ�--����װƷ�ඩ��
        self.assertNotEqual(order["id"], "error", msg=order)
        reserve_HomeCheck(order)
        order_id = order["id"]
        order_sn = order["orderNum"]
        UploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "ǽֽ��װһ�ڼ��깤ͼ")[
            0]  # ��ѯǽֽ��װһ�ڼ��깤ͼ�ϴ��깤ͼ�������

        UploadDoneReq = json.loads(UploadDoneData["data"])
        UploadDoneReq["orderId"] = order_id
        UploadDoneReq["finishImages"][0]["goodName"] = my_order_info(order_id, order_sn)["goodsName"]
        UploadDoneRes = RequestApi.worker_requests(UploadDoneData["method"], UploadDoneData["uri"],
                                                   UploadDoneReq)  # ����ǽֽ��װһ�ڼ��깤ͼ�ϴ��깤ͼ�ӿ�
        self.assertTrue(assert_key(UploadDoneData["assert"], UploadDoneRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")

        signUploadDoneData = get_request_data("/lbdj/app/order/AppUploadDoneImageApiRequest", "ǽֽ��װһ�ڼ�ǩ��ͼ")[
            0]  # ��ѯǽֽ��װһ�ڼ�ǩ��ͼ��ǩ��ͼ�������
        signUploadDoneReq = json.loads(signUploadDoneData["data"])
        signUploadDoneReq["orderId"] = order_id
        signUploadDoneRes = RequestApi.worker_requests(signUploadDoneData["method"], signUploadDoneData["uri"],
                                                       signUploadDoneReq)  # ����ǽֽ��װһ�ڼ�ǩ��ͼ�ϴ�ǩ��ͼ�ӿ�
        self.assertTrue(assert_key(signUploadDoneData["assert"], signUploadDoneRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")
        respond = ServiceDone(order)
        self.assertEqual(respond["msg"], "�ɹ�", msg=respond)

    def test_worker_baojia(self):
        """ʦ����������"""

        ApiRequestData = json.loads(
            get_request_data("/lbdj/app/order/AppGrabOrderHallApiRequest", "�鿴ʦ�����۶���")[0]["data"])
        ApiRequestData["token"] = config.worker_environment["test"]["token"]
        wait_baojia = RequestApi.worker_requests("post", "/lbdj/app/order/AppGrabOrderHallApiRequest",
                                                 ApiRequestData).json()
        order_id = wait_baojia["data"][0]["id"]

        GrabOrderData = get_request_data("/lbdj/app/order/AppGrabOrderApiRequest", "ʦ������")[0]
        GrabOrderReq = json.loads(GrabOrderData["data"])
        GrabOrderReq["id"] = order_id
        GrabOrderRes = RequestApi.worker_requests(GrabOrderData["method"], GrabOrderData["uri"], GrabOrderReq)
        self.assertTrue(assert_key(GrabOrderData["assert"], GrabOrderRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")

    def test_get_zhipai_dingdan(self):
        """��ȡָ�ɶ���"""
        # wait_baojia = RequestApi.worker_requests("post", "/lbdj/app/order/AppGrabOrderHallApiRequest", data).json()
        # order_id = wait_baojia["data"][0]["id"]

        GrabOrderData = get_request_data("/lbdj/app/order/AppGrabOrderHallApiRequest", "��ȡָ�ɶ���")[0]
        GrabOrderReq = json.loads(GrabOrderData["data"])

        GrabOrderReq["token"] = config.worker_environment["test"]["token"]

        GrabOrderRes = RequestApi.worker_requests(GrabOrderData["method"], GrabOrderData["uri"],
                                                  GrabOrderReq)
        if GrabOrderRes.json()["data"] == []:
            self.assertEqual(GrabOrderRes.text, '{"isSuccess":true,"code":"200","msg":"�ɹ�","data":[]}',
                             msg=GrabOrderRes.text)
        else:
            self.assertTrue(assert_key(GrabOrderData["assert"], GrabOrderRes.text), msg="Ԥ�ڵ�key��ʵ�ʵ�key��һ��")


if __name__ == '__main__':
    # reserve_HomeCheck()
    # unittest.main()
    # print(get_order("140", "anz", 0))
    suit = unittest.TestSuite()
    suit.addTest(TestWorkerOrder("test_worker_baojia"))
    runner = unittest.TextTestRunner()
    runner.run(suit)
