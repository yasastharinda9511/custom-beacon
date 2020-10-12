from scapy.all import *
from threading import Thread
import pandas
import time
import os

# initialize the networks dataframe that will contain all access points nearby
networks = pandas.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Crypto"])
# set the index BSSID (MAC address of the AP)
networks.set_index("BSSID", inplace=True)

def callback(packet):
    dot11elt=packet.getlayer(Dot11Elt)
#    print(packet)
    try:
        if(packet.haslayer(Dot11Elt)):
            print("time",time.time()),
            print(packet[Dot11Elt][Dot11EltVendorSpecific].info)
    except:
        print("currupted")
    if packet.haslayer(Dot11Beacon):
        # extract the MAC address of the network
        bssid = packet[Dot11].addr2
        # get the name of it
        #print(packet[Dot11Elt])
        ssid = packet[Dot11Elt].info.decode()
        try:
            dbm_signal = packet.dBm_AntSignal
        except:
            dbm_signal = "N/A"
        # extract network stats
        stats = packet[Dot11Beacon].network_stats()
        # get the channel of the AP
        channel = packet[RadioTap].Channel
        
        #channel=packet[Dot11Elt][1].info
        #channel=int(channel.encode('hex'),16)
        
        # get the crypto
        crypto = stats.get("crypto")
        networks.loc[bssid] = (ssid, dbm_signal, channel, crypto)

def print_all():
    while True:
        #os.system("clear")
        print(networks)
        time.sleep(0.1)


def change_channel():
    ch = 1
    while True:
        os.system("sudo iwconfig {interface} channel {ch}")
#        #\switch channel from 1 to 14 each 0.5s
#        ch = ch % 14 + 1
        time.sleep(2)


if __name__ == "__main__":
    
    # interface name, check using iwconfig
    interface = "wlan1mon"
    #change_channel()
     #start the thread that prints all the networks
    printer = Thread(target=print_all)
    printer.daemon = True
    printer.start()
    # start the channel changer
    channel_changer = Thread(target=change_channel)
    channel_changer.daemon = True
    channel_changer.start()
    # start sniffing
    sniff(prn=callback, iface=interface)



