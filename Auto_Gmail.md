```bash
import smtplib
import time
import os
import codecs

listchanges=["[ending]", "[grade]", "[name]"]
file= [x.strip().split('\t') for x in codecs.open (r'F:\Garcilazo\Python\00Exercises\Letters_collecting\names.txt',"r", "utf_8").readlines()]#Your file with names, grades and endings
list_letter=[x for x in codecs.open(r"F:\Garcilazo\Python\00Exercises\Letters_collecting\Letter.txt","r","utf_8").readlines()]#Your letter template
for k in list_letter:
    newletter+=k
    
for i in file:
    if i[4]!="*":#In my list of names file, I added an extra column with an asterisk * to mark the people who were already emailed
        for h in listchanges:
            tolocal=newletter.replace(listchanges[h],i[h])#For each item, go to the letter template and change each for their value
###This part below sends the message
        gmail_user = 'garcilazo.uriel@gmail.com'  
        gmail_password = 'your_password_here'

        toaddr = "garcilazo.uriel@gmail.com" #recipient
        cc = []
        bcc = []
        message_subject = "Colecta de Salticidae en Sinaloa UBC-UNAM"
        message_text = tolocal
        message = "From: %s\r\n" % gmail_user + "To: %s\r\n" % toaddr + "CC: %s\r\n" % ",".join(cc) + "Subject: %s\r\n" % message_subject + "\r\n" + str(message_text)
        toaddrs = [toaddr] + cc + bcc
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, toaddrs, message)
        server.close()
```
