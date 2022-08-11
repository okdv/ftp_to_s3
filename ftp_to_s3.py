import os
import ftplib
import re
from dotenv import load_dotenv

load_dotenv()

class Credentials:
    def __init__(self, bucket_name,ftp_url, ftp_user, ftp_pass):
        self.bucket_name = bucket_name
        self.ftp_url = ftp_url
        self.ftp_user = ftp_user
        self.ftp_pass = ftp_pass

ftp_credentials = Credentials(
    os.getenv("BUCKET_NAME"),
    os.getenv("FTP_URL"),
    os.getenv("FTP_USER", "anonymous"),
    os.getenv("FTP_PASS", "anonymous"),
)

paths_str = os.getenv("GET_PATHS", "")

def parse_paths(str):
    parsed_paths = str.split(',')
    paths_arr = [path.strip() for path in parsed_paths if len(path.strip()) > 0]
    print(paths_arr)
    return paths_arr
    
def is_dir(conn, path):
    try:
        res = conn.sendcmd('MSLT {}'.format(path))
        return re.search("type=[pc]?dir", res)
    except: 
        print("File or directory does not exist")
        return None

def ftp_access():
    try:
        conn = ftplib.FTP(ftp_credentials.ftp_url)
        conn.login(ftp_credentials.ftp_user, ftp_credentials.ftp_pass)
        return conn
    except:
        print("Cannot connect to FTP")
        quit()

def ftp_download(conn, path):
    if not os.path.isfile("/tmp/{}".format(path)):
        print("Downloading {}...".format(path))
        # conn.retrbinary("RETR {}".format(path), open("/tmp/{}".format(path), 'wb').write

def resolve_paths(conn, paths):
    for path in paths:
        dir_bool = is_dir(conn,path)
        if dir_bool:
            print("Is directory")
            resolve_path(conn, path)

        elif dir_bool == False: 
            print("Begin download")
            ftp_download(conn, path)


paths = parse_paths(paths_str)
conn = ftp_access()
fp = open("test.csv", 'rb')
conn.storbinary('STOR test.csv', fp, 1024)
fp.close()
files = conn.nlst()
print(files)
resolve_paths(conn, paths)
conn.close()
