from __future__ import absolute_import, print_function
import itertools
from threading import Thread, Event
import os
import re
import subprocess
import time
import types
import random

from scapy.all import *

sender_mac="11:11:11:11:11:cc"
ve= str(200)
ssid="Pakaya"
dot11=Dot11(type=0,subtype=8,addr1="ff:ff:ff:ff:ff:ff",addr2=sender_mac,addr3=sender_mac)
beacon = Dot11Beacon()
vendor_elements=Dot11Elt(ID=221,info=ve,len=len(ve))
essid = Dot11Elt(ID="SSID", info=ssid, len=len(ssid))
x =RadioTap()/dot11/beacon/essid/vendor_elements

#frame=RadioTap()
def sendspeed(inter=0, loop=0, iface=None, iface_hint=None,socket=None,count=None, verbose=None, realtime=None, return_packets=False, *args, **kargs):  # noqa: E501
    global x
    global ve
    if iface is None and iface_hint is not None and socket is None:
        iface = conf.route.route(iface_hint)[0]
    need_closing = socket is None
    s = socket or conf.L2socket(iface=iface, *args, **kargs)

    if isinstance(x, str):
        x = conf.raw_layer(load=x)
    if not isinstance(x, Gen):
        x = SetGen(x)
    if verbose is None:
        verbose = conf.verb
    n = 0
    if count is not None:
        loop = -count
    elif not loop:
        loop = -1
    if return_packets:
        sent_packets = PacketList()
    try:
        while loop:
            dt0 = None
            print(time.time())
            print(ve)
            for p in x:
                if realtime:
                    ct = time.time()
                    if dt0:
                        st = dt0 + float(p.time) - ct
                        if st > 0:
                            time.sleep(st)
                    else:
                        dt0 = ct - float(p.time)
                s.send(p)
                if return_packets:
                    sent_packets.append(p)
                n += 1
                if verbose:
                    os.write(1, b".")
                time.sleep(inter)
            if loop < 0:
                loop += 1
    except KeyboardInterrupt:
        pass
    if need_closing:
        s.close()
    if verbose:
        print("\nSent %i packets." % n)
    if return_packets:
        return sent_packets

def createframe():
    global x
    global ve
    global ssid
    global sender_mac
    
    while(1):
        #sender_mac= "11:11:11:11:11:cc"
        ve=str(hex(random.randint(1,1000000)))
        #ssid="Pakaya"
        dot11=Dot11(type=0,subtype=8,addr1="ff:ff:ff:ff:ff:ff",addr2=sender_mac,addr3=sender_mac)
        beacon = Dot11Beacon()
        vendor_elements=Dot11Elt(ID=221,info=ve,len=len(ve))
        essid = Dot11Elt(ID="SSID", info=ssid, len=len(ssid))
        x = RadioTap()/dot11/beacon/essid/vendor_elements
        time.sleep(0.1)

if __name__ == "__main__":
    iface = "mon1"
    os.system("sudo iwconfig mon1 channel 1")
    time.sleep(1.5)
    creator= Thread(target=createframe)
    creator.start()
    beacon= Thread(target=sendspeed,args=(0.1,1,"mon1"))
    beacon.start()
    #sendspeed(0.1,1,iface)


