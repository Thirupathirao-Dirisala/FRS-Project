'''from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

chrome_options = Options()

# Set the path to the ChromeDriver executable (replace with your actual path)
chrome_options.add_argument('C:\\Users\\raot1\\Desktop\\chromedriver.exe')
chrome_options.add_experimental_option('debuggerAddress','localhost:8989')  # Update with your path'''
'''>chrome.exe --remote-debugging-port=8989 --user-data-dir="D:\Programs\chromeprofile"'C:\Program Files\Google\Chrome\Application'''
# Create a WebDriver instance with the Chrome options
'''driver = webdriver.Chrome(options=chrome_options)

# Open messages.google.com
driver.get('https://messages.google.com/web/conversations')

time.sleep(40)

numbers = ['+91 7207044710']

# Combine all numbers into a single string separated by commas
numbers_string = ', '.join(numbers)

# Find the search box and enter the numbers separated by commas
search=driver.find_element(By.XPATH,"/html/body/mw-app/mw-bootstrap/div/mw-g-ui-container/main/div/mw-main-container/div/mw-main-nav/div/mw-fab-link/a/span[2]/div/div")
search.click()
search_box=driver.find_element(By.XPATH,"/html/body/mw-app/mw-bootstrap/div/mw-g-ui-container/main/div/mw-main-container/div/mw-new-conversation-container/mw-new-conversation-sub-header/div/div[2]/mw-contact-chips-input/div/div/input")
search_box.send_keys(numbers[0])
search_box.send_keys(Keys.ENTER)
time.sleep(2)  # Adjust delay as needed
entered=driver.find_element(By.XPATH,"/html/body/mw-app/mw-bootstrap/div/mw-g-ui-container/main/div/mw-main-container/div/mw-new-conversation-container/div/mw-contact-selector-button/button/span[2]/span/span/span")
entered.click()
time.sleep(6)
add=driver.find_element(By.XPATH,"/html/body/mw-app/mw-bootstrap/div/mw-g-ui-container/main/div/mw-main-container/div/mw-conversation-container/div/div[1]/div/div/mw-new-conversation-sub-header/div/div[2]/button")
add.click()
for i in range(1,len(numbers)):
    try:
        search_box=driver.find_element(By.XPATH,"/html/body/mw-app/mw-bootstrap/div/mw-g-ui-container/main/div/mw-main-container/div/mw-new-conversation-container/mw-new-conversation-sub-header/div/div[2]/mw-contact-chips-input/div/div/input")
        search_box.send_keys(numbers[i])
        search_box.send_keys(Keys.ENTER)
        entered=driver.find_element(By.XPATH,"/html/body/mw-app/mw-bootstrap/div/mw-g-ui-container/main/div/mw-main-container/div/mw-new-conversation-container/div/mw-contact-selector-button/button/span[2]/span/span/span")
        entered.click()
        time.sleep(6)
        time.sleep(2)  # Adjust delay as needed
    except:
        driver.back()
next=driver.find_element(By.XPATH,"/html/body/mw-app/mw-bootstrap/div/mw-g-ui-container/main/div/mw-main-container/div/mw-new-conversation-container/mw-new-conversation-sub-header/div/div[2]/mw-contact-chips-input/button")
next.click()
time.sleep(4)
# Find the message box and enter the message
message_box = driver.find_element(By.XPATH,"/html/body/mw-app/mw-bootstrap/div/mw-g-ui-container/main/div/mw-main-container/div/mw-conversation-container/div/div[1]/div/mws-message-compose/div/div[2]/div/div/mws-autosize-textarea/textarea")
message_box.send_keys("Hii....!")
time.sleep(2)  # Adjust delay as needed
message_box.send_keys(Keys.ENTER)
time.sleep(2)  # Adjust delay as needed

driver.quit()'''
import csv
from datetime import datetime

# Get the current date


def retrieve_student_attendance(student_id):
    # Iterate over each day in the month
    d=datetime.now().day
    m=datetime.now().month
    y=datetime.now().year
    s,p=0,0
    a=[]
    for day in range(1, d+1):  # Assuming maximum of 31 days in a month
        try:
            
            # Construct the file name based on date format
            date_str = f"{m:02d}_{day:02d}_{y % 100:02d}"
            file_name = f"Attendance/Attendance-{date_str}.csv"
            # Read the CSV file for the day
            with open(file_name, newline='') as csvfile:
                reader = csv.reader(csvfile)
                s+=1
                # Search for the student's data in the file
                for row in reader:
                    if row[0] == student_id:
                        if row[4]=='Present':
                            p+=1
                            break
                        else:
                            a.append(date_str)
        except FileNotFoundError:
            # Handle missing files
            print(f"File {file_name} not found.")
            continue
    per=(p/s)*100
    return per,a

# Example usage
student_id = "y20acs441"  # Replace with the actual student ID
attendance = retrieve_student_attendance(student_id)
print(attendance)

