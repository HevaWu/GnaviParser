# coding: UTF-8

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox import service
from selenium import webdriver
import pandas as pd
import time

cap = DesiredCapabilities().FIREFOX
cap["marionette"] = True
firefox_service1 = service.Service(executable_path="/usr/local/bin/geckodriver")
driver = webdriver.Firefox(service=firefox_service1)
firefox_service2 = service.Service(executable_path="/usr/local/bin/geckodriver")
detail_driver = webdriver.Firefox(service=firefox_service2)

link = 'https://r.gnavi.co.jp/character/kods00074/rs/'

# https://r.gnavi.co.jp/character/kods00074/rs/
# https://r.gnavi.co.jp/character/kods00074/rs/?p=2

def main():
    df_restaurant = pd.DataFrame()
    try:
        for i in range(0, 204):
            pageLink = link + '?p=' + str(i+1)
            print("==== current link ", i, pageLink)

            driver.get(pageLink)
            time.sleep(2)

            for lists in driver.find_elements(By.CLASS_NAME, 'result-cassette__list'):
                for element in lists.find_elements(By.CLASS_NAME, 'result-cassette__box'):
                    titles = element.find_elements(By.CSS_SELECTOR, ' div.result-cassette__box-inner.js-slide.js-cassette-link-expander.js-measure > div.result-cassette__box-main > div.result-cassette__box-head > div > a')

                    if len(titles) == 0:
                        continue
                    else:
                        title = titles[0]

                    r_name = title.text
                    r_url = title.get_attribute('href')

                    r_address = ""
                    detail_driver.get(r_url)
                    time.sleep(2)
                    address_links = detail_driver.find_elements(By.CSS_SELECTOR, '#info-table > table > tbody > tr:nth-child(3) > td > p > span.region')
                    if len(address_links) > 0:
                        address_info = address_links[0]
                        r_address = address_info.text

                    r_access = ""
                    r_description = ""
                    r_average_price = ""

                    info_elements = element.find_elements(By.CLASS_NAME, 'result-cassette__box-basic-info')
                    if len(info_elements) > 0:
                        info = info_elements[0]
                        access = info.find_elements(By.CLASS_NAME, 'result-cassette__box-access')
                        if len(access) > 0:
                            r_access = access[0].text
                        info_items = info.find_elements(By.CLASS_NAME, 'result-cassette__box-summary-item')
                        if len(info_items) > 0:
                            r_description = info_items[0].text
                        if len(info_items) > 1:
                            r_average_price = info_items[1].text

                    r_pet_dog_small = ""
                    r_pet_dog_medium = ""
                    r_pet_dog_large = ""
                    r_pet_cat = ""
                    r_pet_others = ""

                    r_pet_other_info = ""

                    foot_lists = element.find_elements(By.CLASS_NAME, 'result-cassette__box-foot')
                    if len(foot_lists) > 0:
                        foot_list = foot_lists[0]

                        for foot_ele in foot_list.find_elements(By.CSS_SELECTOR, 'dl.result-cassette__table.result-cassette__table--link.js-cassette-link-expander.js-measure'):
                            pet_tables = foot_ele.find_elements(By.CLASS_NAME, 'result-cassette__table-head-text')
                            if len(pet_tables) == 0:
                                continue
                            pet_table = pet_tables[0]
                            pet_list_elements = foot_ele.find_elements(By.CLASS_NAME, "pet-list__item")

                            if pet_table.text == "ペット同伴可":
                                other_info1 = foot_ele.find_elements(By.CLASS_NAME, 'result-cassette__table-set-head result-cassette__table--underline')
                                if len(other_info1) > 0:
                                    r_pet_other_info = r_pet_other_info + other_info1[0].text + " "

                                other_info2 = foot_ele.find_elements(By.CLASS_NAME, 'result-cassette__table-set-body')
                                if len(other_info2) > 0:
                                    r_pet_other_info = r_pet_other_info + other_info2[0].text

                                for pet_list_element in pet_list_elements:
                                    pet_list_element_details = pet_list_element.find_elements(By.CLASS_NAME, 'pet-list__text')
                                    if len(pet_list_element_details) == 0:
                                        continue
                                    pet_list_name = pet_list_element_details[0].text
                                    pet_list_status_elements = pet_list_element.find_elements(By.CSS_SELECTOR, 'li.pet-list__status-list-item.pet-list__status-list-item--active')

                                    pet_temp = ""
                                    for pet_list_status_ele in pet_list_status_elements:
                                        pet_temp = pet_temp + pet_list_status_ele.text

                                    if pet_list_name == "小型犬":
                                        r_pet_dog_small = pet_temp
                                    elif pet_list_name == "中型犬":
                                        r_pet_dog_medium = pet_temp
                                    elif pet_list_name == "大型犬":
                                        r_pet_dog_large = pet_temp
                                    elif pet_list_name == "ネコ":
                                        r_pet_cat = pet_temp
                                    elif pet_list_name == "その他小動物":
                                        r_pet_others = pet_temp

                    restaurant = {
                        'name': r_name,
                        'url': r_url,
                        'address': r_address,
                        'access': r_access,
                        'description': r_description,
                        'average_price': r_average_price,
                        'pet_dog_small': r_pet_dog_small,
                        'pet_dog_medium': r_pet_dog_medium,
                        'pet_dog_large': r_pet_dog_large,
                        'pet_cat': r_pet_cat,
                        'pet_others': r_pet_others,
                        'pet_otherInfo': r_pet_other_info
                    }

                    df_restaurant=df_restaurant.append(restaurant,ignore_index=True)
        df_restaurant.to_csv('./gnavi.csv', index=False, encoding='utf_8_sig')
        driver.quit()
        detail_driver.quit()
    except:
        df_restaurant.to_csv('./gnavi.csv', index=False, encoding='utf_8_sig')


if __name__ == '__main__':
    main()

