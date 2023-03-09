from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import sys
import csv


def decline_cookies(driver):
    try:
        wait = WebDriverWait(driver, 10)
        cookie_decline = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div[4]/div[3]")))
        cookie_decline.click()
    except:
        print("Unable to decline cookies.")

def get_department_list():
    
    department_dropdown.click()
    department_select = department_dropdown.find_elements(By.TAG_NAME, 'a')
    # department_list = [department.text for department in department_select]
    department_list = [department.text.rstrip() for department in department_select] # Needed for Product Management Department, as there is a stray &nbsp whitespace preceding it
    return department_list


def select_department(chosen_department):
    department_list = get_department_list()
    if chosen_department not in department_list:
        sys.exit(f"The {chosen_department} department is not listed.")
    for department in department_list:
        if department == chosen_department:
            department_select = driver.find_element(By.LINK_TEXT, department)
            try:
                wait.until(EC.element_to_be_clickable(department_select))
                department_select.click()
                break
            except ElementClickInterceptedException:
                # is_empty_department = True
                department_dropdown.click()
                return True
                break
                


def get_language_list():
    language_dropdown = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div[1]/div/div[3]/div/div/button')
    language_dropdown.click()
    lang = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div[1]/div/div[3]/div/div/div')
    language_select = lang.find_elements(By.TAG_NAME, 'div')
    language_list = []
    for language in language_select:
        name = language.find_element(By.CSS_SELECTOR, 'label.custom-control-label').text
        language_list.append(name)
    return language_list


def select_language(chosen_language):
    language_list = get_language_list()
    if chosen_language not in language_list:
        sys.exit(f"No available language by the name of {chosen_language}.")
    for language in language_list:
        if language == chosen_language:
            language_select = driver.find_element(By.XPATH, f"//label[text()='{language}']/preceding-sibling::input")
            if not language_select.is_selected():
                language_select.click()
            for other_language in language_list:
                if other_language != chosen_language:
                    other_language_select = driver.find_element(By.XPATH, f"//label[text()='{other_language}']/preceding-sibling::input")
                    if other_language_select.is_selected():
                        other_language_select.click()
            break



with open('input.csv', 'r') as input_file, open('output.csv', 'w', newline='') as output_file:
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)
    writer.writerow(['Department', 'Language', 'Listing Count'])

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    url = "https://cz.careers.veeam.com/vacancies"
    driver.get(url)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    department_dropdown = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div[1]/div/div[2]')
    is_empty_department = False
    decline_cookies(driver)

    next(reader) # Skip Header values

    for row in reader:
        chosen_department = row[0]
        chosen_language = row[1]

        is_empty_department = select_department(chosen_department)
        # cookie_decline = driver.find_element(By.XPATH, '/html/body/div[7]/div[4]/div[3]')
        # cookie_decline.click()
        select_language(chosen_language)
        
        if is_empty_department == True:
            listing_count = 0
        else:
            listing_column = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div[2]/div')
            listings = listing_column.find_elements(By.XPATH, './*')
            for listing in listings:
                if listing.tag_name == 'a':
                    listing_count = len(listings)
                    break
                else:
                    listing_count = 0

        writer.writerow([chosen_department, chosen_language, listing_count])

    driver.quit()