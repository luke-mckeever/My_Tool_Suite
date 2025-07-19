import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def bypass_recaptcha(url):
    # Initialize the WebDriver (assumes chromedriver is in PATH)
    driver = webdriver.Chrome()

    try:
        # Open the provided URL
        driver.get(url)
        time.sleep(2)  # Wait for page load

        # Fill visible input fields with dummy data
        input_fields = driver.find_elements(By.TAG_NAME, "input")
        for field in input_fields:
            field_type = field.get_attribute("type")
            field_name = field.get_attribute("name") or field.get_attribute("id")

            if field_type not in ["hidden", "submit", "checkbox"] and field.is_displayed():
                if field_name:
                    if "email" in field_name.lower():
                        field.send_keys("test@example.com")
                    elif "name" in field_name.lower() or "first" in field_name.lower():
                        field.send_keys("John")
                    elif "last" in field_name.lower():
                        field.send_keys("Doe")
                    elif "color" in field_name.lower():
                        field.send_keys("Blue")
                    else:
                        field.send_keys("Test123")

        # Handle reCAPTCHA iframe (if present)
        try:
            recaptcha_iframe = driver.find_element(By.XPATH, "//iframe[contains(@src, 'recaptcha')]")
            driver.switch_to.frame(recaptcha_iframe)
            recaptcha_checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox"))
            )
            recaptcha_checkbox.click()
            time.sleep(5)  # Wait for challenge (if any)

            # Check for image-based challenge
            if "imageselect" in driver.page_source.lower():
                print("[!] Image-based reCAPTCHA detected. Manual solving required.")

            driver.switch_to.default_content()  # Return to main page

        except Exception as e:
            print(f"[!] reCAPTCHA interaction failed: {e}")

        # Submit the form (if possible)
        submit_buttons = driver.find_elements(By.XPATH, "//input[@type='submit'] | //button[@type='submit']")
        if submit_buttons:
            submit_buttons[0].click()
            print("[+] Form submitted successfully!")
        else:
            print("[!] No submit button found.")

        time.sleep(5)  # Wait for result

    finally:
        driver.quit()  # Close browser

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python recaptcha.py <URL>")
        sys.exit(1)
    
    target_url = sys.argv[1]
    bypass_recaptcha(target_url)
