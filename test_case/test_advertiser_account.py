import json

from test_case import *

request = RequestApi()


class TestUserAuthorization(unittest.TestCase):

    def tearDown(self):  # 每个用例运行之后运行的
        pass

    @classmethod
    def tearDownClass(cls):  # 在所有用例都执行完之后运行的
        # warnings.simplefilter('ignore', ResourceWarning)
        pass

    def test_ocean_engine(self):  # 函数名要以test开头，否则不会被执行
        import requests
        ocean_engine_url = "https://open.oceanengine.com/openapi/api/advertiser/oauth2/authorize/"

        header = {
            'host': 'open.oceanengine.com',
            'user-agent': 'mozilla/5.0 (windowS NT 10.0; win64; x64) appLewEbkit/537.36 (KHTML, likE gecko) chrome/93.0.4577.82 safari/537.36',
            'content-type': 'application/json;charseT=UTF-8',
            'accept': 'application/json, text/plain, */*',
            'origin': 'https://open.oceanengine.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://open.oceanengine.com/audit/oauth.html?app_id=1709127165168719&scope=%5B10000000%2C11000000%2C130%2C3%2C4%2C5%2C8%2C9%2C2%2C14%2C112%2C110%2C120%2C122%2C12000000%5d&material_auth=1&redirect_uri=https%3A%2F%2fagent-sz-dev7.yiye.ai%2fapi%2Fv1%2fmarketing%2fadvertiser-accounts%2faction%2foauth%2ffrom%2focean-engine&rid=bedbr0ez7y&state=dev7:b4dc5b1B:PMP_4',
            'cookie': 'ttcid=3f167bd19ba94e448bdf75c6ad0d9ed130; passport_csrf_token_default=b8cb9c2ebd8870bff9baa5c348bcc74f; passport_csrf_token=b8cb9c2ebd8870bff9baa5c348bcc74f; n_mh=9-mIeuD4wZnlYrrOvfzG3MuT6aQmCUtmr8FxV8Kl8xY; gr_user_id=c9204415-1c0d-4381-ae4f-1e7d10c08216; aefa4e5d2593305f_gr_last_sent_cs1=1642912301664260; grwng_uid=27428edc-5311-48a2-bc03-7ce52b7dbd77; csrf_session_id=fcff12a2f3df4763b0e69d7454a0528d; x-jupiter-uuid=16323789518487540; s_v_web_id=verify_9debeb9d97588b82864c35c61fb28e6b; MONITOR_DEVICE_ID=706278ad-8a65-447f-b1bd-612a198370d9; aefa4e5d2593305f_gr_session_id=c25136d2-b00e-4aac-ba4f-000836c2cd04; aefa4e5d2593305f_gr_last_sent_sid_with_cs1=c25136d2-b00e-4aac-ba4f-000836c2cd04; aefa4e5d2593305f_gr_session_id_c25136d2-b00e-4aac-ba4f-000836c2cd04=true; aefa4e5d2593305f_gr_cs1=1642912301664260; MONITOR_WEB_ID=cadf9e01-f57b-4c03-9d20-f27496d3d340; tt_scid=VMTF8HZBzik0LFequX8WKjmj-g1gUTi52eu36UCLiT0LQcikU6wZcZN4CT2bE3sq9d42; sid_guard=0c7f6b4897f488fd7442795ef6464283%7C1632473231%7C5183999%7CTue%2C+23-Nov-2021+08%3A47%3A10+GMT; uid_tt=f18a7c84fb1bf511f5d7f507434efbbe; uid_tt_ss=f18a7c84fb1bf511f5d7f507434efbbe; sid_tt=0c7f6b4897f488fd7442795ef6464283; sessionid=0c7f6b4897f488fd7442795ef6464283; sessionid_ss=0c7f6b4897f488fd7442795ef6464283; sid_ucp_v1=1.0.0-KGMyYmQ5ZTMyMzk2NDNmODk4NTMzZjZiNTgzZjg2NmY5NGQ4M2UxNzYKFAjnueDT0YzEBBCPobaKBhjQCjgBGgJobCIgMGM3ZjZiNDg5N2Y0ODhmZDc0NDI3OTVlZjY0NjQyODM; ssid_ucp_v1=1.0.0-KGMyYmQ5ZTMyMzk2NDNmODk4NTMzZjZiNTgzZjg2NmY5NGQ4M2UxNzYKFAjnueDT0YzEBBCPobaKBhjQCjgBGgJobCIgMGM3ZjZiNDg5N2Y0ODhmZDc0NDI3OTVlZjY0NjQyODM',
        }

        data = {"app_id": 1709127165168719, "state": "dev7:b4dc5b1b:PMP_4",
                "scope": [10000000, 11000000, 130, 3, 4, 5, 8, 9, 2, 14, 112, 110, 120, 122, 12000000],
                "redirect_uri": "https://agent-sz-dev7.yiye.ai/api/v1/marketing/advertiser-accounts/action/oauth/from/ocean-engine",
                "advertiser_ids": [1694462909668360], "material_auth": 0}
        ocean_engine_respond = requests.post(ocean_engine_url, headers=header, json=data).text  # verify=False
        authorization_url = json.loads(ocean_engine_respond)["data"]["next_url"]
        data = {"uri": authorization_url, "method": "get", }
        request.request(data)


if __name__ == '__main__':
    unittest.main()
