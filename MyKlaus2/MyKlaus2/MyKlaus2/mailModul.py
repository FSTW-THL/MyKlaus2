import zipfile
import os
import io
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import smtplib 
from MyKlaus2.config import Config

def zip_file_list(filePaths,dirpath):
    zip_file = zipfile.ZipFile(dirpath+'.zip', 'w')
    with zip_file:
    # writing each file one by one
        for file in filePaths:
         zip_file.write(file)
    return dirpath+'.zip'

def upload_file(file):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    f = open(file,"r")
    fn = os.path.basename(f.name)
    drive_file = drive.CreateFile({'title': fn })
    drive_file.SetContentFile(file)
    drive_file.Upload()
    drive_file.InsertPermission({
                        'type': 'anyone',
                        'value': 'anyone',
                        'role': 'reader'})
    return drive_file['alternateLink']

def send_mail(empfaenger,link):
    FROM = Config.MAIL_USERNAME
    TO = empfaenger
    SUBJECT = "Klausuren"
    TEXT = "Deine Klausuren findest du unter diesem Link: "+link
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    s = smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) 
    s.ehlo()
    s.starttls() 
    s.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD) 
    s.sendmail(Config.MAIL_USERNAME, empfaenger, message) 
    s.quit() 



