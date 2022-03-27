from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains


class ChromeDriver(object):

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r"../config/chromedriver.exe")  # Chrome浏览器

    def press_qr_code(self):
        img_add = "qrcode-img"
        ActionChains(self.driver).click_and_hold(on_element=self.driver.find_element_by_class_name(img_add)).perform()

    def form_submit(self, url):
        self.open_web(url)
        name_xpath = '//*[@data-title="姓名"]'
        self.driver.find_element_by_xpath(name_xpath).send_keys("zhanghui")
        phone_xpath = '//*[@data-title="电话"]'
        self.driver.find_element_by_xpath(phone_xpath).send_keys("13666666666")
        self.driver.find_element_by_link_text("提交").click()

    def open_web(self, url):
        # 打开网页
        self.driver.get(url)  # 打开url网页 比如 driver.get("http://www.baidu.com")

    def order_submit(self, url):
        self.open_web(url)
        name_xpath = '//*[@data-title="姓名"]'
        self.driver.find_element_by_xpath(name_xpath).send_keys("zhanghui")
        phone_xpath = '//*[@data-title="手机号"]'
        self.driver.find_element_by_xpath(phone_xpath).send_keys("13666666666")
        sleep(2)
        self.driver.find_element_by_xpath('//*[@class="tip"]').click()


if __name__ == '__main__':
    chromedrive = ChromeDriver()
    # chromedrive.open_web("https://www.baidu.com/")
    chromedrive.open_web("https://lwn.asp.yiye-a.com/lwn/PcwDD5jx?_cl=b656")
