import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import requests
import os

# Setup for the webdriver 
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.amazon.sa/-/en")
driver.maximize_window()

# Setup for the csv file and product images folder
csv_file_name = "product_details.csv"
img_file_name = "product images"
if not os.path.exists(img_file_name):
    os.makedirs(img_file_name)

input_element = driver.find_element(By.ID, "twotabsearchtextbox")
input_element.clear()
input_element.send_keys("shoes" + Keys.ENTER) # switch "shoes" with whatever products you want to collect info on

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "s-result-sort-select"))
)
sort_dropdown = driver.find_element(By.ID, "s-result-sort-select")
driver.execute_script("arguments[0].scrollIntoView();", sort_dropdown)
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(sort_dropdown)
)
ActionChains(driver).move_to_element(sort_dropdown).click().perform()
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//option[@value='price-desc-rank']"))
)
high_to_low_option = driver.find_element(By.XPATH, "//option[@value='price-desc-rank']")
high_to_low_option.click()
time.sleep(3)

product_index = 0

shoes = {
    "names" : [],
    "prices" : [],
    "care instructions": [],
    "sole materials":[],
    "outer materials":[],
    "closure types":[],
    "dates first available": [],
    "asin": [],
    "department":[],
    "ships from":[],
    "sold by":[]
}


products = WebDriverWait(driver,10).until(
    EC.visibility_of_all_elements_located((By.XPATH, "//a[@class='a-link-normal s-no-hover s-underline-text s-underline-link-text s-link-style a-text-normal']")))

for product in products:
    if product_index < 3:
        product.click()
        # Product Name
        product_name = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//h1[@class='a-size-large a-spacing-none a-color-secondary']/span")))
        shoes["names"].append(product_name.text)
        
        # Product Price
        price_whole = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[@class='a-price-whole']"))
        )
        price_fraction = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[@class='a-price-fraction']"))
        )
        price = 'SAR' + price_whole.text + '.' + price_fraction.text
        shoes['prices'].append(price)
        
        # Product Details 1
        product_details1 = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//span[@class='a-color-base']")))
        values = [span.text for index, span in enumerate(product_details1) if index % 2 != 0]
        shoes["care instructions"].append(values[0])
        shoes["sole materials"].append(values[1])
        shoes["outer materials"].append(values[2])
        shoes["closure types"].append(values[3])
        
        # Product Details 2
        product_details2 = []
        ul_list = driver.find_element(By.XPATH,"//div[@id='detailBullets_feature_div']")
        details = ul_list.find_elements(By.TAG_NAME, "li")
        for detail in details:
            product_details2.append(detail.text)
        
        for i in range(len(product_details2)):
            if "Date First Available" in product_details2[i]:
                value = product_details2[i].split(" : ", 1)[1]
                shoes["dates first available"].append(value)
            elif "ASIN" in product_details2[i]:
                value = product_details2[i].split(" : ", 1)[1]
                shoes["asin"].append(value)
            elif "Department" in product_details2[i]:
                value = product_details2[i].split(" : ", 1)[1]
                shoes["department"].append(value)
        
        # Ships from and Sold by
        min_msg = WebDriverWait(driver,10).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//span[@class='a-size-small offer-display-feature-text-message']"))
        )
        values = [span.text for index, span in enumerate(min_msg) if index != 2]
        shoes["ships from"].append(values[0])
        shoes["sold by"].append(values[1])
        
        # Product Picture
        img = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH, "//img[@id='landingImage']"))).get_attribute('src')
        img_name = shoes["names"][product_index] + ".jpg"
        img_path = os.path.join(img_file_name, img_name)
        response = requests.get(img)
        with open(img_path, "wb") as file:
            file.write(response.content)
    
        # go back to results to select another product
        driver.back()
        product_index +=1

# Export product details to a csv file
with open(csv_file_name, mode="w", newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=shoes.keys())
    writer.writeheader()
    
    for i in range(len(shoes["names"])):
        row = {key:shoes[key][i] for key in shoes}
        writer.writerow(row)

driver.quit()
