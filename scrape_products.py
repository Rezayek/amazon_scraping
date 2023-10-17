import requests
from bs4 import BeautifulSoup
import csv
# Product Url | Name | Price | Rating | Number of reviews

def scrape_products(url, headers):
    
    page = requests.get(url, headers=headers)
    
    
    soup = BeautifulSoup(page.content, 'html.parser')


    products_url = []
    products_name = []
    products_rating = []
    products_reviews_nb = []
    products_price = []

    for product_element in soup.find_all('div', class_='sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16'):
        
        h2_element = product_element.find('h2', class_='a-size-mini a-spacing-none a-color-base s-line-clamp-2')
        
        # Find product URLs
        url_element = h2_element.find('a', class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal", href=True)
        if url_element:
            product_url = "https://www.amazon.in" + url_element['href']
        else:
            product_url = "URL not found"
            
        # Find product names
        name_element = h2_element.find('span', class_="a-size-medium a-color-base a-text-normal")
        if name_element:
            product_name = name_element.get_text()
        else:
            product_name = "Name not found"
            
        
        div_rating = product_element.find('div', class_='a-section a-spacing-none a-spacing-top-micro')
        span_rating = div_rating.find('span', class_="a-declarative")
        #Find stars rating
        star_rating = span_rating.find('span', class_="a-icon-alt")
        if star_rating:
            product_star_rating = star_rating.get_text()
        else:
            product_star_rating = "Rating not found"
            
        #Find reviews
        reiewers_rating = div_rating.find('a', class_="a-link-normal s-underline-text s-underline-link-text s-link-style")
        reiewers_rating_element = reiewers_rating.find('span', class_="a-size-base s-underline-text")
        if reiewers_rating_element  :
            product_reiewers_rating  = reiewers_rating_element .get_text()
        else:
            product_reiewers_rating  = "reviews not found"
            
            
        # Find product prices
        price_span = product_element.find_all('span', class_='a-price')
        
        if (len(price_span) == 2 and  product_element.find_all('span', class_='a-price-range')):
            a_offscreen_span = price_span[1].find('span', class_='a-offscreen')
            product_price = a_offscreen_span.get_text()
        elif(len(price_span) > 1):
            a_offscreen_span = price_span[0].find('span', class_='a-offscreen')
            product_price = a_offscreen_span.get_text()
        else:
            product_price = "Price not found"
            
        products_url.append(product_url)
        products_name.append(product_name)
        products_rating.append(product_star_rating)
        products_reviews_nb.append(product_reiewers_rating)
        products_price.append(product_price)
            


    # Save the scraped data to a CSV file in append mode
    with open('amazon_products.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Check if the file is empty (no header row), and if so, write the header
        if csvfile.tell() == 0:
            writer.writerow(['Product Name', 'Product Rating', 'Number of Reviews', 'Product Price', 'Product URL'])

        for i in range(len(products_url)):
            writer.writerow([products_name[i], products_rating[i], products_reviews_nb[i], products_price[i], products_url[i]])

    print("Data has been saved to amazon_products.csv")  