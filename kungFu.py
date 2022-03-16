import base64
from xml.dom.minidom import Document
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def princ():
    method = 'GET'
    uri = "https://websistemak-httptest.appspot.com"
    hdrs = {'Host': 'websistemak-httptest.appspot.com'}
    response = requests.request(method, uri, headers=hdrs, allow_redirects=False)
    
    resp_headers = response.headers
    body = response.content
    location = resp_headers.get("Location")
    
    print(response.status_code)
    print("---------------------------------------------------")
    
    method = 'GET'
    hdrs = {'Host': 'websistemak-httptest.appspot.com'}
    response = requests.request(method, location, headers=hdrs, allow_redirects=False)
    
    resp_headers = response.headers
    body = response.content
    
    print(response.status_code)
    print("---------------------------------------------------")

    if response.status_code == 200:
        html = BeautifulSoup(body, "html.parser")
        form = str(html.find_all('form')).split('"')[1]
        
        method = 'POST'
        uri = uri + form
        hdrs = {'Host': 'websistemak-httptest.appspot.com',
                'Content-Type': 'application/x-www-form-urlencoded'}
        pet_body = "erantzuna=a&erantzuna=b&erantzuna=c"
        response = requests.request(method, uri, data=pet_body, headers=hdrs, allow_redirects=False)
        
        resp_headers = response.headers
        body = response.content
        location = resp_headers.get("Location")
        
        print(response.status_code)
        print("---------------------------------------------------")
        
        browser = webdriver.Firefox(executable_path=r'C:\\geckodriver.exe')
        browser.get(location)
        body = browser.page_source
        browser.close()
        html = BeautifulSoup(body, "html.parser")
        
        img_results = html.find_all('img')
        for idx, each in enumerate(img_results):
            if each.has_attr('src'):
                src = each['src']
            else:
                src = each['data-src']
            img = None
            if src.find("data:image") != -1:
                img = base64.b64decode(src.replace("data:image/png;base64,", ""))
            else:
                res = requests.get(src)
                img = res.content
            
            file = open(str(idx) + ".png", "wb")
            file.write(img)
            file.close()

if __name__ == "__main__":
    princ()
