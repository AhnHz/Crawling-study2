from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Chrome()
driver.get("https://www.opinet.co.kr/user/main/mainView.do")
time.sleep(2)
test = driver.find_elements(By.CLASS_NAME, "gnbTopa")[0]
ActionChains(driver).move_to_element(test).perform()

time.sleep(2)
driver.find_element(By.LINK_TEXT, "지역별").click()

time.sleep(2)
region = driver.find_element(By.ID, "SIDO_NM0")
region_detail = region.find_elements(By.TAG_NAME, "option")
for i in region_detail:
    print(i.text)

region_detail[2].click()
time.sleep(2)

region_second = driver.find_element(By.NAME, "SIGUNGU_NM0")
region_second_detail = region_second.find_elements(By.TAG_NAME, "option")[1:]
for i in region_second_detail:
    # 반복의 구를 하나씩 선택
    i.click()
    time.sleep(2)

    # 조회 버튼
    driver.find_element(By.ID, "searRgSelect").click()
    time.sleep(2)

    # 액셀 저장 버튼

    time.sleep(2)

driver.close()