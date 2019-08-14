from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep
import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request
import pandas as pd
driver = webdriver.Chrome("./chromedriver.exe")
driver.get("https://pemilu2019.kpu.go.id/#/dprri/hitung-suara/")
driver.maximize_window()
sleep(2)
#s1= Select(driver.find_element_by_id('scope-options'))
#print(s1.options)
#s1.select_by_index(0)
action = ActionChains(driver)
action_2 = ActionChains(driver)
s1 = driver.find_element_by_id('scope-options')
action.move_to_element(s1).perform()
sleep(2)
s1.click()
#s1.send_keys(Keys.DOWN)
#s1.send_keys(Keys.ENTER)
sleep(2)
s2 = driver.find_element_by_class_name("dropdown-menu")
s2.click()
sleep(2)
s3 = driver.find_element_by_class_name("form-control")
s3.click()
s3.send_keys(Keys.TAB * 3)
sleep(2)

s4 = driver.find_element_by_class_name("dropdown-menu")
#action.move_to_element(s4).perform()
action.send_keys(Keys.ARROW_DOWN * 14)
action.send_keys(Keys.ENTER).perform()

action.move_to_element(s2).perform()
s3.click()
sleep(2)
s3.send_keys(Keys.TAB * 4)

sleep(2)

s6 = driver.find_element_by_class_name("dropdown-menu")
action_2.send_keys(Keys.ARROW_DOWN * 17)
action_2.send_keys(Keys.ENTER).perform()
#action.send_keys("SURABAYA")
##action.move_to_element(s6).perform()
sleep(3)
#action.send_keys(Keys.ENTER).perform()

scrapy_selector = Selector(text = driver.page_source)
table = scrapy_selector.xpath('//*[@class="data-table"]')
trs = table.xpath('.//tr')[1:]

province, pkb, gerindra, pdip, golkar, nasdem, garuda, berkarya, pks, perindo, ppp, psi, pan, hanura, demokrat, pbb, pkpi = ([] for i in range(17))
party = [pkb, gerindra, pdip, golkar, nasdem, garuda, berkarya, pks, perindo, ppp, psi, pan, hanura, demokrat, pbb, pkpi]
for indexes in range (31):
    label_province = trs.xpath('//*[@class="clear-button text-primary text-left"]/text()')[indexes].extract()
    label_province = label_province.replace('\n','')
    province.append(label_province)


for indexes_count in range(2,18):
    str_indexes_count = str(indexes_count)
    for go in range(31):
        rank_1 = trs.xpath('.//td['+str_indexes_count+']/text()')[go].extract()
        #print(rank_1)
        rank_1 = rank_1.replace('\n','')
        rank_1 = rank_1.replace('.','')
        rank_1 = int(rank_1)
        party[indexes_count-2].append(rank_1)
print("DONE !!!")
data = pd.DataFrame({'Provinsi':province,
                    'PKB':party[0],
                    'Gerindra':party[1],
                    'PDIP':party[2],
                    'Golkar':party[3],
                    'Nasdem':party[4],
                    'Garuda':party[5],
                    "Berkarya":party[6],
                    "PKS":party[7],
                    "Perindo":party[8],
                    "PPP":party[9],
                    "PSI":party[10],
                    "PAN":party[11],
                    "Hanura":party[12],
                    "Demokrat":party[13],
                    "PBB":party[14],
                    "PKPI":party[15]
                    })#
#data.to_csv('dpr_election_new.csv',index=False)
data.to_excel('dpr_election_new_1.xlsx')

driver.quit()





