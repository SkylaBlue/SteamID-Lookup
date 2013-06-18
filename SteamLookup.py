# -*- coding: cp1252 -*-
import re, sys, urllib2

"""
Copyright© 2013 Skyla Blue
All Rights Reserved
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
class cResolve:
    def __init__(self, steamID):
        self.steamID = steamID
        self.Date    = " "
        self.tList   = []
        self.pattern = "address,(.*?)<b"
        self.com     = re.compile(self.pattern)
        self.lineBar = '-' * 65

    def buildOpener(self):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        opener.addheaders = [('Referer', 'http://www.google.com/')]
        request = opener.open("http://www.google.com/search?q="+self.steamID+"&hl=en&num=2000&client=google-csbe").read()
        return request

    def printList(self, mList, steam):
        mList = list(set(mList))
        listLen = len(mList)
        
        if listLen < 1:
            print "No IP\'s found for " + steam
        if listLen > 5:
            listLen = 5
            
        print self.lineBar
        for a in range(0, listLen):
            print "Found[%i]:" % (a), mList[a] 
        print self.lineBar
        print "\nFound", listLen, "IP address(es)\n"

    def parseDate(self, dateString):
        match=re.search(r'(\d+[-/]\d+[-/]\d{2})', dateString) # Check if there was a ban date
        if match:
            DateYear = match.group(1)[-2:]
            Date = match.group(1)[:-2]+'20'+DateYear          # So you don't think we're formatting the date like Euros :D
            return Date
        else:
            Date = "Unknown"
            return Date
        if not Date:
            Date = "Unknown"
            return Date
        
    def parseResult(self):
        IPs = self.com.findall(self.buildOpener())

        if not IPs:
            print "No IP\'s found"

        else:
            for i in IPs:
                if "no IP" in i or "<a href" in i: # Just skip no IP's and ones with a lot of random bs in it
                    pass
                else:
                    foundIP = re.findall( r'[0-9]+(?:\.[0-9]+){3}', i)
                    foundDate = self.parseDate(i[4:-2])
                    Country = i[0:4].strip()
                    
                    for a in set(foundIP):
                        if a in ' '.join(self.tList):#re.search(a, ' '.join(self.tList)):
                            break
                        
                        if Country == "zz" or Country == "no" or len(Country) > 2:
                            Country = "Unknown"
                        else:
                            self.tList.append("("+Country+") " + a + " || Banned on: " + foundDate)
                        
            if ''.join(IPs).find("Player IP Addresses"):
               for i in IPs:
                    if "<wbr>" in i:
                        i.replace("<wbr>", "")
                        
                    ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', ''.join(IPs))
                    for a in set(ip):
                        if a in ' '.join(self.tList):
                            break
                        Country = "Unknown"
                        self.tList.append("IP: " + a + " || Country: " + Country)
               pass
            
            self.printList(self.tList, self.steamID)
            
            
print "Python SteamID Lookup->Version:1.1.7 - Made by Skyla Blue(5/31/2013)\n"        
def main():
    steamid = raw_input("Enter SteamID: ")
    steamid = steamid.strip()
    if not steamid.startswith("STEAM"):
        print "You must enter a SteamID!"
    else:
        cResolve(steamid).parseResult()

while True:
    main()

raw_input()
