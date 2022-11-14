from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import random

filenames = ['email.txt', 'password.txt']
chrome_options = Options()
chrome_prefs = {
    "profile.default_content_setting_values": {
        "images": 1,
        "javascript": 1
    }
}

chrome_options.experimental_options["prefs"] = chrome_prefs
chrome_options.headless = False
chrome_options.add_argument("--log-level=3")
# driver_path = r"driver\chromedriver.exe"
# chrome_service = Service(driver_path)
driver = webdriver.Chrome(executable_path=r'driver\chromedriver.exe',chrome_options=chrome_options)
wait = WebDriverWait(driver, 20)
desired_url = "https://app.karier.mu/programmu"
url_login = "https://www.karier.mu/login"

def check_exists_by_xpath(classname):
    try:
        driver.find_element(By.CLASS_NAME,classname)
    except NoSuchElementException:
        return False
    return True
def check_exists_by_id(id):
    try:
        driver.find_element(By.ID,id)
    except NoSuchElementException:
        return False
    return True
def gen_line(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()

def wait_for_correct_current_url(desired_url):
    wait.until(
        lambda driver: driver.current_url == desired_url)


def cek_login():
    if(check_exists_by_xpath('login-error-message') == True):
        print('error message')
        message = driver.find_element(By.CLASS_NAME,"login-error-message").get_attribute("innerText")
        print(message)
        f1.write("Failed \t" + file1_line +"\t" + file2_line + "\t" + message + "\n")
        f1.close()
        print("-------------------------------------------------")
    elif(check_exists_by_xpath('field-error') == True):
        print("Failed input")
        f1.write("Failed \t" + file1_line +"\t" + file2_line + "\tFailed input login\n")
        f1.close()
        print("-------------------------------------------------")
    else:
        # print(driver.current_url)
        # sleep(100)
        print("Redirect to "+driver.current_url)
        driver.get("https://app.karier.mu/programmu")
        # wait_for_correct_current_url(desired_url)
        sleep(2)
        if(check_exists_by_xpath('card-program') == True):
            print("Login be successful")
            f1.write("Success\t" + file1_line +"\t" + file2_line + "\t")
            rows = len(driver.find_elements(By.CLASS_NAME,"card-program"))
            # pelatihan_judul = driver.find_element(By.XPATH,'//*[@id="programmu"]/div/div[3]/div/div[1]/a/div[1]/div[2]/div[2]').get_attribute("innerText")
            # pelatihan_presentase = driver.find_element(By.XPATH,'//*[@id="programmu"]/div/div[3]/div/div[1]/a/div[2]/div[2]/div/span').get_attribute("innerText")
            # f1.write(pelatihan_judul +"\t")
            pel = rows
            for x in range(rows):
                element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="programmu"]/div/div[3]/div/div['+str(pel)+']/a')))
                e = driver.find_element(By.XPATH,'//*[@id="programmu"]/div/div[3]/div/div['+str(pel)+']/a').get_attribute('href')
                judul = driver.find_element(By.XPATH,'//*[@id="programmu"]/div/div[3]/div/div['+str(pel)+']/a/div[1]/div[2]/div[2]').get_attribute("innerText")
                pelatihan_presentase = driver.find_element(By.XPATH,'//*[@id="programmu"]/div/div[3]/div/div['+str(pel)+']/a/div[2]/div[2]/div/span').get_attribute("innerText")
                f1.write("Pel " + str(pel) +"\t")
                f1.write(judul + "\t")
                f1.write(pelatihan_presentase + "\t")
                # driver.execute_script("window.open('');")
                # driver.switch_to.window(driver.window_handles[1])
                # driver.get(e)
                # print("redirect to pelatihan")
                # sleep(3)
                # if(check_exists_by_id('button-rating') == True):
                #     element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="button-rating"]')))
                #     e = driver.find_element(By.XPATH,'//*[@id="button-rating"]')
                #     e.click()
                #     e = driver.find_element(By.XPATH,'//*[@id="inactive-star-5"]')
                #     e.click()
                #     e = driver.find_element(By.XPATH,'//*[@id="activity-rating-modal___BV_modal_body_"]/div/div/textarea')
                #     testi = random.choice(list(open("testi.txt", "r", encoding="utf-8")))
                #     e.send_keys(testi)
                #     e = driver.find_element(By.XPATH,'//*[@id="rating-action-button"]')
                #     e.click()
                #     sleep(2)
                #     print("Testi terisi")
                #     f1.write("Testi ada\t")
                # else:
                #     print("Testi tidak ada")
                #     f1.write("Testi tidak ada\t")
                # # print(e)
                # driver.close()
                # driver.switch_to.window(driver.window_handles[0])
                x+=1
                pel -=1
            f1.write("\n")
            f1.close()
        else:
            print("Failed load page after login")
            f1.write("Failed \t" + file1_line +"\t" + file2_line + "\tFailed load after login\n")
            f1.close()
        print("Process Logout")
        driver.get('https://prakerja.karier.mu/?logout=1')
        print("-------------------------------------------------")

def login():
        print("Login with "+ file1_line + " & " + file2_line)
        driver.get("https://www.karier.mu/login")
        sleep(1)
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="input-login-email"]/input'))
        )
        e = driver.find_element(By.XPATH,'//*[@id="input-login-email"]/input')
        e.send_keys(file1_line)
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="input-login-password"]/input'))
        )
        e = driver.find_element(By.XPATH,'//*[@id="input-login-password"]/input')
        e.send_keys(file2_line)
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="button-login"]'))
        )
        e = driver.find_element(By.XPATH,'//*[@id="button-login"]')
        sleep(1)
        e.click()
        sleep(2)
        cek_login()

try:
    gens = [gen_line(n) for n in filenames]
    for file1_line,file2_line in zip(*gens):
        f1 = open('result_login.txt', 'a')
        login()
except:
    print("error login")
finally:
    print("complete")