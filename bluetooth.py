# encoding: utf-8
import time
import urllib.request
import bluetooth

previous_addr=[]
while(1):
    print("start scanning...")
    try:
        nearby_devices = bluetooth.discover_devices(duration=4, lookup_names=True, flush_cache=True, lookup_class=False)
        for addr, name in nearby_devices:
            try:
                print("  %s - %s" % (addr, name))
                #filter unknown bluetooth user
                if len(name)==0:  
                    continue
                    
                if addr in previous_addr:
                    #should change the IP address
                    url = "http://localhost:3000/bluetooth?bluetooth_id=" + addr    
                    request = urllib.request.Request(url)
                    response = urllib.request.urlopen(request).read()
                    previous_addr.remove(addr)
                    if response[:7].decode('utf-8') == "success":
                        time.sleep(5)
                        break
                    continue
                previous_addr.append(addr)
            except UnicodeEncodeError:
                print("  %s - %s" % (addr, name.encode('utf-8', 'replace')))
        
        if len(previous_addr) > 10:
            previous_addr.pop(0)

    except:
        print("error")
