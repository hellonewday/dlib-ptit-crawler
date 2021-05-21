#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
import csv
import urllib


chrome_options = webdriver.ChromeOptions();
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--mute-audio")


def extract_flowpaper(pureUrl):
    needToExtract = pureUrl.split("&");
    documentId = needToExtract[1].split("=")[1];
    subFolder = needToExtract[0].split("?subfolder=")[1];
    
    return f"http://dlib.ptit.edu.vn/flowpaper/services/view.php?doc={documentId}&format=pdf&subfolder={subFolder}";

def execute_program(url):
    print(f"Execute URL: {url}");
    browser = webdriver.Chrome("./chromedriver.exe",options=chrome_options);
    browser.get(url);
    
    ## Execute your hack here
    
    time.sleep(1);
    username = browser.find_element_by_name("login_email");
    username.send_keys("some-username");
    time.sleep(1);
    password = browser.find_element_by_name("login_password");
    password.send_keys("some-password");
    time.sleep(1);
    login = browser.find_element_by_name("login_submit");
    login.click();
    print("Login");
    browser.get("http://dlib.ptit.edu.vn/handle/HVCNBCVT/your-id?offset=your-offset");
    time.sleep(1);
    loopLength = len(browser.find_elements_by_class_name("img-listitem"));
    for i in range(0,loopLength):
                     
        document = browser.find_elements_by_class_name("img-listitem")[i];
        document.click();

        time.sleep(1);
        title = browser.find_elements_by_class_name("dc_title")[1].get_attribute("innerHTML");
        year = browser.find_elements_by_class_name("dc_date_issued")[1].get_attribute("innerHTML");
        print(f"{title} - {year}.pdf");
        browser.execute_script("document.getElementsByClassName('viewonline')[0].setAttribute('target', '_self');")
        accessDocument = browser.find_elements_by_class_name("viewonline")[0];
        accessDocument.click();

        time.sleep(1);
        downloadUrl = extract_flowpaper(browser.current_url);
        browser.get(downloadUrl);
        urllib.request.urlretrieve(downloadUrl, f'Your root dir:/your folder/{title} - {year}.pdf');
        ## Tell the program to close
        print("Done!");
        browser.get("http://dlib.ptit.edu.vn/handle/HVCNBCVT/your-id?offset=your-offset");
    browser.close();
    
execute_program("http://dlib.ptit.edu.vn/password-login");

