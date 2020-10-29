from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from pynput.keyboard import Key, Controller
import urllib.request
import time
import os
import getpass
import re

def instagramLogin(wd):
    
    time.sleep(3)
    user = wd.find_element_by_name("username")
    password = wd.find_element_by_name("password")

    user.clear()
    password.clear()

    instagram_username = getpass.getpass("Please enter your Instagram user account")
    user.send_keys(instagram_username)

    instagram_password = getpass.getpass("Please enter your Instagram password account")
    password.send_keys(instagram_password)
    
    time.sleep(5)
    wd.find_element_by_xpath("//button[@type='submit']").click()
    time.sleep(4)
    return

def makeMainDirectory(directory):
    main_directory = directory
    if not os.path.isdir(main_directory):
        os.mkdir(main_directory)
        os.chdir(main_directory)

def getInstagramAccount(instagram_username, wd):
    time.sleep(4)
    instagram_holder = instagram_username
    wd.get(f'https://www.instagram.com/{instagram_holder}/')

    time.sleep(2)

    #Scraping Photos
    scrapeInstagramAccountImages(instagram_holder, wd)

    #Get Inspector
    getInspector()

    #Scraping Instagram Actions
    hrefActions = getInstagramActions(instagram_holder, wd)
    print(hrefActions)
    
    #Scraping Following
    following = getFollowingInformation(hrefActions, wd)

    print(following)
    #Scraping Followers
    followers = getFollowersInformation(hrefActions, wd)
    print(followers)

def scrapeInstagramAccountImages(instagram_holder, wd):

    lenOfPage = wd.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage")
    match = False
    x = 100

    while match == False:
        directory = instagram_holder
        lastCount = lenOfPage
        time.sleep(30)
        instagram_urls = []
        instagram_capture = wd.find_elements_by_xpath("//img[@class='FFVAD']")

        for i in instagram_capture:
            instagram_urls.append(i.get_attribute('src'))
        
        if not os.path.isdir(directory):
            os.mkdir(directory)
        
        for i, link in enumerate(instagram_urls):
            path = os.path.join(instagram_holder, '{:06}.jpg'.format(i+x))

            urllib.request.urlretrieve(link, path)
          
        
        x += 100
        lenOfPage = wd.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage")

        if lastCount == lenOfPage:
            match = True
def getInstagramActions(instagram_holder, wd):

    wd.get(f'https://www.instagram.com/{instagram_holder}/')
    time.sleep(5)
    href_temp = wd.find_elements_by_xpath("//li[@class=' LH36I']")

    return href_temp

def getFollowingInformation(actions, wd):

    following_names = []
    following = actions[2]
    following.click()
    time.sleep(20)

    following_temp = wd.page_source
    following_data = bs(following_temp, 'html_parser')
    following_name = following_data.find_all('a')
    for i in following_name:
        following_names.append(i.get('title'))
    
    clean_following_names = [x for x in following_names if x != None]
    return clean_following_names
def getFollowersInformation(actions, wd):
    followers_names = []
    followers = actions[1]
    followers.click()
    time.sleep(20)

    followers_temp = wd.page_source
    followers_data = bs(followers_temp, 'html.parser')
    followers_name = following_data.find_all('a')

    for i in followers_name:
        followers_names.append(i.get('title'))
    
    clean_followers_names = [x for x in followers_names if x != None]
    return clean_followers_names

def getInspector():
    keyboard = Controller()
    keyboard.press(Key.ctrl)
    keyboard.press(Key.shift)
    keyboard.press('i')

    keyboard.release(Key.ctrl)
    keyboard.release(Key.shift)
    keyboard.release("i")
    time.sleep(5)

def main():

    DRIVER_PATH = './chromedriver'
    wd = webdriver.Chrome(executable_path= DRIVER_PATH)
    wd.get('https://www.instagram.com/')
    instagramLogin(wd)
    mainAccountDirectory = input(str("Please type a name to store your instagram accounts into: "))
    makeMainDirectory(mainAccountDirectory)

    while(True):
        instagramAccount = input(str("Please Type Instagram Account for me to find or 'quit' to end the program: "))

        if instagramAccount != "quit":
            getInstagramAccount(instagramAccount,wd)
        else:
            return False
if __name__ == "__main__":
    main()
