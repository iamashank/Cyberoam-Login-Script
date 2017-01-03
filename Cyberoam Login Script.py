from __future__ import print_function
import ssl
from mechanize import Browser
import time
from Crypto.Cipher import AES
import base64
import getpass

MASTER_KEY="Some-life-long-base-key-yolo-to-use-as-life-a-encyrption-key"

def encrypt_val(clear_text):
    enc_secret = AES.new(MASTER_KEY[:32])
    tag_string = (str(clear_text) +
                  (AES.block_size -
                   len(str(clear_text)) % AES.block_size) * "\0")
    cipher_text = base64.b64encode(enc_secret.encrypt(tag_string))

    return cipher_text


def decrypt_val(cipher_text):
    dec_secret = AES.new(MASTER_KEY[:32])
    raw_decrypted = dec_secret.decrypt(base64.b64decode(cipher_text))
    clear_val = raw_decrypted.rstrip("\0")
    return clear_val

br = Browser()
br.set_handle_robots( False )
br.addheaders = [('User-agent', 'Firefox')]
url = "https://172.16.1.1:8090"         #Cyberroam IP

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

br.open(url)
password = ''
try:
    file = open('pass.txt', 'r')
    password = file.read()
    file.close()
except:
    file = open("pass.txt", "w")
    file.close()

if (not password):
        password = getpass.getpass('Enter the password:\n')
        password = encrypt_val(password)
        file = open("pass.txt", "w")
        file.write(password)
        file.close()

password = decrypt_val(password)

br.select_form( 'frmHTTPClientLogin' )
br.form['username'] = 'be1014815'       #Enter username here
br.form['password'] = password          #User password
br.submit()

response_code = ""
response_code = br.response().read()

    
i = 0
count_i = 0
while count_i != 4:
    if response_code[i] == '[':
        count_i += 1
    i += 1

while response_code[i] != ']':
    print (response_code[i],end="")
    i += 1
print ()

a = raw_input("Press Enter to Exit")
