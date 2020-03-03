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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def email(a,b):
        
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
    my_ip_a = 'https://www.hyundaihmall.com/front/pde/search.do?searchTerm=%EB%A7%88%EC%8A%A4%ED%81%AC%20KF80'
    #my_ip_b = 'Your %s ip is %s' % (ip_type_b, ipaddr_b)
    #ddb_pk = store_id+"/"+rack_no+"/"+inventory_no
    # Creates the text, subject, 'from', and 'to' of the message.
    msg = MIMEText(my_ip_a)
    msg['Subject'] = 'Hmall [마스크 KF90] 검색 결과가 바뀜 : '+ str(b) + '개 ->'+ str(a) + '개' 

    msg['From'] = gmail_user

    for toUser in to:
        msg['To'] = toUser
        # Sends the message
        smtpserver.sendmail(gmail_user, [toUser], msg.as_string())
    # Closes the smtp server.
    smtpserver.quit()



def job():
    

    try:    

        with open('count2.json', encoding="utf-8") as jsonfile:
            data = json.load(jsonfile)
        print("현재 판매수:",data[0]["count"])
        MASK_COUNT = data[0]["count"]


        print('url try')

        url = "https://www.hyundaihmall.com/front/pde/search.do?searchTerm=%EB%A7%88%EC%8A%A4%ED%81%AC%20KF80"
        #print('url try2')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('disable-gpu')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')

        driver = webdriver.Chrome('/home/mask/chromedriver', chrome_options=options)

        driver.implicitly_wait(10)

        driver.get(url)
        print("1")
        _ = WebDriverWait(driver, 13).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="footer"]/div[2]/div[1]/img')))

        print("2")

        soup = BeautifulSoup(driver.page_source, "html.parser")
        #print(soup)   
    except:
        
        print('except==============================>')
        pass
    else:      
        print('no except')
        a = 0
        for idx, tag in enumerate(soup.select('.pl_main_category_tabcontents'), 1):
            #print('pl_main_category_tabcontents',tag)
            for idx, xtag in enumerate(tag.select('.pl_itemlist_img'), 1):
                a = a+1
                
        driver.quit()
        print("a",a)  
        print("MASK_COUNT",MASK_COUNT)  
        if  str(a) == str(MASK_COUNT):
            print("pass",a)
            
            
        else:
            print("email",a)
            NEW_MASK = []
            NEW_MASK.append({'count':str(a)})
            
            print(NEW_MASK)
            #이메일 발송
            email(a,MASK_COUNT)

            #재고 변경
            folder = '/home/mask/'
            filepath = os.path.join(folder, "count2")
            
            with open(filepath+'.json','w',encoding="utf-8") as make_file:
                json.dump(NEW_MASK, make_file, ensure_ascii=False, indent="\t") 


#if __name__ == "__main__":
#    job()
    
schedule.every(0.5).minutes.do(job) #

while True:
    schedule.run_pending()
    time.sleep(5)
