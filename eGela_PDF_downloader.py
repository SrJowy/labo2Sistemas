import time
from bs4 import BeautifulSoup
from pynput import keyboard
import requests
import getpass as gpass
import sys

break_program = False

def on_press(key):
    global break_program
    print(key)
    if key == keyboard.Key.end:
        print('end pressed')
        break_program = True
        return False

def princ(username, name):
    method = 'GET'
    print(method)
    uri = "https://egela.ehu.eus/login/index.php"
    print(uri)
    hdrs = {'Host': 'egela.ehu.eus',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.request(method, uri, headers=hdrs, allow_redirects=False)
    
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
        logintoken = logintoken_html.split('"')[5].split('"')
        
        password = gpass.getpass()

        method = 'POST'
        print(method)
        print(uri)
        hdrs = {'Host': 'egela.ehu.eus',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': cookie}
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
        #print("\n" + str(response.headers))
        #print(str(response.content) + "\n")
        
        print(response.status_code)
        print(cookie)
        print(location)
        print("---------------------------------------------------")
        
        if response.status_code == 303:
            html = BeautifulSoup(body, "html.parser")
            link_html = str(html.find_all('a'))
            link = link_html.split('"')[1]
            
            method = 'GET'
            print(method)
            print(link)
            location = resp_headers.get("Location")
            hdrs = {'Host': 'egela.ehu.es',
                    'Cookie': cookie}
            
            
            response = requests.request(method, link, headers=hdrs, allow_redirects=False)
            body = response.content
            location = resp_headers.get("Location")
            #print("\n" + str(response.headers))
            #print(str(response.content) + "\n")
            
            print(response.status_code)
            print(cookie)
            print(location)
            print("---------------------------------------------------")
            
            if response.status_code == 303:
                html = BeautifulSoup(body, "html.parser")
                #link_html = str(html.find_all('a'))
                #link = link_html.split('"')[1]
                link = "https://egela.ehu.eus"
                
                method = 'GET'
                print(method)
                print(link)
                hdrs = {'Host': 'egela.ehu.es',
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
                            while break_program == False:
                                print ('Press any key to continue...')
                                time.sleep(20)
                            listener.join()
                    elif body.find(name) == -1:
                        print("Program exited with code 1")
                        exit(1)
    

if __name__ == "__main__":
    username = sys.argv[1]
    name = sys.argv[2]
    princ(username, name)
