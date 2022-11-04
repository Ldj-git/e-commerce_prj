from selenium import webdriver
from urllib.request import urlopen
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os

# https://velog.io/@jungeun-dev/Python-%EC%9B%B9-%ED%81%AC%EB%A1%A4%EB%A7%81Selenium-%EA%B5%AC%EA%B8%80-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EC%88%98%EC%A7%91
# 참고 페이지
# pip로 selenium 깔고 크롬 드라이버도 받으면 됩니다.

#폴더 생성
if not os.path.isdir("test_img"):
    os.makedirs("test_img")

driver = webdriver.Chrome()
driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")

# 여기 리스트에 검색하려는 단어 넣어주면 됩니다. 
hubo=["대파"]

for search in hubo:
    # search = "향나무" # 검색어 여기에 식물 이름 들어감니다
    elem = driver.find_element_by_name("q") #검색창 찾기
    elem.clear()
    elem.send_keys(search) #검색어 입력
    elem.send_keys(Keys.RETURN) #엔터

    #스크롤 내리기
    SCROLL_PAUSE_TIME = 1

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            try:
                driver.find_element_by_css_selector(".mye4qd").click() #결과 더보기 버튼인듯?
            except:
                break
        last_height = new_height

    # 썸넬 클릭하고 원본 저장
    images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd") # 썸넬 이미지 css 셀렉터
    
    # 일단 항목당 200장만 받기로
    # 학습150 검증 50
    count = 1

    # test_img 라는 폴더 안에 사진 저장합니다.
    if not os.path.isdir("test_img/"+search):
        os.makedirs("test_img/"+search)

    for image in images:

        if count==201:
            break

        try:
            image.click()
            time.sleep(2)
            imgUrl = driver.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img').get_attribute('src') #썸낼 클릭한 커진 이미지의 xpath 넣어주기
            urllib.request.urlretrieve(imgUrl, "test_img/"+search+"/" + search + "_" + str(count) + ".jpg")
            print("Image saved: {}_{}.jpg".format(search, count))
            count += 1
        except:
            pass

driver.close()