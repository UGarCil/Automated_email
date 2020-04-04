import smtplib
import time
import os
import codecs
from os.path import join as jn
import argparse as args
import pandas as pd

### call argparse and create the dictionary prmts ###
parser = args.ArgumentParser()
parser.add_argument("prmts", help='''The script accepts two arguments: the name of the folder that contains the student's folders and a second argument: status, send_all For example: python Send_emails.py week11 status   sends an emil to all students on the status of their submission. If the folder with their name for week11 contains a file, then it sends the student a confirmation, if the folder is empty then sends email asking for explanation or requesting a new copy of the file
''',nargs=2)
armnts = parser.parse_args()
week = armnts.prmts[0]

''' This function takes the message, recipient and quiz number and send
    the message to the respective emails'''
def send_message(message,recipient,subjctname):
    gmail_user = 'garcilazo.uriel@gmail.com'  
    gmail_password = '' #yourpassword for gmail
    toaddr = recipient #recipient
    cc = []
    bcc = []
    message_subject = subjctname
    message_text = message
    message = "From: %s\r\n" % gmail_user + "To: %s\r\n" % toaddr + "CC: %s\r\n" % ",".join(cc) + "Subject: %s\r\n" % message_subject + "\r\n" + str(message_text)
    toaddrs = [toaddr] + cc + bcc
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(gmail_user, toaddrs, message)
    server.close()

####Manage directories. working_folder will contain the directory where the script is running from and that also contains
#### important txt files with the messages to send and students lists
# os.chdir(r"D:\Garcilazo\articles hmwrk\00_Doctorado\Laboral_Experience\Jobs\TA\BIOL_234\00_online_TA\Filtering_folders_students_gaveAss") #This gets uncommented when the script editor is currently in a different working directory

###Setting the directories
working_folder= os.getcwd()
print(working_folder)
chdir= os.getcwd().split('\\')[:len(os.getcwd().split('\\'))-1]
    ### Go up one directory and enter the folder that contains the list of students for a particular week
namenewdir= ''
for each in chdir:
    namenewdir+= each+'\\'
namenewdir += week
list_folders=(os.listdir(namenewdir)) #A list of the folders contained within the folder with the name specified when running the script

if armnts.prmts[1] == 'status':
    ### put the letter that will be sent to students that submitted something on time into memory ####
    with open(jn(working_folder,'Letter_received.txt'),'r') as letter:
        letterreceived = ''
        letter=letter.readlines()
        for x in letter:
            letterreceived+=x
        letterreceived = letterreceived.replace('[weeknumber]',week)

    ### put the letter that will be sent to students that did not submit something on time into memory ####
    with open(jn(working_folder,'Letter_notreceived.txt'),'r') as letter:
        letter_not_received = ''
        letter=letter.readlines()
        for x in letter:
            letter_not_received+=x
        letter_not_received = letter_not_received.replace('[weeknumber]',week)
    ### read the names, emails and messaging status into memory through a pandas dataframe
    df=pd.read_csv(jn(working_folder,'names.txt'), delimiter = '\t')
    df = df.fillna('')

    for i,j in df.iterrows():
        if 'sent_' not in j['status_message']:
            print('working on the folder/student: '+ j['folder_name'])
            if j['folder_name'] in list_folders and 'ZZ_'+j['folder_name'] not in list_folders:
                lettertosend =letterreceived.replace('[name]',j['pref_name'])
                j['status_message']='sent confirmation'
                df['status_message'][i]= 'sent_confirmation'
                if j['email']!='':
                    send_message(lettertosend,j['email'],'Confirmation on your submission for %s'%week)
                else:
                    df['status_message'][i]= 'notsent_email_notfound_studentSUBMITTED'
            elif 'ZZ_'+j['folder_name'] in list_folders:
                lettertosend = letter_not_received.replace('[name]',j['pref_name'])
                # df.replace(df.iloc[i]['status_message'],'sent_request',inplace=True)
                df['status_message'][i]= 'sent_request'
                if j['email']!='':
                    send_message(lettertosend,j['email'],'Further action is needed regarding your submission for %s'%week)
                else:
                    df['status_message'][i]= 'notsent_email_notfound_studentDIDNTSUBMIT'
            else:
                df['status_message'][i]= 'notsent_student_notfound'
        else:
            pass

    ###finally save the file with the updated status of the messaging
    print(df)
    df.to_csv('names.txt', sep='\t', index= False)
######  If the flag taken from argparse says --send_all, then the user wants to send an email to every student. We need to load the student name into a pandas dataframe, load the preloaded message into memory and send the message
elif armnts.prmts[1] == 'send_all':
    ### read the names, emails and messaging status into memory through a pandas dataframe
    df=pd.read_csv(jn(working_folder,'names.txt'), delimiter = '\t')
    df = df.fillna('') #Fill the empty cells with '' instead of the super annoying nan that is float type but you can't do anything with it when dealing with text

    ### put the letter that will be sent to students that submitted something on time into memory ####
    with open(jn(working_folder,'Letter_everyone.txt'),'r') as letter:
        lettereveryone = ''
        letter=letter.readlines()
        for x in letter:
            lettereveryone+=x
        lettereveryone=lettereveryone.replace('[weeknumber]',week)

    print('sending the preloaded message "Letter_everyone.txt" to all the contacts:')
    for i,j in df.iterrows():
        print('working on the folder/student: '+ j['folder_name'])
        if j['email'] !='':
            send_message(lettereveryone,j['email'],'Scores for %s posted on canvas'%week)
        else:
            pass
