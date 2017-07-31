from ftplib import FTP
import xml.etree.ElementTree as ET
import sys
import threading
import time
import re

class FTPScanner(object):
    
    found_servers = []
    hosts = []
    threads = []
    
    def __init__(self, xmlfile):
        self.xmlfile = xmlfile
        tree = ET.parse(xmlfile)
        pattern = './host/address/../address[@addrtype="ipv4"]'    
        self.hosts = list(i.get('addr') for i in tree.findall(pattern))
        

    def _valadate_ip(self, ip):
        return re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip)
        
        
    def _worker(self):
        while self.hosts: 
            try:
                if not self.hosts:
                    sys.exit(0)
                host = self.hosts.pop()
                ftp = FTP(host)
                ftp.login()
                #ftp.retrlines('LIST')
                self.found_servers.append(host)
                ftp.quit()
                print host
                sys.stdout.flush()
            except KeyboardInterrupt:
                sys.exit(0)
            except Exception as e:
                #print e
                continue

        
    def run(self, n_threads):
        
        for i in range(n_threads):
            try:
                t = threading.Thread(target=self._worker)
                t.daemon=True
                t.start()
            except KeyboardInterrupt:
                sys.exit(0)
                
        self._worker()
        
        while 1:
            try:
                time.sleep(5)
                if not self.hosts:
                    sys.exit(0)
                #print "{} Hosts found.".format(len(FOUND))
                #print "{} Hosts left to scan.".format(len(HOSTS))
            except KeyboardInterrupt:
                sys.exit(0)


scanner = FTPScanner('ftp-servers.xml')
scanner.run(200)
