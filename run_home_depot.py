import product_scraper as ps
import product_scraper.menards.menards_scraper as menards
import product_scraper.home_depot.home_depot_scraper as hd

if __name__ == '__main__':

    hd_obj = hd.HomeDepotScraper()
    hd_obj.run_scrape()
