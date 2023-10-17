from scrape_product import scrape_product
from scrape_products import scrape_products


def main_scrap(use_proxy):
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
    url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
    totale_pages = 200
    for i in range(1,(totale_pages + 1)):
        scrape_products(url+str(i), headers)

    scrape_product(headers, use_proxy)
    

if __name__ == "__main__":
    main_scrap(False)