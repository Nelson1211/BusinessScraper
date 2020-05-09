from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time 
import csv
from os import path

browser = None
Link = "https://www.buzzfile.com/Home/Basic"
input_file = ''
output_file = ''

def open_page():
    global browser, Link
    browser = webdriver.Chrome('<PATH to Chrome Driver>')
    wait = WebDriverWait(browser, 600)
    browser.get(Link)
        
def check_exists_by_xpath(xpath):
    global browser
    try:
        browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def store_businesses(target, message):
    filename = "{}.csv".format(target)
    if path.exists(filename):
        with open('{}.csv'.format(target), 'a', newline='') as csvfile:
            businessWriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            businessWriter.write(message)
    else:
        with open('{}.csv'.format(target), 'w', newline='') as csvfile:
            businessWriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            businessWriter.write(message)

def search_business(business, business_address):
    global browser
    time.sleep(2)
    search_bar = browser.find_element_by_xpath("//input[contains(@class,'form-control searchTerm nav-search-term-text-home ui-autocomplete-input')]")
    search_bar.click()
    search_bar.send_keys(business)
    search_bar.send_keys(Keys.ENTER)
    time.sleep(3)
    counter = 2
    for i in range(1,100):
        if check_exists_by_xpath('//*[@id="companyList"]/tbody/tr[{}]'.format(counter)):
            address = browser.find_element_by_xpath('//*[@id="companyList"]/tbody/tr[{}]/td[4]/div/a'.format(counter))
            if address.text.strip() == business_address:
                browser.find_element_by_xpath('//*[@id="companyList"]/tbody/tr[{}]/td[2]/a'.format(counter)).click()
                time.sleep(2)
                if check_exists_by_xpath('//*[@id="1"]/div[3]/table/tbody/tr[1]/td[2]/span'):
                    contact = browser.find_element_by_xpath('//*[@id="1"]/div[3]/table/tbody/tr[1]/td[2]/span').text
                if check_exists_by_xpath('//*[@id="1"]/div[3]/table/tbody/tr[2]/td[2]/span'):
                    title = browser.find_element_by_xpath('//*[@id="1"]/div[3]/table/tbody/tr[2]/td[2]/span').text
                if check_exists_by_xpath('//*[@id="1"]/div[3]/table/tbody/tr[3]/td[2]/span'):
                    number = browser.find_element_by_xpath('//*[@id="1"]/div[3]/table/tbody/tr[3]/td[2]/span').text
                print(contact)
                print(title)
                print(number)
                if not contact:
                    contact = ""
                if not title:
                    title = ""
                return contact, title, number
            counter += 1
        else:
            break

def business_to_search(input_file, output_file):
    with open(output_file, mode='w') as number_file:
        output_writer = csv.writer(number_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        with open(input_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                name = row[0]
                address = row[1]
                try:
                    contact, title, phone = search_business(name, address)
                    output_writer.writerow([name, address, contact, title, phone])
                except:
                    print('Not Found')
                line_count += 1
                browser.quit()
                open_page()

if __name__ == "__main__":
    open_page()
    business_to_search(input_file, output_file)
    browser.quit()