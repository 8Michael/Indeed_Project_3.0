import selenium
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait as WA
from selenium.webdriver.support import expected_conditions as EC
import time
service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service("/Users/manla/Desktop/driver/chromedriver"))
#actions = ActionChains(driver)
def website(job,min_salary):
    links = []
    driver.get("https://www.indeed.com/")
    location = driver.find_element(By.XPATH, '//*[@id="label-text-input-what"]')
    location.send_keys(job)
    find_job = driver.find_element(By.CSS_SELECTOR, '.yosegi-InlineWhatWhere-primaryButton')
    find_job.click()
    salary = driver.find_element(By.ID,"filter-salary-estimate-menu")
    salary2 = salary.find_elements(By.CSS_SELECTOR, '.yosegi-FilterPill-dropdownListItem')
    salary_link = salary.find_elements(By.CSS_SELECTOR, '.yosegi-FilterPill-dropdownListItem [href]')
    for x in range(len(salary2)):
        links.append(salary_link[x].get_attribute('href'))
        salary2[x] = salary2[x].get_attribute("innerText").replace('$',"")
        salary2[x] = salary2[x].replace(',', "")
        salary2[x] = salary2[x].split('+')[0]
        if float(salary2[x]) >= float(min_salary):
            driver.get(links[x])
            url = driver.current_url
            gather_data()
            return 0
    length = len(salary2[0])
    if length < 6:
        print("ERROR: NO JOBS FIT CRITERIA. The minimum is: $" + salary2[0] + "+/hour and the maximum is: $" + salary2[len(salary2)-1]+ "+/hour")
    else:
        print("ERROR: NO JOBS FIT CRITERIA. The minimum is: $" + salary2[0] + "+/year and the maximum is: $" + salary2[len(salary2)-1]+ "+/year")
    return 0
def gather_data():
    #test = driver.find_element(By.XPATH,'//*[@id="filter-jobtype-menu"]/li[1]/a')
    #test2 = test.get_attribute('href')
    #driver.get(test2)
    acc2 = []
    jobs = driver.find_element(By.XPATH,'//*[@id="mosaic-provider-jobcards"]')
    company_name = jobs.find_elements(By.CSS_SELECTOR,'.css-1x7z1ps')
    company_address = jobs.find_elements(By.CSS_SELECTOR,'.css-t4u72d')
    company_pay = jobs.find_elements(By.CSS_SELECTOR, ".salary-snippet-container .css-1ihavw2")
    company_job = jobs.find_elements(By.CSS_SELECTOR,"h2 a")
    company_link = jobs.find_elements(By.CSS_SELECTOR,"h2 [href]")
    for x in range(len(company_pay)):
        acc = {"name":company_name[x].get_attribute('innerText'),"address":company_address[x].get_attribute('innerText'),"pay":company_pay[x].get_attribute('innerText'),"job":company_job[x].get_attribute('innerText'),"link":company_link[x].get_attribute('href')}
        acc2.append(acc)
    sheets(acc2)

def sheets(a):
    time.sleep(2)
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLScAMSOxyohRvJwPqIFt0H3rd3G6ieM7JyMphMYe8dh4Of4pRw/viewform?usp=sf_link")
    for x in range(len(a)):
        time.sleep(2)
        q1 = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        q1.send_keys(a[x]["name"])
        q2 = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        q2.send_keys(a[x]["job"])
        q3 = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        q3.send_keys(a[x]["address"])
        q4 = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input')
        q4.send_keys(a[x]["pay"])
        q5 = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input')
        q5.send_keys(a[x]["link"])
        submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
        submit.click()
        driver.get("https://docs.google.com/forms/d/e/1FAIpQLScAMSOxyohRvJwPqIFt0H3rd3G6ieM7JyMphMYe8dh4Of4pRw/viewform?usp=sf_link")
    driver.get("https://docs.google.com/spreadsheets/d/1kl1qp3Thj0ompyVqLPApW5x-cQPsIevpWx5XWmP3VV4/edit?resourcekey#gid=247262278")
    time.sleep(60)
website("Lawyer",50000)
#https://docs.google.com/forms/d/e/1FAIpQLScAMSOxyohRvJwPqIFt0H3rd3G6ieM7JyMphMYe8dh4Of4pRw/viewform?usp=sf_link
