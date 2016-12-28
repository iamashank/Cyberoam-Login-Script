from __future__ import print_function
import ssl
from mechanize import Browser
import time

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


br.select_form( 'frmHTTPClientLogin' )
br.form['username'] = 'be1014815'       #Enter username here
br.form['password'] = 'your-password-here'        #Enter password in plain-text here (I know, so much for security...)
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
