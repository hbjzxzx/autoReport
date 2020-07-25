from selenium import webdriver as webd
from selenium.webdriver.chrome.options import Options
import os
import time


class dummyReport(object):
    def __init__(self, account, password, brower, pic_root, mock_local=None):
        self.act = account
        self.psd = password
        self.br_ins = brower
        self.mock_local = mock_local
        if not os.path.exists(pic_root):
            os.makedirs(pic_root, exist_ok=True)
        self.root = pic_root

    
    def report(self, debug=False):
        url = 'https://m.nuaa.edu.cn/ncov/wap/default/index'
        if self.mock_local:
            self.br_ins.execute_cdp_cmd("Emulation.setGeolocationOverride", self.get_local_param())
            #self.br_ins.refresh()
        self.br_ins.get(url)

        actui = self.br_ins.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/input')
        psdui = self.br_ins.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/input')
    
        actui.send_keys(self.act)
        psdui.send_keys(self.psd)

        loginui = self.br_ins.find_element_by_xpath('//*[@id="app"]/div[3]')
        loginui.click()

        localui = self.br_ins.find_element_by_xpath('/html/body/div[1]/div/div/section/div[4]/ul/li[7]/div/input')
        localui.click()
        self.save_image('information')

        if debug:
            return
        assertui = self.br_ins.find_element_by_xpath('/html/body/div[1]/div/div/section/div[5]/div/a')
        assertui.click()

        assertui2 = self.br_ins.find_element_by_xpath('//*[@id="wapcf"]/div/div[2]/div[2]')
        assertui2.click()

        suc_assert_ui = self.br_ins.find_element_by_xpath('//*[@id="wapat"]/div/div[2]/div')
        self.save_image('report_result')
        suc_assert_ui.click()


    def save_image(self, prefix=''):
        width = self.br_ins.execute_script("return document.documentElement.scrollWidth")
        height = self.br_ins.execute_script("return document.documentElement.scrollHeight")
        #print(width,height)

        self.br_ins.set_window_size(width, height)

        self.br_ins.save_screenshot(os.path.join(self.root, self.get_pic_name(prefix)))
    

    def get_pic_name(self, ac, prefix=''):
        nowtime = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
        return f'{prefix}-{nowtime}-{self.act}.jpeg'

    def get_local_param(self):
        if self.mock_local == 'nanjing':
            params = {
                "latitude": 31.940413,
                "longitude": 118.794794,
                "accuracy": 100}
            return params
        elif self.mock_local == 'shanghai':
            params = {
                "latitude": 31.166253,
                "longitude": 121.390819,
                "accuracy": 100
            }
            return params
        else:
            raise Exception(f'unkown location {self.mock_local}')
def run():
    chrome_options = Options()
    chrome_options.add_argument('headless')
    chromedriver = '/Users/admin/chromedriver'
    driver = webd.Chrome(chromedriver,chrome_options=chrome_options)
    driver.implicitly_wait(20)
    my_report = dummyReport('SX1816001', '100057', driver, 'save_imgs', mock_local='nanjing')
    my_report.report(debug=True)


if __name__ == '__main__':
    run()

