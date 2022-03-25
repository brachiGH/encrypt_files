from pathlib import Path
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = Path('')
DESKTOP_PATH = Path.home() / 'Desktop'

from datetime import date
import json
from cryptography.fernet import Fernet
from hashlib import sha512
from binascii import hexlify, unhexlify


class cipher:
    def __init__(self, password):
        self.today = str(date.today())
        self.password = sha512(password.encode('utf-8')).hexdigest()
        self.cipher = getcipher(password)
        self.data = getdata()
        self.filestoencrypt = []
    
    def get_files(self):
        folders = []
        files = []
        for folder in self.data['folders'].values():
            for file in folder['files']:
                if file['password'] == self.password:
                    files.append(file['file'])
            if len(file) != 0:
                folders.append({'date':folder['date'], 'files':files})
        return folders

    def encrypt(self):
        BASE_TOENCRYPT_DIR = DESKTOP_PATH / 'files to encrypt'
        BASE_ENCRYPT_DIR = BASE_DIR / 'encrypted files' / self.today
        getfilestoencrypt(self, BASE_TOENCRYPT_DIR)
        createdate(BASE_ENCRYPT_DIR)
        savefolder(self)

        for file in self.filestoencrypt:
            self.encryptfile(file, BASE_ENCRYPT_DIR, BASE_TOENCRYPT_DIR)
        savedata(self.data)


    def encryptfile(self, file, BASE_ENCRYPT_DIR, BASE_TOENCRYPT_DIR):
        toencrypt = Path(str(BASE_TOENCRYPT_DIR)+file).resolve()
        encrypted = Path(str(BASE_ENCRYPT_DIR)+file).resolve()
        createParentDir(encrypted)

        with open(toencrypt, 'rb') as f:
            content = f.read()

        hexValue = hexlify(content)
        cipher_text = self.cipher.encrypt(hexValue)

        with open(encrypted, 'wb') as f:
            f.write(cipher_text)
        
        print('  succufuly encrypted:  ', file)


    def  decrypt(self, filestodecrypt, date):
        BASE_DECRYPT_DIR = DESKTOP_PATH / 'decrypted files' / date
        BASE_ENCRYPT_DIR = BASE_DIR / 'encrypted files' / date

        createdate(BASE_DECRYPT_DIR)

        for file in filestodecrypt:
            self.decryptfile(file, BASE_DECRYPT_DIR, BASE_ENCRYPT_DIR)

    def decryptfile(self, file, BASE_DECRYPT_DIR, BASE_ENCRYPT_DIR):
        encrypted = Path(str(BASE_ENCRYPT_DIR)+file).resolve()
        decrypted = Path(str(BASE_DECRYPT_DIR)+file).resolve()
        createParentDir(decrypted)

        if encrypted.is_file():
            with open(encrypted, 'rb') as f:
                content = f.read()

            try:
                decrypt = self.cipher.decrypt(content)

                with open(decrypted, 'wb') as f:
                    f.write(unhexlify(decrypt))

                print('  succufuly decrypted:  ', file)
            except:
                print('  invalide cipher:  ', file)



def getcipher(password):
    defaultKey = 'xDtS2S-QnRmN5_UEh6KdSd8OwFcInQqGayudY3NmVf8='

    key = bytes(password+defaultKey[len(password):], 'utf-8')
    print(password+defaultKey[len(password):])
    return Fernet(key)

def getdata():
    data = {'folders':{}} # '{date}':{'password':'', 'date':'', 'files':[]}
    ENCRYPT_DATA_PATH = BASE_DIR / 'data/data.json'
    if ENCRYPT_DATA_PATH.is_file():
        try:
            with open(ENCRYPT_DATA_PATH, 'r') as file:
                data = json.load(file)
        except:
            pass
    return data

def savefolder(self):
    today = str(self.today)
    files = []
    for file in self.filestoencrypt:
        files.append({'file': file, 'password': self.password})
    if today in self.data['folders']:
        for file in self.data['folders'][today]['files']:
            for file2 in files:
                if file['file'] == file2['file']:
                    self.data['folders'][today]['files'].remove(file)
        for file in self.data['folders'][today]['files']:
            files.append(file)

    self.data['folders'][today] = {"date": self.today, "files": files}


def getfilestoencrypt(self, DIR):
    DIR_LIST = DIR.iterdir()
    for x in DIR_LIST:
        if x.is_dir():
            getfilestoencrypt(self, x)
        else:
            self.filestoencrypt.append(str(x).replace(str(DESKTOP_PATH / 'files to encrypt'), ''))

def createdate(DIR):
    print(DIR, '\n')
    if not DIR.is_dir():
        DIR.mkdir(mode=511, parents=False, exist_ok=False)

def createParentDir(DIR):
    DIR = DIR.parent
    if not DIR.is_dir():
        DIR.mkdir(mode=511, parents=True, exist_ok=False)

def savedata(data):
    ENCRYPT_DATA_PATH = BASE_DIR / 'data/data.json'
    with open(ENCRYPT_DATA_PATH, 'w') as file:
        json.dump(data, file)

def inputgetint(msg, range_=False):
    while True:
        x = input(msg)

        if (x.replace('-', '')).isdigit():
            if range_:
                if int(x) in range_:
                    return int(x)
                else:
                    print('Must enter a number between {} and {}'.format(min(range_), max(range_)))
            else:
                return int(x)
        print('Must enter a number!')

def inputgetmultipleint(msg, range_=False):
    while True:
        n = input(msg)
        
        r = []
        for x in n.split(' '):
            if (x.replace('-', '')).isdigit():
                if range_:
                    if int(x) in range_:
                        r.append(int(x))
                    else:
                        print('Must enter a number between {} and {}'.format(min(range_), max(range_)))
                else:
                    r.append(int(x))
            else:
                print('Must enter a number!')
        return r

