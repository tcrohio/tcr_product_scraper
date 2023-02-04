from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
import configs.utils as utils
import product_scraper.common as common
import csv
import datetime

class HomeDepotScraper():

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
        with open(utils.home_depot_stores, newline='') as csvfile:
            storereader = csv.reader(csvfile, delimiter=',')
            header = next(storereader, None)
            for row in storereader:
                tmp_list = [{header[0]:row[0],header[1]:row[1],header[2]:row[2]}]
                self.store_list.append(tmp_list)

    def get_products(self):

        self.product_list = []
        with open(utils.home_depot_products, newline='') as csvfile:
            productreader = csv.reader(csvfile, delimiter=',')
            header = next(productreader, None)
            for row in productreader:
                tmp_list = [{header[0]:row[0],header[1]:row[1]}]
                self.product_list.append(tmp_list)

    def set_store(self, store_id):

        try:
            self.driver.get(store_id)
        except Exception as e:
            print("Error setting store")
            print(e)
            return False

        common.short_sleep()

        if self.driver.find_element(By.XPATH, "//span[text()='Shop This Store']"):
            try:
                self.driver.find_element(By.XPATH, "//span[text()='Shop This Store']").click()
            except Exception as e:
                print("Error selecting store")
                print(e)
                return False
            else:
                return True
                common.short_sleep()

    def save_scrape(self, store, product):

        file_name = "homedepot_" + store[0]['store_id'].rsplit("/", 1)[1]
        file_name = file_name + "_" + store[0]['zip_code']
        file_name = file_name + "_" + product[0]['item']
        file_name = file_name + "_" + datetime.datetime.today().strftime('%Y-%m-%d')
        file_name = file_name + ".html"

        try:
            with open(utils.html_source_path + file_name, "w") as f:
                f.write(self.driver.page_source)
        except Exception as e:
            print(e)
            common.log_action({"status": "failed",
                               "filename": file_name})
        else:
            common.log_action({"status": "success",
                               "filename": file_name,
                               "title": self.driver.title})
            f.close()

    def run_scrape(self):

        for store in self.store_list:
            common.short_sleep()
            if self.set_store(store[0]['store_id']):
                common.long_sleep()

                maxtry = 3
                for product in self.product_list:
                    ntry = 0
                    while ntry < maxtry:
                        try:
                            self.driver.get(product[0]['url'])
                        except Exception as e:
                            print("Failed - Try again")
                            print(e)
                            ntry = ntry + 1
                            common.short_sleep()
                        else:
                            common.short_sleep()
                            self.save_scrape(store, product)
                            ntry = maxtry

        self.driver.close()

