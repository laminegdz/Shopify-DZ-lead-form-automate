from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

# List of Algerian cities
algeria_cities = [
    "Algiers", "Oran", "Constantine", "Annaba", "Blida", "Batna", "Djelfa", "Setif", 
    "Sidi Bel Abbes", "Biskra", "Tiaret", "Tlemcen", "Ouargla", "Bejaia", "Skikda", 
    "Mostaganem", "Tizi Ouzou", "Mascara", "Ghardaia", "Relizane", "El Oued", "Boumerdes", 
    "Bouira", "Chlef", "Medea", "Ain Defla", "Laghouat", "Khenchela", "Ain Temouchent", 
    "Tindouf", "Tamanrasset", "Adrar", "Saida", "Illizi", "Tebessa", "El Bayadh", 
    "Naama", "Bordj Bou Arreridj", "Tipaza", "Guelma", "Jijel", "Mila", "Souk Ahras", 
    "Tissemsilt", "El Tarf", "Bechar", "Oum El Bouaghi"
]

# Load file
with open('data/arabic_latin_names.txt', 'r', encoding='utf-8') as file:
    names = file.readlines()

# generate random Algerian phone numbers
def generate_algerian_phone_number():
    prefixes = ['078121', '077469', '055534', '067275']
    prefix = random.choice(prefixes)
    remaining_digits = ''.join(random.choices("0123456789", k=4))
    phone_number = f"{prefix}{remaining_digits}"
    return phone_number

#  setup Selenium WebDriver
def setup_driver():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection
    driver = webdriver.Chrome(options=options)
    return driver


order_count = 0


while True:
    driver = setup_driver()  

    try:
        driver.get("www.example.com")

        # Load email list
        with open('emails.txt', 'r', encoding='utf-8') as email_file:
            emails = email_file.readlines()

        if not emails:
            print("-------------- EMAILS ARE EMPTY ------------")
            driver.quit()
            break

        current_email = emails[0].strip()
        wait = WebDriverWait(driver, 30)

        # Fill form fields
        first_name = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='lfcod_first_name']")))
        first_name.click()
        first_name.send_keys(random.choice(names))
        time.sleep(1)

        phone = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='lfcod_phone']")))
        phone.click()
        phone_number = generate_algerian_phone_number()
        phone.send_keys(phone_number)
        time.sleep(1)

        city = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='lfcod_city']")))
        city.click()
        city.send_keys(random.choice(algeria_cities))
        time.sleep(1)

        email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='lfcod_email']")))
        email_input.click()
        email_input.send_keys(current_email)
        time.sleep(1)
        
        with open('emails.txt', 'w', encoding='utf-8') as email_file:
            email_file.writelines(emails[1:])

        
        submit_button = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='set-show-price']")))
        submit_button.click()
        time.sleep(5)
        order_count += 1
        print(f"[{order_count}] : {current_email} - Order sent successfully.")

        # Pause after every 15 orders
        if order_count % 15 == 0:
            print("Pausing for 5 seconds to avoid rate limiting...")
            time.sleep(10)
    
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()  # Close browser instance
