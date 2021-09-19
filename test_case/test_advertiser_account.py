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
            'cookie': 'MONITOR_WEB_ID=421cc24d-5258-4ca3-83b1-271c22a0dc19; x-jupiter-uuid=1632038040589467; csrf_session_id=a968894883fe4768a02b48f52adbbc54; tt_sciD=EGlSKUZFC12.620F08iD9Kw3STG0p-NZTFWzLi.rucapY8Cc3j5DQZFRatsye3jD8887; passport_csrf_token_default=772d90974deb13c319006cc2fc1a6059; passport_csrf_token=772d90974deb13c319006cc2fc1a6059; s_v_web_id=verify_8cca777c6383bec8c9c2ac7fc8678587; MONITOR_DEVICE_ID=2f0e484e-949d-4f6a-a9ce-1d10d8f5d096; sid_guard=c2ab364f697450013e4274634022f7a5%7C1632038063%7C5184000%7cthu%2C+18-nov-2021+07%3A54%3A23+GMT; uid_tt=0e8c12376f91d83face716ac64f58dca; uid_tt_ss=0e8c12376f91d83face716ac64f58dca; sid_tt=c2ab364f697450013e4274634022f7a5; sessionid=c2ab364f697450013e4274634022f7a5; sessionid_ss=c2ab364f697450013e4274634022f7a5; sid_ucp_v1=1.0.0-KdQXZdVjNjQ5OTI3YzI2MdYzmzK1YWU0NtYYOwZKntHIytHIZTU0NZYKfajnUEDT0YZEBbCV2ZUkbHJqcJGbGgJsZiIgYzJhYjM2NGY2oTC0NtAWMtNLNDI3NdYZNdAyMmY3YTU; ssid_ucp_v1=1.0.0-KdQXZdVjNjQ5OTI3YzI2MdYzmzK1YWU0NtYYOwZKntHIytHIZTU0NZYKfajnUEDT0YZEBbCV2ZUkbHJqcJGbGgJsZiIgYzJhYjM2NGY2oTC0NtAWMtNLNDI3NdYZNdAyMmY3YTU; n_mh=9-miEud4wzNlyRrovFzG3Mut6aQMcutmR8FxV8Kl8xY',

        }

        data = {"app_id": 1709127165168719, "state": "dev7:b4dc5b1b:PMP_4",
                "scope": [10000000, 11000000, 130, 3, 4, 5, 8, 9, 2, 14, 112, 110, 120, 122, 12000000],
                "redirect_uri": "https://agent-sz-dev7.yiye.ai/api/v1/marketing/advertiser-accounts/action/oauth/from/ocean-engine",
                "advertiser_ids": [1694462909668360], "material_auth": 0}
        ocean_engine_respond = requests.post(ocean_engine_url, headers=header, json=data).text  # verify=False
        authorization_url = json.loads(ocean_engine_respond)["data"]["next_url"]
        data = {"uri":authorization_url,"method":"get", }
        request.request(data)



if __name__ == '__main__':
    unittest.main()
