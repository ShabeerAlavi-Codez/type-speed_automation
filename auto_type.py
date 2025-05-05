from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random




 # Wait for the text window to be visible
def simulate_human_typing(driver):
    text_window = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="text_window"]'))
    )
    
    # Find all letter spans in the text
    spans = driver.find_elements(By.CSS_SELECTOR, ".letter_default, .letter_marked, .letter_space")
    
    # Keep track of the current letter index
    current_index = 0
    # Start typing
    print("Starting typing automation...")
    
    for span in spans:
        # Randomize typing speed to simulate human behavior
        typing_delay = random.uniform(0.05, 0.2)
        
        # Get the letter to type
        letter_class = span.get_attribute("class")
        letter_id = span.get_attribute("id")
        
        # Extract the letter text
        if "letter_space" in letter_class:
            letter = " "
        else:
            letter = span.text
        
        # Simulate typing the letter
        driver.execute_script(f"document.dispatchEvent(new KeyboardEvent('keydown', {{key: '{letter}', code: 'Key{letter.upper() if letter.isalpha() else letter}', keyCode: {ord(letter.lower() if letter.isalpha() else letter)}, which: {ord(letter.lower() if letter.isalpha() else letter)}, bubbles: true}}));")
        driver.execute_script(f"document.dispatchEvent(new KeyboardEvent('keypress', {{key: '{letter}', code: 'Key{letter.upper() if letter.isalpha() else letter}', keyCode: {ord(letter.lower() if letter.isalpha() else letter)}, which: {ord(letter.lower() if letter.isalpha() else letter)}, bubbles: true}}));")
        driver.execute_script(f"document.dispatchEvent(new KeyboardEvent('keyup', {{key: '{letter}', code: 'Key{letter.upper() if letter.isalpha() else letter}', keyCode: {ord(letter.lower() if letter.isalpha() else letter)}, which: {ord(letter.lower() if letter.isalpha() else letter)}, bubbles: true}}));")
        
        # Wait to simulate human typing speed
        time.sleep(typing_delay)
        
        # Occasionally wait a bit longer to simulate thinking
        if random.random() < 0.05:
           # random.uniform(0.03, 0.1) #fast
           #random.uniform(0.3, 0.8) #noraml
            time.sleep(random.uniform(0.03, 0.05))
        
        current_index += 1
        
        if current_index % 10 == 0:
            print(f"Typed {current_index} characters...")

def main():
    service=Service()
    option = webdriver.ChromeOptions()
    option.add_argument("-incognito")
    option.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=service, options=option)

    
    try:
        # Navigate to the typing speed test website
        driver.get("https://typing-speed.net/")
        
        print("Page @1")
        # Wait for the page to load
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="text_window"]'))
        )
        
        print("Page loaded successfully")
        
        # Allow time for any initial animations or popups
        time.sleep(1)
        
        # Start the typing test
        # start_button = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, '//*[@id="speedtest_start"]'))
        # )
        # start_button.click()
        
        print("Test started")
        
        # Wait for the test to be ready
        time.sleep(2)
        
        # Simulate human typing
        simulate_human_typing(driver)
        
        # Wait to see the results
        print("Typing completed. Waiting for results...")
        time.sleep(10)
        
        # Try to get the results
        try:
            wpm = driver.find_element(By.XPATH, '//*[@id="result_wpm"]').text
            accuracy = driver.find_element(By.XPATH, '//*[@id="result_accuracy"]').text
            
            print(f"Results - WPM: {wpm}, Accuracy: {accuracy}")
        except:
            print("Could not retrieve results")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Keep the browser open for a while to see the results
        time.sleep(10)
        
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()