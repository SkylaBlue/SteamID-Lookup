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
        self.pattern = "%s(.*?)</span" % (self.steamID)
        self.com     = re.compile(self.pattern)
        self.lineBar = '-' * 65

    def buildOpener(self):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        opener.addheaders = [('Referer', 'http://www.google.com/')]
        request = opener.open("http://www.google.com/search?q="+self.steamID+"&hl=en&num=2000&client=google-csbe").readlines()
        return request

    # Some links are encoded, so we need to replace the encoding with it's proper ascii character
    def replace(self, inp):
        try:
            inp = inp.replace("%3F", "?").replace("%3D", "=").replace("%253D", "=").replace("%253F", "?")
            if "%26" in inp:
                inp = inp.replace("%26", "&")
                return inp
            else:
                return inp
        except Exception, e:
            print e
            return inp

    # A makeshift crawler    
    def followLink(self, inputLine):
        outlist = []
        country = ""
        link = "http://(.*?)\">"
        c = re.findall(link, inputLine)

        for l in c:
            
            # Don't want a cached version of the site
            if "googleusercontent" in l:
                pass
            
            else:
                li = self.replace(l)

                try:
                    opener = urllib2.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                    opener.addheaders = [('Referer', "http://" + li)]
                    request = opener.open("http://" + li).read()

                    try:
                        country = re.findall("/flags/(.*?)\.png", request)
                        if not country:
                            country = "??"
                        else:
                            country = country[0]
                            
                    except Exception, e:
                        print e
                        country = "??"
                    
                    foundIP = re.findall( r'[0-9]+(?:\.[0-9]+){3}', request)

                    # You can uncomment this to find the amount of times the IP has been used, it's a bit buggy though
                    #timesUsed = re.findall(r'<span>[1-9][0-9]*</span>', request)

                    for ip in foundIP:
                        #print ip
                        if ip in foundIP:
                            pass
                        else:
                            outlist.append("(%s) %s" % (country.upper(), ip)) #, time)

                    
                except Exception, e:
                    print e
                    pass

            return outlist

        
    def printList(self, mList, steam):
        mList = list(set(mList))
        listLen = len(mList)
        
        if listLen < 1:
            return "No IP\'s found for " + steam
        if listLen > 5:
            listLen = 5
            
        print "\nBanned IPs\n" + self.lineBar
        for a in range(0, listLen):
            print "Found[%i]:" % (a+1), mList[a] 
        print self.lineBar
        print "\nFound", listLen, "IP address'\n"
        

    def parseDate(self, dateString):
        match=re.search(r'(\d+[-/]\d+[-/]\d{2})', dateString) # Check if there was a ban date that used slashes
        if match:
            DateYear = match.group(1)[-2:]
            Date = match.group(1)[:-2]+"20"+DateYear
            Date = Date.replace('/', '-')
            Date = Date.split('-')

            if int(Date[0]) > 12:
                Date = "%s-%s-%s" % (Date[1], Date[0], Date[2])
            else:
                Date = "%s-%s-%s" % (Date[0], Date[1], Date[2])

            Date = ''.join(Date)
            return Date
        
        else:
            Date = "Unknown"
            return Date
        
        if not Date:
            Date = "Unknown"
            return Date
        

    def parseIPs(self, line):
        outlist = []
        try:
            foundIP = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line)
            if len(foundIP) < 1:
                return

            

            else:
                #print foundIP
                line = line.split("s,")
                foundDate = self.parseDate(' '.join(line))
                try:
                    Country = line[1][1:3].strip()
                except:
                    Country = "??"
                    
                for a in set(foundIP):
                    if a in ' '.join(outlist):#re.search(a, ' '.join(self.tList)):
                        break
                    
                    if Country == "zz" or Country == "no" or len(Country) > 2 or Country.lower() == "un":
                        Country = "??"
                    else:
                        outlist.append("("+Country+") " + a + " || Logged on: " + foundDate)
                return outlist

        except Exception, e:
            pass

    
    def parseResult(self):
        #IPs = self.com.findall(self.buildOpener())
        IPs = self.buildOpener()
        
        for i in IPs:
            if "no IP" in i: # Just skip no IP's and ones with a lot of random bs in it
                pass

                 
            else: 
                # Probably a stats page with multiple ips, try to follow the link
                # and pull IPs, if not read directly from Google
                if "Addresses" in i or "Steamids." in i or "IP Addresses." in i :
                       out = self.followLink(i)
                       ips = self.parseIPs(i)
                       if out:
                           print "\nIPs from stats site"
                           print "-----------------------------------------------------------------"
                           for ip in out:
                               print ip
                           print "-----------------------------------------------------------------"
                           
                       elif ips:
                           try:
                               print "\nIPs from stats site"
                               print "-----------------------------------------------------------------"
                               ips = self.parseIPs(i)
                               if not ips:
                                   break
                               for ip in ips:
                                   if ip == None:
                                       break
                                   print ip
                               print "-----------------------------------------------------------------" 
                           except:
                               break
                       else:
                           pass
                           
                       

                # Found a ban site, try to pull the IP and ban date, else just print IP   
                if "address," in i:
                    
                    foundIP = re.findall( r'[0-9]+(?:\.[0-9]+){3}', i)
                    if len(foundIP) < 1:
                        break
                    else:
                        i = i.split("address,")
                        foundDate = self.parseDate(' '.join(i))
                        Country = i[1][1:3].strip()
                        
                        for a in set(foundIP):
                            if a in ' '.join(self.tList):#re.search(a, ' '.join(self.tList)):
                                break
                            
                            if Country == "zz" or Country == "no" or len(Country) > 2 or Country.lower() == "un":
                                Country = "??"
                            else:
                                self.tList.append("("+Country+") " + a + " || Logged on: " + foundDate)                           
                
                        
        
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
