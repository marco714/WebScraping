from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup 

my_url = 'https://www.newegg.com/global/ph-en/p/pl?d=graphic+card'

#Opening up connection, grabbing the page
uClient = uReq(my_url)
page_html = uClient.read()

page_soup = soup(page_html, "html.parser")


# Grab each product
containers = page_soup.findAll("div", {"class":"item-container"})

filename = "product.csv"
f = open(filename, "w")

headers = "brand, product_name, shipping\n"

f.write(headers)
for container in containers:

    brand = container.div.div.a.img["title"]
    title_container = container.find("a", {"class", "item-title"})
    product_name = title_container.text 

    shipping_container = container.find("li", {"class", "price-ship"})
    shipping = shipping_container.text.strip()

    print("Brand: " + brand)
    print("Product Name:" + product_name)
    print("Shipping: " + shipping)

    f.write(brand + "," + product_name.replace(",", "|") + "," + shipping + "\n")
uClient.close()






#containers = page_soup.findAll("div", {"class":"item-container"})
#container = containers[0]
#div_with_info = container.find("div", "item-info")
#print(div_with_info)
#print(container.a)
#print(container.div)
#print(container.prettify())
