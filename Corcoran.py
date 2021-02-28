#!/usr/bin/python3
import re
import os
from html import unescape
import csv
from natsort import natsorted # pip install natsort

dir='C:\\Users\\ahale\\Documents\\Corcoran\\'
regionName = 'nyc'
#regionName = 'westchester'
#regionName = 'phoenix-scottsdale'

# wget --restrict-file-names=nocontrol -O phoenix-scottsdale.html https://www.corcoran.com/phoenix-scottsdale-real-estate/agents?pageSize=36&page=200&append=true

if False:
    with open(dir+regionName+'.html', 'r', encoding="UTF-8") as f:
        urls = re.findall(r'<a href="(/[a-z-]*/agents/.*?)"', f.read())
        with open(dir+regionName+'-urls.txt', 'w', encoding="UTF-8") as urlFile:
            urlFile.write('\nhttps://www.corcoran.com'.join([""]+urls)[1:])
    print('wget --no-clobber --tries=1 --wait=0.5 --restrict-file-names=nocontrol --input-file=../'+regionName+'-urls.txt')
else:
    filesList = natsorted(os.listdir(dir+regionName))
    print(filesList[0])
    agentDict = {}
    for fileName in filesList:
        with open(dir+regionName+'\\'+fileName, 'r', encoding="UTF-8") as f:
    #        print(fileName)
            htmlText = f.read()
            names = re.findall(r'<h1 class="Heading__H1-sc-19hes1t-0 AEmcX">(.*?)</h1>', htmlText, flags=re.IGNORECASE)
            emails = re.findall(r'<a href="mailto:(.*?.com)"', htmlText)
            emails.remove('info@corcoran.com')
            if len(emails) > 1 or not fileName.isdigit():
                names += re.findall(r'<div class="PartnershipTeamMembers__AgentNameText-sc-1iiojea-3 dWZBDe">(.*?)</div>', htmlText)
    #            print(names, emails)
            if len(names) == len(emails)+1:
                names = names[1:]
            if len(emails) != len(names) or (len(names) and any(substring in names[0] for substring in ['The ', 'Team', ' And ', ' and '])):
                print(fileName)
                print(names)
                print(emails)
                raise ValueError
            for i in range(len(emails)):
                agentDict[emails[i]] = unescape(names[i]).split(' ', maxsplit=1)

    print('writing csv')
    with open(dir+regionName+'.csv', 'w', newline='\n', encoding="UTF-8") as f:
        writer = csv.writer(f)
        for email, fullName in agentDict.items():
    #        print([email]+fullName)
            writer.writerow([email]+fullName)

    # daja-gonzalez/19282