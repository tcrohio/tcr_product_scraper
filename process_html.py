from bs4 import BeautifulSoup
import glob
import subprocess
import pandas as pd

file_list = glob.glob('html_source/homedepot*.html')
print(file_list)

product_info_list = []

for file in file_list:
    print(file)
    tmp_dict = {}
    with open(file) as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    if soup.find_all('div', {'class': 'mediagallery__mainimage'}):
        product_titles = soup.find_all('div', {'class': 'mediagallery__mainimage'})

        for product_title in product_titles:
            print(product_title.img['src'])
            product_image = product_title.img['src']

    # quantity
    if soup.find_all('span', {'class': 'alert-inline__message'}):
        quantities = soup.find_all('span', {'class': 'alert-inline__message'})

        for quantity in quantities:
            print(quantity.text)
            quantity = quantity.text

    elif soup.find_all('div', {'class': 'fulfillment__unavailable'}):
        quantities = soup.find_all('div', {'class': 'fulfillment__unavailable'})
        print("unavailable")
        quantity = 'unavailable'
    elif soup.find_all('div', {'class': 'u__center pick-up-true'}):
        print('Ship To Store')
        quantity = 'Ship To Store'

    if soup.find_all('span', {'class': 'product-title'}):
        product_titles = soup.find_all('span', {'class': 'product-title'})
        for product_title in product_titles:
            print(product_title.text)
            title = product_title.text

    if soup.find_all('div', {'class': 'price-format__large price-format__main-price'}):
        for price in soup.find_all('div', {'class': 'price-format__large price-format__main-price'}):
            product_price = price.text[:-2] + price.text[-2:]
            if '\xa2' in product_price:
                product_price = product_price.replace('\xa2', '')
                product_price = "$0" + product_price
            product_price = product_price[:-2] + '.' + product_price[-2:]
            print(product_price)

    else:
        print("$0.00")
        product_price = 0.0
            #print(price[1] + '.' + price[2])

    tmp_dict = {'product_title': title,
                'quantity': quantity,
                'price': product_price,
                'image': product_image,
                'file': file}
    product_info_list.append(tmp_dict)

#print(product_info_list)
df = pd.DataFrame(product_info_list)
df.to_csv("test.csv", index=False)