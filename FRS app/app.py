from flask import Flask, render_template, request, redirect, url_for, session
import random
import smtplib
from apscheduler.schedulers.blocking import BlockingScheduler
import matplotlib.pyplot as plt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import sqlite3
import hashlib
import pickle
import cv2
import os
import re
import threading
import winsound
import datetime as dt
import face_recognition
from datetime import date
from datetime import datetime
import numpy as np
import pandas as pd
import joblib
import time
import schedule
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By



app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
MESSAGE = "WELCOME  " \
          " Instruction: to register your attendence kindly click on 'a' on keyboard"
datetoday = date.today().strftime("%m_%d_%y")
day = datetime.today().strftime("%A")
datetoday2 = date.today().strftime("%d-%B-%Y")
c_time = datetime.now().strftime("%H:%M")
month=datetime.now().strftime("%B")
year=datetime.now().year
known_images, known_encodings, known_names =[],[],[]
#### Initializing VideoCapture object to access WebCam
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
try:
    cap = cv2.VideoCapture(1)
except:
    cap = cv2.VideoCapture(0)
import csv
import sqlite3
import csv
import csv
import os
from datetime import datetime
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
def retrieve_user_data(user_id):
    # Get the current month
    #cm= datetime.now().strftime("%m")
    
    # List to store user data
    user_data_list = []
    dates=[]
    attendance_data = []
    p=0
    a=0
    # Directory containing CSV files
    directory = 'Attendance'
    
    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            a+=1
            parsed_date = datetime.strptime(filename[11:19], "%m_%d_%y")
            # Convert the datetime object to the desired format
            formatted_date = parsed_date.strftime("%Y-%m-%d")
            dates.append(formatted_date)
            file_path = os.path.join(directory, filename)
            
            # Read CSV file
            with open(file_path, 'r', newline='') as file:
                reader = csv.reader(file)
                
                # Skip header
                next(reader)
                
                # Iterate through rows
                for row in reader:
                    # Check if row corresponds to the current month and user_id
                    if row[0] == user_id:
                        # Append the row to user_data_list
                        if row[4]=='':
                            user_data_list.append('Absent')
                        else:
                            p+=1
                            user_data_list.append(row[4])
    
    for date, statuses in zip(dates, user_data_list):
        attendance_data.append({"date": date, "status": statuses})
    per=int((p/a)*100)
    return p,a,per,attendance_data

def add_users_to_csv(username,role, ip_address):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('user-logs.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
    for i, row in enumerate(rows):
            if i == 0:  # Skip header row
                continue
            if row[0]==username:  # Check for leading/trailing whitespaces
                if row[3] =='-':
                    with open('user-logs.csv', 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerows(rows)
                    break
                else:
                    with open('user-logs.csv', 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerows(rows)
                        writer.writerow([username,role, timestamp,"-",ip_address])

def add_logout_time(username):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        # Read the CSV file
        with open("user-logs.csv", 'r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
        # Find the row with the matching userid
        for i, row in enumerate(rows):
            if i == 0:  # Skip header row
                continue
            if row[0]==username:  # Check for leading/trailing whitespaces
                if row[3] =='-':
                    row[3] = timestamp
                    try:
                        with open("user-logs.csv", 'w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerows(rows)
                    except Exception as e:
                        print(f"Error writing to file: {e}")
    except Exception as e:
                        print(f"Error writing to file: {e}")
                    
                
        

def add_column_to_csv(csv_file, new_column_name, new_column_data):
    # Read existing CSV file and store data
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Add new column header to the first row
    rows[0].append(new_column_name)

    # Add new column data to each row
    for row in rows[1:]:
        row.append(new_column_data)

    # Write updated data back to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def add_row(csv_file,id,user,email,mobile,status):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
    data=[id,user,email,mobile,status]
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write header row
        # Write data rows
        writer.writerows(rows)
        writer.writerow(data)


def export_to_csv(database_file,table_name,csv_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor() 
    included_columns = ['id', 'username', 'email','mobile']  # Specify column names
    # Generate the SELECT query with specified columns
    columns_str = ', '.join(included_columns)
    select_query = f"SELECT {columns_str} FROM {table_name}"

    # Fetch data from the database table
    cursor.execute(select_query)
    data = cursor.fetchall()
    # Write data to CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write header row
        writer.writerow(included_columns)
        # Write data rows
        writer.writerows(data)

    # Close database connection
    conn.close()

#### If these directories don't exist, create them
if not os.path.isdir('Attendance'):
    os.makedirs('Attendance')
if not os.path.isdir('static'):
    os.makedirs('static')
if not os.path.isdir('static/faces'):
    os.makedirs('static/faces')
if f'Attendance-{datetoday}.csv' not in os.listdir('Attendance'):
    export_to_csv('users.db', 'students', f'Attendance/Attendance-{datetoday}.csv')
    add_column_to_csv(f'Attendance/Attendance-{datetoday}.csv','Attendance', '')
def monthly_report():
    df=pd.read_csv(f'Attendance/Attendance-{datetoday}.csv')
    id=df['id']
    p,a=[],[]
    emails=df['email']
    users=df['username']
    for i in range(len(id)):
        pers,att=retrieve_student_attendance(id[i])
        p.append(pers)
        a.append(att)
    sender_email = 'raot14693@gmail.com'
    password = 'fwio cdlx sofp ddvu'
    for i in range(0,len(emails)):
        # Email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = emails[i]
        msg['Subject'] = f"Monthly Attendance Report of {users[i]}"
        body = f"""\

Dear,

I hope this email finds you well. As part of our ongoing commitment to keeping you informed about your child's progress, I am pleased to provide you with the monthly attendance report for {users[i]}.

Month: {month}
Year: {year}
Attendance Percentage: {p[i]}
Absent Summary:
{a[i]}


Please review the attached report for a detailed breakdown of your child's attendance for the past month. If you have any questions or concerns, please don't hesitate to reach out to me.

Thank you for your continued support in your child's education.

Best regards,
Rao
Face Recognition Attendance System


    """
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Connect to SMTP server (for Gmail)
            smtp_server = 'smtp.gmail.com'
            port = 587
            server = smtplib.SMTP(smtp_server, port)
            server.starttls()
            
            # Login to the email account
            server.login(sender_email, password)
            
            # Send the email
            server.sendmail(sender_email,emails[i], msg.as_string())
            print("Email sent successfully")
            
            
            # Close the connection
            server.quit()
        except Exception as e:
            print("Failed to send email:", e)
def send_details():
    df=pd.read_csv(f'Attendance/Attendance-{datetoday}.csv')
    att=df['Attendance']
    email=df['email']
    mobile=df['mobile']
    users=[]
    usernames=df['username']
    eml=[]
    mbl=[]
    for i in range(0,len(att)):
        if att[i]!='Present':
            eml.append(email[i])
            mbl.append(str(mobile[i]))
            users.append(usernames[i])
    return eml,users,mbl
def send_emails():
    emails,users,m=send_details()
    sender_email = 'raot14693@gmail.com'
    password = 'fwio cdlx sofp ddvu'
    for i in range(0,len(emails)):
        # Email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = emails[i]
        msg['Subject'] = f"Notification of Absence - {users[i]}"
        body = f"""\
    Dear,
    
    I hope this email finds you well.
    
    I'm writing to inform you that your son/daughter, {users[i]}, was absent from class today, {datetoday}.
    
    
    Please let us know if there are any circumstances or concerns regarding {users[i]}'s absence that we should be aware of. Additionally, if you could provide a written note or explanation upon his/her return, it would greatly assist us in maintaining accurate attendance records.
    
    If you have any questions or require further clarification, please don't hesitate to reach out to me.
    
    Thank you for your attention to this matter.
    
    Best regards,

    Face Recognition Attendance System
    """
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Connect to SMTP server (for Gmail)
            smtp_server = 'smtp.gmail.com'
            port = 587
            server = smtplib.SMTP(smtp_server, port)
            server.starttls()
            
            # Login to the email account
            server.login(sender_email, password)
            
            # Send the email
            server.sendmail(sender_email,emails[i], msg.as_string())
            print("Email sent successfully")
            print(m)
            
            # Close the connection
            server.quit()
        except Exception as e:
            print("Failed to send email:", e)
    #### get a number of total registered users
def sendsms():
    e,u,numbers=send_details()
    print(numbers)
    chrome_options = Options()
    chrome_options.add_argument('C:\\Users\\raot1\\Desktop\\chromedriver.exe')
    chrome_options.add_experimental_option('debuggerAddress','localhost:8989')  # Update with your path
    '''>chrome.exe --remote-debugging-port=8989 --user-data-dir="D:\Programs\chromeprofile"'C:\Program Files\Google\Chrome\Application'''
    # Create a WebDriver instance with the Chrome options
    driver = webdriver.Chrome(options=chrome_options)

    # Open messages.google.com
    driver.get('https://messages.google.com/web/conversations/new')

    time.sleep(40)


    # Find the search box and enter the numbers separated by commas
    search_box=driver.find_element(By.XPATH,"/html/body/mw-app/mw-bootstrap/div/mw-g-ui-container/main/div/mw-main-container/div/mw-new-conversation-container/mw-new-conversation-sub-header/div/div[2]/mw-contact-chips-input/div/div/input")
    search_box.send_keys(numbers[0])
    search_box.send_keys(Keys.ENTER)
    time.sleep(2)  # Adjust delay as needed
    entered=driver.find_element(By.XPATH,"/html/body/mw-app/mw-bootstrap/div/mw-g-ui-container/main/div/mw-main-container/div/mw-new-conversation-container/div/mw-contact-selector-button/button")
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
    msg="Waste and worst fellow"
    message_box.send_keys(msg)
    time.sleep(2)  # Adjust delay as needed
    message_box.send_keys(Keys.ENTER)
    time.sleep(2)  # Adjust delay as needed

    driver.quit()
    
def schedule_task():
    #schedule.every().day.at("20:31").do(send_emails)
    #schedule.every().day.at("22:27").do(sendsms)
    schedule.every(28).days.at("23:38").do(monthly_report)
    # Run the scheduler indefinitely
    while True:
        schedule.run_pending()
        time.sleep(60)
def schedule_task1():
  scheduler = BlockingScheduler()

  # Define the trigger: 17th of every month at 23:30
  trigger = 'cron'  # Use cron expression for scheduling
  day_of_month = '17'
  hour = '23'
  minute = '59'
  job = scheduler.add_job(monthly_report, trigger, day=day_of_month, hour=hour, minute=minute)

  print("Scheduler started! Waiting for the 17th of each month at 11:30 PM...")
  scheduler.start()
# Start the scheduler in a separate thread
scheduler_thread = threading.Thread(target=schedule_task1)
scheduler_thread.start()


def totalreg():
    return len(os.listdir('static/faces'))
def is_valid_password(password):
    # Check if the password contains at least 8 characters
    if len(password) < 8:
        return False
    
    # Check if the password contains at least one letter, one digit, and one special character
    if not re.search(r"[a-zA-Z]", password) or \
       not re.search(r"\d", password) or \
       not re.search(r"[!@#$%^&*()_+{}[\]:;<>,.?~]", password):
        return False
    
    return True
#### extract the face from an image
def extract_faces(img):
    if img!=[]:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_points = face_detector.detectMultiScale(gray, 1.3, 5)
        return face_points
    else:
        return []

#### Identify face using ML model
def identify_face(facearray):
    model = joblib.load('static/face_recognition_model.pkl')
    return model.predict(facearray)

#### A function which trains the model on all the faces available in faces folder
import os
import face_recognition

def load_images_from_directory(folder_path):
    images = []
    encodings = []
    names = []
    try:
        with open('encodings.pkl', 'rb') as f:
            known_encodings, known_names = pickle.load(f)
    except:
        known_names=[]
        known_encodings=[]
    for root, _, files in os.walk(folder_path):
        # Process images from this subfolder
        for filename in files:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):  # Case-insensitive image extensions
                image_path = os.path.join(root, filename)
                name = os.path.splitext(filename)[0]
                
                if name not in known_names:
                    try:
                        image = face_recognition.load_image_file(image_path)
                        encoding = face_recognition.face_encodings(image)[0]
                        name = os.path.splitext(filename)[0]  # Extract name from filename (without extension)
                        images.append(image)
                        encodings.append(encoding)
                        names.append(name)
                    except FileNotFoundError:
                        print(f"Error: File not found: {image_path}")  # Handle missing files gracefully
                    except IndexError:
                        print(f"Error: No faces detected in image: {image_path}")  # Handle empty images
    with open('encodings.pkl', 'wb') as f:  # Open file in 'wb' mode to overwrite existing content
        pickle.dump((known_encodings + encodings, known_names + names), f)
    return images, encodings, names
def extract_attendance():
    df = pd.read_csv(f'Attendance/Attendance-{datetoday}.csv')
    rolls= df['id']
    names = df['username']
    attendance=df['Attendance']
    present=0
    for i in attendance:
        if i=="Present":
            present=present+1
    l = len(df)
    return names,rolls,attendance,l,present
def extract_users():
    df = pd.read_csv('user-logs.csv')
    names= df['Username']
    roles=df['Role']
    login = df['Login Time']
    logout=df['Logout Time']
    ip=df['IP-Address']
    l = len(df)
    return names,roles,login,logout,ip,l

#### Add Attendance of a specific user
def add_attendance(name):
    username, userid = name.split('_')[0], name.split('_')[1]
    current_time = datetime.now().strftime("%H:%M:%S")
    datetoday = date.today().strftime("%m_%d_%y")
    attendance_file = f'Attendance/Attendance-{datetoday}.csv'

    try:
        # Read the CSV file
        with open(attendance_file, 'r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
        for row in rows:
            print("Rows")
            print(len(row))

        # Find the row with the matching userid
        for i, row in enumerate(rows):
            print(row[0])
            if i == 0:  # Skip header row
                continue
            row_userid = row[0].strip()
            if len(row) >= 5 and row_userid.lower() == userid.lower():  # Check for leading/trailing whitespaces
                # Debugging output
                print("Match found for User ID:", userid)
                
                # Check if attendance is already marked
                if row[4] == '':
                    try:
                        sound_file = 'static/success.wav'
                        winsound.PlaySound(sound_file, winsound.SND_FILENAME)
                    except Exception as e:
                        print(f"Error playing sound: {e}")
                    # Update attendance to 'Present'
                    row[4] = 'Present'
                else:
                    try:
                        sound_file = 'static/failure.wav'
                        winsound.PlaySound(sound_file, winsound.SND_FILENAME)
                    except Exception as e:
                        print(f"Error playing sound: {e}")
                    print(f"{username} ({userid}) has already marked attendance today.")
                break  # Exit loop after updating attendance
            else:
                print(f"User with userid {userid} not found in the attendance file.")
    except FileNotFoundError:
        print(f"Attendance file {attendance_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    else:
        # Write the updated rows back to the CSV file
        try:
            with open(attendance_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
        except Exception as e:
            print(f"Error writing to file: {e}")

def delete_folder_with_name_contains(path, portion):
    # Iterate through all items in the directory
    for item in os.listdir(path):
        # Check if the item is a directory
        if os.path.isdir(os.path.join(path, item)):
            # Check if the portion is in the folder name
            if portion in item:
                # Delete the folder
                folder_path = os.path.join(path, item)
                # Use either os.rmdir() if you're sure the folder is empty or shutil.rmtree() to delete recursively
                # os.rmdir(folder_path)
                import shutil
                shutil.rmtree(folder_path)
                print(f"Deleted folder: {folder_path}")

def delete_entries_with_name_contains(pickle_file, portion):
    # Load the pickle file
    with open(pickle_file, 'rb') as f:
        encodings,names= pickle.load(f)
    print(f'Old:--{names}')
    print(f'Old:--{len(encodings)}')
    # Iterate through the names and encodings
    indices_to_remove = []
    for i, name in enumerate(names):
        if portion in name:
            indices_to_remove.append(i)
    print(indices_to_remove)
    # Remove entries from both lists
    for index in sorted(indices_to_remove, reverse=True):
        del names[index]
        del encodings[index]
    
    # Save the modified lists back to the pickle file
    with open(pickle_file, 'wb') as f:
        pickle.dump((encodings, names), f)
    with open(pickle_file, 'rb') as f:
        encodings, names = pickle.load(f)
    print(f"New:--{names}")
    print(f"New:--{len(encodings)}")

def delete_row_by_id(csv_file, id_value):
    # Read the CSV file and load its contents into a list of dictionaries
    rows = []
    with open(csv_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)

    # Find the index of the row with the matching ID value
    index_to_remove = None
    for i, row in enumerate(rows):
        if row['id'] == id_value:  # Assuming 'ID' is the name of the column containing IDs
            index_to_remove = i
            break

    # Remove the row with the matching ID value
    if index_to_remove is not None:
        del rows[index_to_remove]

    # Write the modified data back to the CSV file
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = rows[0].keys() if rows else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def send_email(subject, message, to_email):
    # Your email credentials
    sender_email = 'raot14693@gmail.com'
    password = 'fwio cdlx sofp ddvu'

    # Email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Connect to SMTP server (for Gmail)
        smtp_server = 'smtp.gmail.com'
        port = 587
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        
        # Login to the email account
        server.login(sender_email, password)
        
        # Send the email
        server.sendmail(sender_email, to_email, msg.as_string())
        print("Email sent successfully")
        
        # Close the connection
        server.quit()
    except Exception as e:
        print("Failed to send email:", e)

# Connect to SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS admin
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT  NOT NULL,
              password TEXT NOT NULL,
              email TEXT UNIQUE NOT NULL,
              mobile TEXT NOT NULL)''')
c.execute('''CREATE TABLE IF NOT EXISTS faculty
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT  NOT NULL,
              password TEXT NOT NULL,
              email TEXT UNIQUE NOT NULL,
              mobile TEXT NOT NULL)''')
c.execute('''CREATE TABLE IF NOT EXISTS students
             (id TEXT PRIMARY KEY NOT NULL ,
              username TEXT  NOT NULL,
              password TEXT NOT NULL,
              email TEXT UNIQUE NOT NULL,
              mobile TEXT UNIQUE NOT NULL)''')
conn.commit()
c.close()
def admin():
    conn = sqlite3.connect('users.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute the SQL query to count the number of rows in your table
    cursor.execute('SELECT COUNT(*) FROM faculty')

    # Fetch the result of the query
    fa_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM students')
    st_count=cursor.fetchone()[0]
    # Close the cursor and connection
    cursor.close()
    conn.close() 
    return fa_count,st_count

def is_authenticated():
    return 'username' in session
# Generate OTP
def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])
@app.route('/')
def home():
    try:
        if 'username' in session:
            type=session['type']
            user=session['user']
            if type=="admin":
                f,s=admin()
                n,r,li,lo,ip,l=extract_users()
                return render_template('admin_home.html',faculty=f,student=s,name=user,names=n,roles=r,login=li,logout=lo,ip=ip,l=l)
            elif type=="faculty":
                names, rolls, times, l ,p= extract_attendance()
                MESSAGE = 'Welcome back '+user
                return render_template('faculty_home.html', names=names, rolls=rolls, times=times, l=l, totalreg=totalreg(),
                                    datetoday2=datetoday2, mess=MESSAGE,name=user,present=p)
            elif type=="student":
                name=session['user']
                ate,tot,per,at=retrieve_user_data(session['username'])
                return render_template('student_home.html',user=user[1],a=ate,t=tot,p=per,attendance_data=at,name=name)  
        else:
            return render_template('home.html')
    except:
        return render_template('home.html')
@app.route('/admin_login')
def login1():
    try:
        if 'username' in session:
            type=session['type']
            if type=="admin":
                return render_template('admin_home.html')
            elif type=="faculty":
                return render_template('faculty_home.html')
            elif type=="student":
                return render_template('student_home.html')
        else:
            return render_template('admin_login.html')
    except:
        return render_template('home.html')
@app.route('/staff_login')
def login2():
    try:
        if 'username' in session:
            type=session['type']
            if type=="admin":
                return render_template('admin_home.html')
            elif type=="faculty":
                return render_template('faculty_home.html')
            elif type=="student":
                return render_template('student_home.html')
        else:
            return render_template('faculty_login.html')
    except:
        return render_template('home.html')
@app.route('/student_login')
def login3():
    try:
        if 'username' in session:
            type=session['type']
            if type=="admin":
                return render_template('success.html')
            elif type=="faculty":
                return render_template('faculty_home.html')
            elif type=="student":
                return render_template('success.html')
        else:
            return render_template('student_login.html')
    except:
        return render_template('home.html')
@app.route('/forgot',methods=['GET','POST'])
def forgot():
    try:
        type=request.form['typed']
        return render_template('forgot_pass.html',type=type)
    except:
        return render_template('home.html')
@app.route('/changed')
def changed():
    try:
        return render_template('change_pass.html')
    except:
        session.pop('username')
        session.pop('user')
        session.pop('type')
        render_template('home.html')
@app.route('/delete')
def delt():
    return render_template('delete_record.html')
@app.route('/deleted',methods=['GET', 'POST'])
def deleted():
    id=request.form['id']
    reg=id.lower()
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM students WHERE id = ?''', (reg,))
        user = c.fetchone()
        if user:
            c.execute('''DELETE FROM students WHERE id = ?''', (reg,))
            conn.commit()
            delete_folder_with_name_contains('static/faces',reg)
            delete_entries_with_name_contains('encodings.pkl', reg)
            delete_row_by_id(f'Attendance/Attendance-{datetoday}.csv',reg)
            return render_template('delete_record.html',msg="User deleted successfully ")
        else:
            return render_template('delete_record.html',err="User does not exists")
    except ValueError as e:
        return render_template('delete_record.html',err=e)
@app.route('/registera')
def registera():
    try:
        n=session['user']
        return render_template('register_a.html',name=n)
    except:
        session.pop('username')
        session.pop('user')
        session.pop('type')
        render_template('home.html')
@app.route('/registerf')
def registerf():
    try:
        n=session['user']
        return render_template('register_f.html',name=n)
    except:
        session.pop('username')
        session.pop('user')
        session.pop('type')
        render_template('home.html')
@app.route('/logout')
def logout():
    try:
        add_logout_time(session['user'])
        session.pop('username')
        session.pop('user')
        session.pop('type')
        return render_template('home.html')
    except:
        return render_template('home.html')
@app.route('/login',methods=['GET', 'POST'])
def login():
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        type=request.form['type']
        if type=="admin" or type=="faculty":
            id="1"
            email=request.form['email']
        else:
            id=request.form['email']
            email="dummy"
        password=request.form['pass']
        if type=="admin":
            c.execute('''SELECT * FROM admin WHERE email = ?''', (email,))
            user = c.fetchone()
            if user:
                # Verify password
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if user[2] == hashed_password:
                    session['username'] = user[3]
                    session['user']=user[1]
                    session['type']='admin'
                    ip_address = request.remote_addr
                    add_users_to_csv(user[1],session['type'],ip_address)
                    n,r,li,lo,ip,l=extract_users()
                    f,s=admin()
                    return render_template('admin_home.html',faculty=f,student=s,name=session['user'],names=n,roles=r,login=li,logout=lo,ip=ip,l=l) 
                else:
                    return render_template('admin_login.html',err="!..Invalid Password..!")
            else:
                return render_template('admin_login.html',err="!..User not found..!")
        elif type=="faculty":
            c.execute('''SELECT * FROM faculty WHERE email = ?''', (email,))
            user = c.fetchone()
            if user:
                # Verify password
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if user[2] == hashed_password:
                    session['username'] = user[3]
                    session['type']='faculty'
                    session['user']=user[1]
                    names,rolls,times,l,p = extract_attendance()
                    ip_address = request.remote_addr
                    name=user[1]
                    add_users_to_csv(user[1],session['type'],ip_address)
                    return render_template('faculty_home.html',names=names,rolls=rolls,times=times,l=l,totalreg=totalreg(),datetoday2=datetoday2,day=day, mess =f"Welcome {name}",name=session['user'],present=p)
                else:
                    return render_template('faculty_login.html',err="!..Invalid Password..!")
            else:
                return render_template('faculty_login.html',err="!..User not found..!")
        elif type=="student":
            c.execute('''SELECT * FROM students WHERE id = ?''', (id,))
            user = c.fetchone()
            if user:
                # Verify password
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if user[2] == hashed_password:
                    session['username'] = id
                    session['user']=user[1]
                    session['type']='student'
                    ip_address = request.remote_addr
                    add_users_to_csv(user[1],session['type'],ip_address)
                    name=session['user']
                    ate,tot,per,at=retrieve_user_data(session['username'])
                    return render_template('student_home.html',user=user[1],a=ate,t=tot,p=per,attendance_data=at,name=name)       
                else:
                    return render_template('student_login.html',err="!..Invalid Password..!")
            else:
                return render_template('student_login.html',err="!..User not found..!")
        c.close()
    except Exception as e:
        err=str(e)
        session.pop('username')
        session.pop('user')
        session.pop('type')
        return render_template('error.html',error=err)
@app.route('/change_init')
def change_init():
    try:
        return render_template('change_pass.html')
    except:
        session.pop('username')
        session.pop('user')
        session.pop('type')
        render_template('home.html')
@app.route('/altered')
def altered():
    try:
        n=session['user']
        return render_template('alter_pass.html',name=n)
    except:
        session.pop('username')
        session.pop('user')
        session.pop('type')
        render_template('home.html')
@app.route('/alter',methods=['GET', 'POST'])
def alter():
    try:
        email=session['username']
        type=session['type']
        old=request.form['password1']
        new=request.form['password2']
        if old==new:
            return render_template('alter_pass.html',err="Two Passwords must not be the same")
        else:
            if is_valid_password(new):
                conn = sqlite3.connect('users.db')
                cursor = conn.cursor()
                hash_p= hashlib.sha256(old.encode()).hexdigest()
                hash_n= hashlib.sha256(new.encode()).hexdigest()
                # Execute the SQL UPDATE statement
                if type=="admin":
                    cursor.execute('''SELECT * FROM admin WHERE email = ?''', (email,))
                    user = cursor.fetchone()
                    if user[2]==hash_p:
                        cursor.execute("UPDATE admin SET password = ? WHERE email = ?", (hash_n, email))
                        conn.commit()
                        conn.close()
                        add_logout_time(session['user'])
                        session.pop('username')
                        session.pop('user')
                        session.pop('type')
                        
                        return render_template('admin_login.html')
                    else:
                        return render_template('alter_pass.html',err="Invalid Old Password") 

                elif type=="faculty":
                    cursor.execute('''SELECT * FROM faculty WHERE email = ?''', (email,))
                    user = cursor.fetchone()
                    if user[2]==hash_p:
                        cursor.execute("UPDATE faculty SET password = ? WHERE email = ?", (hash_n, email))
                        conn.commit()
                        conn.close()
                        add_logout_time(session['user'])
                        session.pop('username')
                        session.pop('user')
                        session.pop('type')
                        return render_template('faculty_login.html')
                    else:
                        return render_template('alter_pass.html',err="Invalid Old Password") 
                elif type=="student":
                    cursor.execute('''SELECT * FROM students WHERE id = ?''', (email,))
                    user = cursor.fetchone()
                    if user[2]==hash_p:
                        cursor.execute("UPDATE students SET password = ? WHERE id = ?", (hash_n, email))
                        conn.commit()
                        conn.close()
                        add_logout_time(session['user'])
                        session.pop('username')
                        session.pop('user')
                        session.pop('type')
                        return render_template('student_login.html')
                    else:
                        return render_template('alter_pass.html',err="Invalid Old Password") 
            else:
                return render_template('alter_pass.html',err="Passwords length must be greater than 8,contains letters,numbers,special characters") 
    except:
        session.pop('username')
        session.pop('user')
        session.pop('type')
        render_template('home.html')
@app.route('/change',methods=['GET','POST'])
def change():
    try:
        email=session['username']
        type=session['type']
        pass1=request.form['password1']
        pass2=request.form['password2']
        if pass1==pass2:
            if is_valid_password(pass1):
                conn = sqlite3.connect('users.db')
                cursor = conn.cursor()
                hash_p= hashlib.sha256(pass1.encode()).hexdigest()
                # Execute the SQL UPDATE statement
                if type=="admin":
                    cursor.execute("UPDATE admin SET password = ? WHERE email = ?", (hash_p, email))
                    conn.commit()
                    conn.close()
                    return render_template('admin_login.html')
                elif type=="faculty":
                    cursor.execute("UPDATE faculty SET password = ? WHERE email = ?", (hash_p, email))
                    conn.commit()
                    conn.close()
                    return render_template('faculty_login.html')
                elif type=="student":
                    cursor.execute("UPDATE students SET password = ? WHERE id = ?", (hash_p, email))
                    conn.commit()
                    conn.close()
                    return render_template('student_login.html')
            else:
                return render_template('change_pass.html',err="Passwords length must be greater than 8,contains letters,numbers,special characters") 
        else:
            return render_template('change_pass.html',err="Passwords must be same")
    except:
        session.pop('username')
        session.pop('user')
        session.pop('type')
        render_template('home.html')
# Route for sending OTP
@app.route('/send_otp', methods=['GET', 'POST'])
def send_otp():
    try:
        if request.method == 'POST':
            email = request.form['email']
            type=request.form['type']
            session['type']=type
            session['username']=email
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            if type=="admin":
                c.execute('''SELECT * FROM admin WHERE email = ?''', (email,))
                user = c.fetchone()
                if user:
                    otp = generate_otp()
                    session['otp'] = otp
                    subject = 'FRS Verification Code'
                    message= f"Hello,\n\nHere is your One-Time Password (OTP) for account verification: {otp}.\n\n Please do not share this OTP with anyone for security reasons.\n\nThank you,\nFace Recognition Attendance System"
                    try:
                        send_email(subject, message,email)
                        return render_template('verify_otp.html')
                    except Exception as e:
                        return render_template('error.html', error=str(e))
                else:
                    return render_template('forgot_pass.html',err="!..User not found..!",type=type)
            elif type=="faculty":
                c.execute('''SELECT * FROM faculty WHERE email = ?''', (email,))
                user = c.fetchone()
                if user:
                    otp = generate_otp()
                    session['otp'] = otp
                    subject = 'FRS Verification Code'
                    message= f"Hello,\n\nHere is your One-Time Password (OTP) for account verification: {otp}.\n\n Please do not share this OTP with anyone for security reasons.\n\nThank you,\nFace Recognition Attendance System"
                    try:
                        send_email(subject, message,email)
                        return render_template('verify_otp.html')
                    except Exception as e:
                        return render_template('error.html', error=str(e))
                else:
                    return render_template('forgot_pass.html',err="!..User not found..!",type=type)
            elif type=="student":
                c.execute('''SELECT * FROM students WHERE email = ?''', (email,))
                user = c.fetchone()
                if user:
                    otp = generate_otp()
                    session['otp'] = otp
                    subject = 'FRS Verification Code'
                    message= f"Hello,\n\nHere is your One-Time Password (OTP) for account verification: {otp}.\n\n Please do not share this OTP with anyone for security reasons.\n\nThank you,\nFace Recognition Attendance System"
                    try:
                        send_email(subject, message,email)
                        return render_template('verify_otp.html')
                    except Exception as e:
                        return render_template('error.html', error=str(e))
                else:
                    return render_template('forgot_pass.html',err="!..User not found..!",type=type)
        c.close()
    except:
        session.pop('username')
        session.pop('user')
        session.pop('type')
        render_template('home.html')
        

# Route for verifying OTP
@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    try:
        if request.method == 'POST':
            type=session['type']
            otp_entered = request.form['otp']
            if otp_entered == session['otp']:
                session.pop('otp')
                return render_template('change_pass.html')    
            else:
                return render_template('verify_otp.html', error='Invalid OTP')
        return render_template('success.html')
    except:
        session.pop('username')
        session.pop('user')
        session.pop('type')
        render_template('home.html')
@app.route('/start',methods=['GET'])
def start():
    try:
        current_time = dt.datetime.now().time()

        # Define the time condition (e.g., execute the function if the current time is after 9:00 AM)
        target_time = dt.time(21, 00, 0)  # 9:00 AM

        # Check if the current time satisfies the condition
        if current_time < target_time:
            with open('encodings.pkl', 'rb') as f:
                known_encodings, known_names = pickle.load(f)
            # Initialize video capture and face recognition process
            video_capture = cv2.VideoCapture(0)
            while True:
                ret, frame = video_capture.read()

                # Convert frame to RGB format for face recognition
                # Convert frame to RGB format for face recognition
                rgb_frame = frame[:, :, ::-1]

                # Find all faces and encodings in the frame
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                # Loop through each detected face
                for face_encoding, face_location in zip(face_encodings, face_locations):
                    # Match the face encoding with the known face encodings
                    matches = face_recognition.compare_faces(known_encodings, face_encoding,tolerance=0.5)
                    name = "Unknown"
                    username="Unknown"

                    # If a match is found, get the name
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_names[first_match_index]
                        username=name.split('_')[0]
                        # Mark attendance for the recognized person
                        add_attendance(name)
                        # Play sound notification on detection (Windows)
                    

                    # Draw rectangle around the face and display name
                    top, right, bottom, left = face_location
                    if name=="Unknown":
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    else:
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                    # Display name below the face rectangle
                    font_scale = 1.0
                    font_thickness = 2
                    cv2.putText(frame,username, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX,
                                font_scale, (255, 255, 255), font_thickness)

                # Display the resulting frame
                cv2.imshow('Attendance System', frame)

                # Exit on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # Release video capture and close windows
            video_capture.release()
            cv2.destroyAllWindows()

            names, rolls, times, l,p = extract_attendance()
            MESSAGE = 'Attendence taken successfully'
            print("attendence registered")
            return render_template('faculty_home.html', names=names, rolls=rolls, times=times, l=l, totalreg=totalreg(),
                                datetoday2=datetoday2, mess=MESSAGE,name=session['user'],present=p)
        else:
            names, rolls, times, l,p = extract_attendance()
            MESSAGE = 'Attendence Timed Out'
            print("attendence timed out")
            return render_template('faculty_home.html', names=names, rolls=rolls, times=times, l=l, totalreg=totalreg(),
                                datetoday2=datetoday2, mess=MESSAGE,name=session['user'],present=p)
    except:
        session.pop('username')
        session.pop('user')
        session.pop('type')
        return render_template('home.html')
@app.route('/add',methods=['GET','POST'])
def add():
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        id=request.form['id']
        type=request.form['type']
        username=request.form['username']
        password=request.form['password']
        email=request.form['email']
        mobile=request.form['phone']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        # Insert user data into the database
        if type=="admin":
                try:
                    c.execute('''INSERT INTO admin (username, password, email, mobile)
                                VALUES (?, ?, ?, ?)''', (username, hashed_password, email, mobile))
                    conn.commit()
                    f,s=admin()
                    n,r,li,lo,ip,l=extract_users()
                    return render_template('admin_home.html',faculty=f,student=s,name=session['user'],names=n,roles=r,login=li,logout=lo,ip=ip,l=l)
                except:
                    return render_template('register_a.html',err="User Already Exists..!")
        elif type=="faculty":
            try:
                c.execute('''INSERT INTO faculty (username, password, email, mobile)
                            VALUES (?, ?, ?, ?)''', (username, hashed_password, email, mobile))
                conn.commit()
                f,s=admin()
                n,r,li,lo,ip,l=extract_users()
                return render_template('admin_home.html',faculty=f,student=s,name=session['user'])
            except:
                return render_template('register_f.html',err="User Already Exists..!")
        elif type=="student":
            try:
                c.execute('''INSERT INTO students (id,username, password, email, mobile)
                            VALUES (?,?, ?, ?, ?)''', (id,username, hashed_password, email, mobile))
                conn.commit()
                c.close()
                userimagefolder = 'static/faces/'+username+'_'+str(id)
                if not os.path.isdir(userimagefolder):
                    os.makedirs(userimagefolder)
                '''cap = cv2.VideoCapture(0)
                i,j = 0,0
                while 1:
                    _,frame = cap.read()
                    faces = extract_faces(frame)
                    for (x,y,w,h) in faces:
                        cv2.rectangle(frame,(x, y), (x+w, y+h), (255, 0, 20), 2)
                        cv2.putText(frame,f'Images Captured: {i}/10',(30,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 20),2,cv2.LINE_AA)
                        if j%10==0:
                            name = username+'_'+id+'_'+str(i)+'.jpg'
                            cv2.imwrite(userimagefolder+'/'+name,frame[y:y+h,x:x+w])
                            i+=1
                        j+=1
                    if j==100:
                        break
                    cv2.imshow('Adding new User',frame)
                    if cv2.waitKey(1)==27:
                        break
                cap.release()
                cv2.destroyAllWindows()'''
                print('Training Model')
                known_images_folder = 'static/faces'  # Replace with your actual folder path
                load_images_from_directory(known_images_folder)
                if f'Attendance-{datetoday}.csv' not in os.listdir('Attendance'):
                    export_to_csv('users.db', 'students', f'Attendance/Attendance-{datetoday}.csv')
                    add_column_to_csv(f'Attendance/Attendance-{datetoday}.csv','Attendance', '')
                
                add_row(f'Attendance/Attendance-{datetoday}.csv',id,username,email,mobile,"")
                names,rolls,times,l ,p= extract_attendance()
                if totalreg() > 0 :
                    names, rolls, times, l ,p= extract_attendance()
                    MESSAGE = 'User added Sucessfully'
                    print("message changed")
                    return render_template('faculty_home.html',names=names,rolls=rolls,times=times,l=l,totalreg=totalreg(),datetoday2=datetoday2, mess = MESSAGE,name=session['user'],present=p)
                else:
                    return render_template('faculty_home.html',names=names,rolls=rolls,times=times,l=l,totalreg=totalreg(),datetoday2=datetoday2,name=session['user'],present=p)
            except:
                names, rolls, times, l,p = extract_attendance()
                return render_template('faculty_home.html',names=names,rolls=rolls,times=times,l=l,totalreg=totalreg(),datetoday2=datetoday2,name=session['user'],err='User Already Exists',present=p)
    except:
        names, rolls, times, l = extract_attendance()
        return render_template('faculty_home.html',names=names,rolls=rolls,times=times,l=l,totalreg=totalreg(),datetoday2=datetoday2,name=session['user'],present=p)

# Run the scheduler indefinitely

if __name__ == '__main__':
    app.run(debug=True)
