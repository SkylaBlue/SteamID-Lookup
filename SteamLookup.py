import re, sys, urllib2

class cResolve:
    def __init__(self, steamID):
        self.steamID = steamID
        self.Date    = " "
        self.tList   = []
        self.pattern = "address,(.*?). Banlength,"
        self.com     = re.compile(self.pattern)
        self.lineBar = '-' * 65
    
    # We actually have to build a request, because Google won't reply otherwise
    def buildOpener(self):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        opener.addheaders = [('Referer', 'http://www.google.com/')]
        request = opener.open("http://www.google.com/search?q="+self.steamID+"&hl=en&num=2000&client=google-csbe").read()
        return request

    # Print out the found IPs, and give a nice statistic    
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
    
    # Since there are two possible date formats, I decided to just put this in a method and call it
    def parseDate(self, dateString):
        match=re.search(r'(\d+/\d+/\d+)', dateString) # Check if there was a ban date that used slashes
        if match:
            DateYear = match.group(1)[-2:]
            Date = match.group(1)[:-2]+"20"+DateYear
            Date = Date.replace('/', '-')
            return Date
        else:
            try:
                match=re.search(r'(\d+-\d+-\d+)', dateString) # Check if the date used -'s
                DateYear = match.group(1)[-2:]
                Date = match.group(1)[:-2]+"20"+DateYear
                return Date
            except:
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
                    foundIP = i[4:-28].lstrip().replace(". <br>", "")
                    foundIP = ''.join(set(foundIP))
                    
                    if not r'[0-9]+(?:\.[0-9]+){3}' in foundIP or '.' not in foundIP: # Only found part of an IP, or no IP at all
                        break
                    
                    if ("IP: " + ''.join(foundIP) in tList):  # Make sure there are no dupes
                        pass
                    
                    foundDate = self.parseDate(i[4:-2])
                    if i[0:4].strip() == "zz" or i[0:4].strip() == "no" or len(i[0:4].strip()) > 2: # See if we can find a country for the IP
                        Country = "Unknown"
                        self.tList.append("IP: " + foundIP + " || Banned on: " + foundDate + " || Country: " + Country)
                    else:
                        Country = i[0:4].lstrip()
                        self.tList.append("IP: " + foundIP + " || Banned on: " + foundDate + " || Country: " + Country)

            # If we can't find Banlength in the request
            if ''.join(IPs).find("<b>..."):
                for i in IPs:
                    ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', ''.join(IPs)) 
                    for a in set(ip):
                        if ("IP: " + a + " || Country: ") in ''.join(self.tList) or ("IP: " + a) in ''.join(self.tList):
                            break
                        if i[0:4].strip() == "zz" or i[0:4].strip() == "no" or len(i[0:4].strip()) > 2:
                            Country = "Unknown"
                            self.tList.append("IP: " + a + " || Country: " + Country)
                        else:
                            Country = i[0:4].lstrip()
                            self.tList.append("IP: " + a + " || Country: " + Country)
                pass
            
            # This is what makes mine unique. If we find IP addresses on a stats site, we will pull these as well
            if ''.join(IPs).find("Player IP Addresses"):
               for i in IPs:
                    if "<wbr>" in i:
                        i.replace("<wbr>", "")
                        
                    ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', ''.join(IPs))
                    for a in set(ip):
                        if ("IP: " + a + " || Country: ") in ''.join(self.tList) or ("IP: " + a) in ''.join(self.tList):
                            break
                        Country = "Unknown"
                        self.tList.append("IP: " + a + " || Country: " + Country)
               pass
            
            self.printList(self.tList, self.steamID)

print "Python Steam Resolver->Version:1.6 - Made by Skyla Blue\n" # This thing has undergone many changes the past couple weeks       
def main():
    steamid = raw_input("Enter SteamID: ")
    if not steamid.strip().startswith("STEAM"): # This is actually case sensitive, so don't complain to me
        print "You must enter a SteamID!"
    else:
        cResolve(steamid).parseResult()

while True:
    main()

raw_input()
