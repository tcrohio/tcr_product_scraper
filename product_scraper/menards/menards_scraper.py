from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
import configs.utils as utils
import product_scraper.common as common
import csv
import datetime

class MenardsScraper():

    def __init__(self):

        self.get_stores()
        self.get_products()
        self.init_driver()

    def init_driver(self):

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=utils.driver_location)
        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

    def get_stores(self):

        self.store_list = []
        with open(utils.menards_stores, newline='') as csvfile:
            storereader = csv.reader(csvfile, delimiter=',')
            header = next(storereader, None)
            for row in storereader:
                tmp_list = [{header[0]:row[0],header[1]:row[1],header[2]:row[2]}]
                self.store_list.append(tmp_list)

    def get_products(self):

        self.product_list = []
        with open(utils.menards_products, newline='') as csvfile:
            productreader = csv.reader(csvfile, delimiter=',')
            header = next(productreader, None)
            for row in productreader:
                tmp_list = [{header[0]:row[0],header[1]:row[1]}]
                self.product_list.append(tmp_list)

    def set_store(self, store_id):

        self.driver.get('https://www.menards.com/store-details/store.html?store=' + store_id)
        common.short_sleep()
        store_button = self.driver.find_element(By.ID, "make-my-store")
        store_button.click()
        common.short_sleep()

    def run_scrape(self):

        for store in self.store_list:

            common.short_sleep()
            self.set_store(store[0]['store_id'])
            common.long_sleep()

            for product in self.product_list:
                self.driver.get(product[0]['url'])
                common.short_sleep()
                print(self.driver.title)

                file_name = "menards_" + store[0]['store_id']
                file_name = file_name + "_" + store[0]['zip_code']
                file_name = file_name + "_" + product[0]['item']
                file_name = file_name + "_" + datetime.datetime.today().strftime('%Y-%m-%d')
                file_name = file_name + ".html"
                print(file_name)

                try:
                    with open(utils.html_source_path + file_name, "w") as f:
                        f.write(self.driver.page_source)
                except Exception as e:
                    common.log_action({"status": "failed",
                                       "filename": file_name,
                                       "title": self.driver.title})
                else:
                    common.log_action({"status": "success",
                                       "filename": file_name,
                                       "title": self.driver.title})

        self.driver.close()

