from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv 
import os




def web_scrape(default_URL):
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Set up Chrome WebDriver
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    

    all_car_data = []
    current_page_number = 1
    
    while True:
        url = f"{default_URL}?pageNo={current_page_number}"
        driver.get(url)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.v-pagination'))
            )
            time.sleep(5)  # Ensure all JavaScript has loaded
        except Exception as e:
            print("Error: ", e)
            driver.quit()
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "lxml")


        car_list = soup.find_all('div', attrs={'class':'mod-b-card__footer'})

        car_data_list = []
        for car in car_list:
            car_data = {}
            
            car_name_element = car.find('a', class_="mod-b-card__title")
            car_name_parts = [p.text.strip() for p in car_name_element.find_all("p")]
            car_name = " ".join(car_name_parts)
            car_data["car_name"]  = car_name.replace("\n", "").strip()

            car_info_element = car.find("div", class_="mod-b-card__car-other")
            car_info = car_info_element.find_all("span", recursive=False)
            car_data["car_mileage"] = car_info[0].text.strip()
            car_data["car_transmission"] = car_info[1].text.strip()
            car_data["car_location"] = car_info[2].text.strip()

            car_price_element = car.find('div', class_="mod-card__price__total")
            car_price = car_price_element.find("strong").text.strip()
            car_data["car_price"] = f'RM {car_price}'

            car_installment_element = car.find('div', class_="mod-tooltipMonthPay")
            car_installment = car_installment_element.find("span").text.strip()
            car_data["car_installment"] = car_installment
            
            car_data_list.append(car_data)
        
        all_car_data.extend(car_data_list)
        last_page_element = soup.find_all('button', class_='v-pagination__item')

        page_numbers = [int(item.text) for item in last_page_element if item.text.isdigit()]
        
        last_page_number = max(page_numbers)
        if current_page_number == last_page_number:
            break
        else:
            current_page_number += 1 
        
    return all_car_data


target_URL = "https://www.carsome.my/buy-car/perodua/myvi"
car_listing = web_scrape(target_URL)
print (car_listing)
# Output data to CSV

# get the current working directory
cwd = os.getcwd()
file_path = os.path.join(cwd, 'car_data.csv')

with open(file_path, mode='w+') as file:
    fieldnames = ['car_name', 'car_mileage', 'car_transmission', 'car_location', 'car_price', 'car_installment']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for car_data in car_listing:
        writer.writerow(car_data)

print("Data has been written to car_data.csv")