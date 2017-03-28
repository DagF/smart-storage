# smart-storage


## killing the process
ps aux | grep "main.py"
sudo kill -9 858

#reading from acelerometer

https://www.raspberrypi.org/forums/viewtopic.php?t=22266

# RFID
https://www.parallax.com/sites/default/files/downloads/28140-28340-RFID-Reader-Documentation-v2.4.pdf
https://medium.com/@coryaspencer/using-the-parallax-serial-rfid-reader-with-the-raspberry-pi-8c948090e687#.ika8h5bwy

Format sd card
Copy noob files

Wiernig the acd
https://cdn-learn.adafruit.com/downloads/pdf/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi.pdf

Wiering the pi
https://i.stack.imgur.com/sVvsB.jpg



sudo apt-get update
sudo apt-get install python-dev
sudo apt-get install python-setuptools
sudo easy_install rpi.gpio

git clone git://gist.github.com/3151375.git




https://frillip.com/using-your-raspberry-pi-3-as-a-wifi-access-point-with-hostapd/


http://stackoverflow.com/questions/42505741/raspberrypi-as-hotspot-without-internet-accessed-via-a-domain-name

ssh pi@172.24.1.1

## ssh
https://www.raspberrypi.org/documentation/remote-access/ssh/

## static ip
https://duckduckgo.com/?q=raspberry+pi+static+ip&t=raspberrypi&ia=web

### /etc/network/interfaces
# interfaces(5) file used by ifup(8) and ifdown(8)

# Please note that this file is written to be used with dhcpcd
# For static IP, consult /etc/dhcpcd.conf and 'man dhcpcd.conf'

# Include files from /etc/network/interfaces.d:
```
auto lo
iface lo inet loopback

iface eth0 inet manual

allow-hotplug wlan0
iface wlan0 inet static
    address 192.168.0.2
    netmask 255.255.255.0
    network 192.168.0.0
    broadcast 192.168.0.255
    gateway: 192.168.0.1
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf

allow-hotplug wlan1
iface wlan1 inet manual
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
```
### /etc/wpa_supplicant/wpa_supplicant.conf
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=GB

network={
        ssid="<Network>"
        psk="<Password>"
        key_mgmt=WPA-PSK
}
```
