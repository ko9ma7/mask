import schedule
import time
#날짜
import datetime

from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
#날짜
import datetime
#파일 업로드
import os
#json 파싱
import json

import subprocess
import smtplib
from email.mime.text import MIMEText


def email():
        
    # Change to your own account information
    # Account Information
    #to = ['rosijin@naver.com','pyj628@naver.com','ove16@naver.com','mmx5@nate.com','fatzzin@naver.com','bluegury2@naver.com','kty8305@naver.com'] # Email to send to.
    to = ['rosijin@naver.com'] # Email to send to.
    gmail_user = 'retailtechtf@gmail.com' # Email to send from. (MUST BE GMAIL)
    gmail_password = 'mzivecjwxzedfmix' # Gmail password.
    smtpserver = smtplib.SMTP('smtp.gmail.com', 587) # Server to use.



    smtpserver.ehlo()  # Says 'hello' to the server
    smtpserver.starttls()  # Start TLS encryption
    smtpserver.ehlo()
    smtpserver.login(gmail_user, gmail_password)  # Log in to server
    today = datetime.date.today()  # Get current time/date

    arg='ip route list'  # Linux command to retrieve ip addresses.
    # Runs 'arg' in a 'hidden terminal'.
    p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
    data = p.communicate()  # Get data from 'p terminal'.

    #print(data)

    # Split IP text block into three, and divide the two containing IPs into words.
    ip_lines = data[0].splitlines()
    split_line_a = ip_lines[1].split()
    #split_line_b = ip_lines[2].split()
    #print("split_line_a:", split_line_a)

    # con_type variables for the message text. ex) 'ethernet', 'wifi', etc.
    #ip_type_a = connect_type(split_line_a)
    #ip_type_b = connect_type(split_line_b)

    """Because the text 'src' is always followed by an ip address,
    we can use the 'index' function to find 'src' and add one to
    get the index position of our ip.
    """
    #ipaddr_a = split_line_a[split_line_a.index('src')+1]
    #ipaddr_b = split_line_b[split_line_b.index('src')+1]

    # Creates a sentence for each ip address.
    my_ip_a = 'http://www.welkeepsmall.com/m/product_list.html?type=X&xcode=023'
    #my_ip_b = 'Your %s ip is %s' % (ip_type_b, ipaddr_b)
    #ddb_pk = store_id+"/"+rack_no+"/"+inventory_no
    # Creates the text, subject, 'from', and 'to' of the message.
    msg = MIMEText(my_ip_a)
    msg['Subject'] = '[welkeepsmall 마스크 재고생김' 

    msg['From'] = gmail_user

    for toUser in to:
        msg['To'] = toUser
        # Sends the message
        smtpserver.sendmail(gmail_user, [toUser], msg.as_string())
    # Closes the smtp server.
    smtpserver.quit()



def job():

    try:    
        print('url try')
        url = "http://www.welkeepsmall.com/shop/shopbrand.html?type=M&xcode=023"
        #print('url try2')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('disable-gpu')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        #print('url driver1')
        driver = webdriver.Chrome('/home/newface/mask/chromedriver', chrome_options=options)
        #print('url driver2')
        #driver = webdriver.Chrome('C:/Users/Administrator/PycharmProjects/broccoli/chromedriver.exe')
        driver.implicitly_wait(10)
        #print('url driver3')
        driver.get(url)
        #print('try soup',url)    
        soup = BeautifulSoup(driver.page_source, "html.parser")
        #print(soup)   
    except:
        
        print('except==============================>')
        pass
    else:      
        print('no except')
        a = 0
        for idx, tag in enumerate(soup.select('.soldout'), 1):
            a = a+1

        print('soldout',a)
        driver.quit()  
        if 5 < a < 24:
            print("email",a)
            email()
            
        else:
            print("wait",a)



#      
        
#schedule.every(1).minutes.do(job) #

#while True:
#    schedule.run_pending()
#    time.sleep(5)

schedule.every(0.5).minutes.do(job) #면세점

while True:
    schedule.run_pending()
    time.sleep(5)
