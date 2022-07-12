from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
import random
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from multiprocessing import Pool
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
cwd = os.getcwd()

opts = webdriver.ChromeOptions()

opts.headless = False
opts.add_argument('log-level=3') 
dc = DesiredCapabilities.CHROME
dc['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}
opts.add_argument('--ignore-ssl-errors=yes')
opts.add_argument("--start-maximized")
#opts.add_argument("window-size=200,100")
opts.add_argument('--ignore-certificate-errors')
opts.add_argument('--disable-blink-features=AutomationControlled')
prefs = {"profile.default_content_setting_values.notifications" : 2}
opts.add_experimental_option("prefs",prefs)
opts.add_experimental_option('excludeSwitches', ['enable-logging'])


def xpath_type(el,mount):
    return wait(browser,10).until(EC.presence_of_element_located((By.XPATH, el))).send_keys(mount)

def xpath_el(el):
    element_all = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, el)))
    
    return browser.execute_script("arguments[0].click();", element_all)

def claim():

    try:
        xpath_el('//button[@class="mat-focus-indicator btn-full-width btn-submit mat-raised-button mat-button-base"]')
        
    except:
        pass
    
   
    sleep(2)
    try:
        xpath_el("//button[contains(@class,'redeem')]")
        print(f"[{time.strftime('%d-%m-%y %X')}] [ {email} ] Trying to Redeem")
    except:
        browser.refresh()
        xpath_el("//button[contains(@class,'redeem')]")
     
    try:
        xpath_fast('(//span[@class="checkmark"])[1]')
    except:
        pass
    try:
        xpath_fast('(//span[@class="checkmark"])[2]')
    except:
        pass
    try:
        xpath_fast('(//span[@class="checkmark"])[3]')
    except:
        pass
 
    try:
        xpath_el('//*[text()="Tukarkan" or text()="Claim it"]')
    except:
        pass
    try:
        element = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '//div[@class="code-container"]')))
        element_voc = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '//p[@class="barcode-value"]')))
        element.screenshot(f'{cwd}/result/{email}Alfamart.png')
 
        print(f"[{time.strftime('%d-%m-%y %X')}] [ {email} ] Success Get Voucher [ {element_voc.text} ]")
        with open('sudah_redeem.txt','a') as f: f.write(f'{email}|{element_voc.text}\n')
        browser.quit()
    except:
        print(f"[{time.strftime('%d-%m-%y %X')}] [ {email} ] Failed Get Voucher")
        browser.quit()
   

def login_email():
    global element
    global browser
    
    xpath_el("//span[contains(text(),'Facebook')]")
    sleep(5)
    browser.switch_to.window(browser.window_handles[1])
    try:
        element = wait(browser,1).until(EC.element_to_be_clickable((By.ID, "m_login_email")))
    except:
        element = wait(browser,1).until(EC.element_to_be_clickable((By.ID, "email")))

    element.send_keys(email)
       
 
    sleep(1)
    try:
        element = wait(browser,2).until(EC.element_to_be_clickable((By.ID, 'm_login_password')))
    except:
        element = wait(browser,1).until(EC.presence_of_element_located((By.ID, 'pass')))
    
    element.send_keys(password)
    sleep(0.5)
    element.send_keys(Keys.ENTER)
    wait(browser,2).until(EC.presence_of_element_located((By.XPATH, '(//div[@role="button"])[2]'))).click()
    
    browser.switch_to.window(browser.window_handles[0])
    print(f"[{time.strftime('%d-%m-%y %X')}] [ {email} ] Success Login")
    claim()
    
def open_browser(k):
    
    global browser
    global element
    global email
    global password
    k = k.split("|")
    email = k[0]
    password = k[1]
 
    random_angka = random.randint(100,999)
    random_angka_dua = random.randint(10,99)
    opts.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36")
 
    browser = webdriver.Chrome(options=opts, desired_capabilities=dc)
    urls = "url.txt"
    urlsa = open(f"{cwd}/{urls}","r")
    urlss = urlsa.read()
    urlsss = urlss.split("\n")
    browser.get(urlsss[0])
    try:
        xpath_el('//button[@class="btn-grivy landing-btn"]')
        #print('clicked3')
    except:
        pass
    check_login = "false"
    try:
        xpath_el('//button[@class="mat-focus-indicator mat-primary btn-full-width btn-grivy mat-raised-button mat-button-base"]')
        check_login = "false"
    except:
        pass
        
    if check_login == "false":
        try:
            login_email()
        except Exception as e:
            print(f"[{time.strftime('%d-%m-%y %X')}] [ {email} ] Failed Login, Error: {e}")
            with open('failed.txt','a') as f:
                f.write('{0}|{1}\n'.format(email,password))
            browser.quit()
    else:
        claim()         

if __name__ == '__main__':
    global list_accountsplit
    global url
    print(f"[{time.strftime('%d-%m-%y %X')}] Automation CocaCola")
    url = input(f"[{time.strftime('%d-%m-%y %X')}] URL: ")
    with open('url.txt','w') as f: f.write(f'{url}\n')
    file_list_akun = "data.txt"
    myfile_akun = open(f"{cwd}/{file_list_akun}","r")
    akun = myfile_akun.read()
    list_accountsplit = akun.split("\n")
    jumlah = int(input(f"[{time.strftime('%d-%m-%y %X')}] Multi Processing: "))
    #open_browser(list_accountsplit[0])
    with Pool(jumlah) as p:  
        p.map(open_browser, list_accountsplit)
