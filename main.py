from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support import expected_conditions as EC
import sys


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# service = Service(executable_path="/path/to/chromedriver")
# driver = webdriver.Chrome(service=service)
url = "https://cz.careers.veeam.com/vacancies"

driver.get(url)

driver.maximize_window()

wait = WebDriverWait(driver, 10)

chosenDepartment = "Research & Development"

chosenLanguage = "English"

element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div[1]/div/div[2]')))

departmentDropDown = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div/div[1]/div/div[2]')

departmentDropDown.click() 

departmentSelect = departmentDropDown.find_elements(By.CSS_SELECTOR, 'a.dropdown-item')
departmentList = []
for department in departmentSelect:

    departmentList.append(department.text)

for department in departmentSelect:


    if chosenDepartment in departmentList:
        try:
            wait.until(EC.element_to_be_clickable(department))
            is_clickable = True
        except:
            is_clickable = False
        if department.text == chosenDepartment and is_clickable == True:
            department.click()
            break
        elif department.get_attribute('class') == "text-muted disabled dropdown-item":
            sys.exit(f"The {chosenDepartment} department has no available vacancies.")
        else:
            pass # TODO find way to display print(f'No Available Department by the name of {department}') only once, if no matches found
    else:
        sys.exit(f'The {chosenDepartment} department is not listed')


cookieDecline = driver.find_element(By.XPATH, '/html/body/div[7]/div[4]/div[3]')
cookieDecline.click()

languageDropDown = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div/div[1]/div/div[3]/div/div/button')
languageDropDown.click()

lang = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div[1]/div/div[3]/div/div/div')
languageSelect = lang.find_elements(By.TAG_NAME, 'div')

for language in languageSelect: #TODO create a function/method for this iteration over the lists, rather than repeating this 
    name = language.find_element(By.CSS_SELECTOR, 'label.custom-control-label').text
    button = language.find_element(By.CSS_SELECTOR, 'input.custom-control-input')
    if name == chosenLanguage:
        button.click()
        break
    else:
        pass # TODO find way to display print(f'No Available language by the name of {language}') only once, if no matches found

listingColumn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div[2]/div')
listings = listingColumn.find_elements(By.XPATH, './*')

listingCount = len(listings)

vacanciesOpen = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/h3/span')


print(listingCount)
time.sleep(200)



# driver.quit()
