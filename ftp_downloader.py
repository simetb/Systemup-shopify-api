from ftplib import FTP
from dotenv import load_dotenv
import os

def download_ftp_file():
    
    load_dotenv(dotenv_path='./environment/ftp.env')

    FTP_HOST = os.getenv('FTP_HOST')
    FTP_USER = os.getenv('FTP_USER')
    FTP_PASS = os.getenv('FTP_PASS')
    FTP_FILE = os.getenv('FTP_FILE')

    local_filename = "products.json" 

    ftp = FTP(FTP_HOST)

    ftp.login(user=FTP_USER, passwd=FTP_PASS)

    with open(local_filename, 'wb') as local_file:
        ftp.retrbinary("RETR " + FTP_FILE, local_file.write)

    ftp.quit()
    
    return True


if __name__ == '__main__':
    download_ftp_file()