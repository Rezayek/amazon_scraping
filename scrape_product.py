import time
import requests
from bs4 import BeautifulSoup
import csv
import re

# Product: Description | ASIN | Product Description | Manufacture

def scrape_product(headers, use_proxy):  
    
    url_column = 'Product URL'
    
    proxy_list = [
        '198.27.115.215:80',
        '64.201.163.133:80',
        '168.235.81.149:8080',
        '146.190.79.143:8888',
        '32.223.6.94:80',
        '37.19.220.129:8443',
        '129.213.153.223:80',
        '37.19.220.179:8443',
        '162.223.94.163:80',
        '162.223.94.164:80',
        '35.236.207.242:33333',
        '138.199.48.1:8443',
        '138.199.48.4:8443',
        '68.188.59.198:80',
        '50.122.86.118:80',
        '24.158.29.166:80',
        '172.108.208.74:80',
        '50.171.32.226:80',
        '50.171.32.228:80',
        '50.171.32.227:80',
        '50.171.32.224:80',
        '50.171.32.222:80',
        '50.171.32.230:80',
        '50.171.32.229:80',
        '50.171.32.231:80',
        '50.168.163.180:80',
        '50.168.163.177:80',
        '50.168.163.181:80',
        '50.168.163.183:80',
        '50.168.163.182:80',
        '50.171.152.30:80',
        '50.168.210.232:80',
        '50.168.163.166:80',
        '50.171.32.225:80',
        '50.168.210.226:80'
    ]

    
    data, csv_reader = get_products()

    products_description_list = []
    product_details_list = []
    

    for i,row in enumerate(data):
        
        try:
            if use_proxy:
            # Cycle through the proxies
                current_proxy = proxy_list[i % len(proxy_list)]
                
                proxies = {
                    'http': 'http://' + current_proxy,
                    'https': 'http://' + current_proxy
                }

                product_page = requests.get(row[url_column], headers=headers, proxies= proxies)
            else:
                product_page = requests.get(row[url_column], headers=headers)
            
            products_description, product_details =  fetch_data(product_page.content)
            update_rows(row, products_description)
            update_rows(row, product_details)
            
            
            if len(products_description)==0:
                products_description_list.append({})
            else : 
                products_description_list.append(products_description)
                
            if len(product_details)==0:
                product_details_list.append({})
            else : 
                product_details_list.append(product_details)
            
        except Exception as e:
            print(f"Error while processing Product {i}: {e}")
            products_description_list.append({})
            product_details_list.append({})
            
        time.sleep(2)
            
        
    combined_keys = list(next((d for d in products_description_list if d), {}).keys()) + list(next((d for d in product_details_list if d), {}).keys())

    if update_products(csv_reader, data, combined_keys):
        print("+++++++++++ Update successful +++++++++++")
    else:
        print("+++++++++++ Update failed +++++++++++")
              
def get_products():
    csv_file = 'amazon_products.csv'


    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        data = [row for row in csv_reader]

            
    return data, csv_reader 

def update_products(csv_reader, data, new_keys):
    print(data)
    try:
        
        output_csv_file = 'updated_amazon_products.csv'
        # Write the updated data to a new CSV file
        with open(output_csv_file, 'w', newline='', encoding='utf-8') as file:
            fieldnames = csv_reader.fieldnames + new_keys  # Add more field names as needed
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            
        return True
            
    except Exception:
        return False

def update_rows(row, new_data):
    for key in new_data.keys():
        row[key] = new_data[key]  

def fetch_data(product_page):
    
    soup = BeautifulSoup(product_page, 'html.parser')


    products_description = []

    

    #Description
    data_element = soup.find_all('div', id ='featurebullets_feature_div')
    
    
        
    description_element = data_element[0].find('div', id = "feature-bullets")
    description_list_element = description_element.find_all('span', class_="a-list-item")
    
    
    for detail in description_list_element:
        products_description.append(detail.get_text())
        
    
    #Details
        
    # Find the main product details container
    product_details_container = soup.find('div', id='detailBulletsReverseInterleaveContainer_feature_v2')
    product_details_list = product_details_container.find('div', id='detailBullets_feature_div') 
    # Create a dictionary to store the product details
    product_details = {}

    # Find all list items within the container
    detail_items = product_details_list.find_all('li')

    # Loop through each detail item
    for item in detail_items:
        # Extract the detail name (text in the first <span> element)
        detail_name = item.find('span', class_='a-text-bold').text

        # Extract the detail value (text in the second <span> element)
        detail_value = item.find_all('span')[2].text

        # Add the detail to the product_details dictionary
        product_details[detail_name] = detail_value
    
    # print(clean_description(products_description))
    # print(clean_details(product_details))
    
    
    return clean_description(products_description), clean_details(product_details)

def clean_details(product_details):
    
    # Clean the dictionary
    cleaned_dict = {}
    for key, value in product_details.items():
        # Remove unwanted characters using replace
        cleaned_key = key.replace("\n                      \u200f\n                      :\n                      \u200e\n", "")
        cleaned_value = value.replace("\n                      \u200f\n                      :\n                      \u200e\n", "")
        cleaned_dict[cleaned_key] = cleaned_value
    4

    # Convert the cleaned dictionary to JSON with indentation for readability
    return {key.strip(): value for key, value in cleaned_dict.items()}

def clean_description(products_description):
    cleaned_list =  [re.sub(r'\s+', ' ', item.replace('<br>', '')).strip() for item in products_description]

    # Separator used to split the key-value pairs
    separator = ':'

    # Convert the cleaned list into a dictionary
    result_dict = {}
    for item in cleaned_list:
        parts = item.split(separator, 1)
        if len(parts) == 2:
            key, value = parts[0].strip(), parts[1].strip()
            result_dict[key] = value
     
    return  result_dict

