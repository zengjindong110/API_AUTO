from playwright.sync_api import Playwright, sync_playwright


def browse_page(playwright: Playwright, landing_page_ur) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    # Go to http://aaa.dbq.yiye.ai/dbq/eKir4cvy?_cl=55d1
    page.goto(landing_page_ur)
    # ---------------------
    page.wait_for_timeout(4000)
    context.close()
    browser.close()


def open_url(landing_page_ur):
    with sync_playwright() as playwright:
        browse_page(playwright, landing_page_ur)


def table(playwright: Playwright, table_url) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://dbq.asptest.yiye-a.com/dbq/Aa2lwmNB?_cl=8fbf
    page.goto(table_url)
    page.wait_for_timeout(1500)
    # Click input[name="name"]
    page.locator("input[name=\"name\"]").click()
    page.wait_for_timeout(1500)
    page.locator("input[name=\"name\"]").fill("表单提交测试")
    page.wait_for_timeout(1500)
    # Click text=提交
    page.locator("text=提交").click()

    page.wait_for_timeout(1500)

    # ---------------------
    context.close()
    browser.close()


def table_submit(table_url):
    with sync_playwright() as playwright:
        table(playwright, table_url)


def order(playwright: Playwright, order_url) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    # Go to http://bbb.dbq.yiye.ai/dbq/L4mTNVRP?_cl=253e
    page.goto(order_url)
    # Click input[name="name"]
    page.wait_for_timeout(1500)
    page.locator("input[name=\"name\"]").click()
    # Click text=立即购买
    page.wait_for_timeout(1500)

    page.locator("input[name=\"name\"]").fill("订单提交测试")
    # page.locator("text=立即购买").click()
    # 0× click
    page.wait_for_timeout(1500)
    page.locator("text=立即购买").click()
    # ---------------------
    page.wait_for_timeout(1500)

    context.close()
    browser.close()


def order_submit(order_url):
    with sync_playwright() as playwright:
        order(playwright, order_url)


if __name__ == '__main__':
    table_submit("https://dbq.asptest.yiye-a.com/dbq/Aa2lwmNB?_cl=8fbf")
