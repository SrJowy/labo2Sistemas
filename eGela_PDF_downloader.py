from fileinput import filename
import os
from attr import NOTHING
from bs4 import BeautifulSoup
from pynput import keyboard
from pathlib import Path
import requests
import getpass as gpass


break_program = False

def on_press(key):
    global break_program
    if key == keyboard.Key.enter:
        print('end pressed')
        break_program = True
        return False

def princ(username, name):
    method = 'GET'
    print(method)
    uri = "https://egela.ehu.eus/login/index.php"
    print(uri)
    hdrs = {'Host': 'egela.ehu.eus'}
    body = ''
    response = requests.request(method, uri, headers=hdrs, data=body, allow_redirects=False)
    
    resp_headers = response.headers
    cookie_html = str(resp_headers.get("Set-Cookie")).split(";")
    cookie = cookie_html[0]
    location = resp_headers.get("location")
    body = response.content
    
    print(response.status_code)
    print(cookie)
    print(location)
    print("---------------------------------------------------")
    
    if response.status_code == 200:
        html = BeautifulSoup(body, "html.parser")
        logintoken_html = str(html.find_all('input',{'name': "logintoken"}))
        logintoken = logintoken_html.split('"')[5]
        
        password = gpass.getpass()

        method = 'POST'
        print(method)
        print(uri)
        hdrs = {'Host': 'egela.ehu.eus',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': cookie}
        print(hdrs)
        pet_body = {'logintoken': logintoken,
                    'username': username,
                    'password': password}
        print(pet_body)
        
        response = requests.request(method, uri, data=pet_body, headers=hdrs, allow_redirects=False)
        body = response.content
        resp_headers = response.headers
        cookie_html = str(resp_headers.get("Set-Cookie")).split(";")
        cookie = cookie_html[0]
        location = resp_headers.get("Location")
        
        print(response.status_code)
        print(cookie)
        print(location)
        print("---------------------------------------------------")
        
        if response.status_code == 303:
            method = 'GET'
            print(method)
            print(location)
            
            hdrs = {'Host': 'egela.ehu.eus',
                    'Cookie': cookie}
            print(hdrs)
            
            response = requests.request(method, location, headers=hdrs, allow_redirects=False)
            body = response.content
            location = resp_headers.get("Location")
            
            print(response.status_code)
            print(cookie)
            print(location)
            print("---------------------------------------------------")
            
            if response.status_code == 303:
                link = response.headers['Location']
                
                method = 'GET'
                print(method)
                print(link)
                hdrs = {'Host': 'egela.ehu.eus',
                        'Cookie': cookie}
                response = requests.request(method, link, headers=hdrs, allow_redirects=False)
                body = str(response.content)
                location = resp_headers.get("Location")
                
                
                print(response.status_code)
                print(cookie)
                print(location)
                print("---------------------------------------------------")
                
                if response.status_code == 200:
                    if body.find(name) != -1:
                        with keyboard.Listener(on_press=on_press) as listener:
                            print ('Press enter to continue...')
                            while break_program == False:
                                NOTHING
                            listener.join()
                        downloadPDF(response.content, cookie)
                    elif body.find(name) == -1:
                        print("Program exited with code 1")
                        exit(1)
    
def downloadPDF(res, cookie):
    html = BeautifulSoup(res, "html.parser")
    
    for link in html.find_all('a'):
        if "Sistemas Web" in link:
            uri = str(link).split('"')[3]
            method = 'GET'
            print(method)
            print(uri)
            hdrs = {'Host': 'egela.ehu.eus', 
                    'Cookie': cookie}
            response = requests.request(method, uri, headers=hdrs, allow_redirects=False)
            
            print(response.status_code)
            print(response.reason)
            print(cookie)
            print("---------------------------------------------------")
            
            html = BeautifulSoup(response.content, "html.parser")
            counter = 0
            
            if not os.path.exists("downloadedPDFs"):
                os.mkdir("downloadedPDFs")
            
            print("\nDescargando PDFs...\n")
            for link in html.find_all('img', {'class': 'iconlarge activityicon'}):
                if "/pdf" in str(link):
                    uri = link.parent.get('href')
                    method = 'GET'
                    hdrs = {'Host': 'egela.ehu.eus', 
                            'Cookie': cookie}
                    response = requests.request(method, uri, headers=hdrs, allow_redirects=False)
                    
                    html = BeautifulSoup(response.content, "html.parser")
                    link_pdf = str(html.find_all('a')).split('"')[1]
                    name = str(link_pdf).split('/')[8]
                    filename = Path('./downloadedPDFs/' + name)
                    if not os.path.exists('./downloadedPDFs/' + name):
                        
                        method = 'GET'
                        hdrs = {'Host': 'egela.ehu.eus', 
                                'Cookie': cookie}
                        response = requests.request(method, link_pdf, headers=hdrs, allow_redirects=False)
                        filename.write_bytes(response.content)
                        counter += 1
                    
            print("Descarga completada de " + str(counter) + " PDFs")
                    
                    
                    

if __name__ == "__main__":
    #username = sys.argv[1]
    #name = sys.argv[2]
    username = '966786'
    name = 'JOEL'
    princ(username, name)
