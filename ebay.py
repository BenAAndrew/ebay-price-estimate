from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime

URL = "https://www.ebay.co.uk/sch/i.html?LH_Sold=1&_ipg=240&_nkw={search_term}&LH_ItemCondition={condition}"


def build_url(search_term, condition):
    condition_code = "1000" if condition == "new" else "3000"
    search_term = search_term.replace(" ", "+")
    return URL.format(search_term=search_term, condition=condition_code)


def get_item_price(item):
    try:
        price = item.find_element(By.CLASS_NAME, "s-item__price")
        # Remove prices in italic (from abroad)
        if "ITALIC" not in price.get_attribute("innerHTML"):
            return float(price.text.replace("£", "").replace(",", ""))
    except ValueError:
        return None


def get_delivery_price(item):
    try:
        shipping_text = item.find_element(By.CLASS_NAME, "s-item__shipping").text
        return 0 if shipping_text.startswith("Free") else float(shipping_text.split(" ")[1].replace("£", ""))
    except NoSuchElementException:
        return None


def get_sale_date(item):
    date_text = item.find_element(By.CSS_SELECTOR, ".s-item__title--tagblock .POSITIVE").text
    day, month, year = date_text.split(" ")[1:4]
    return datetime.strptime(f'{day} {month} {year}', "%d %b %Y").date()


def get_items(url, include_delivery_price=True):
    driver = webdriver.Chrome()
    driver.get(url)
    page_items = driver.find_elements(By.CLASS_NAME, "s-item")[1:]

    items = []
    for item in page_items:
        item_price = get_item_price(item)
        date = get_sale_date(item)
        if item_price is not None:
            if include_delivery_price:
                delivery_price = get_delivery_price(item)
                if delivery_price is not None:
                    items.append({"price": item_price + delivery_price, "date": date})
            else:
                items.append({"price": item_price, "date": date})

    driver.close()
    return items
