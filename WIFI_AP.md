# WiFi Setup

1. Install dnsmasq and hostapd

```sudo apt install dnsmaq hostapd```
```sudo systemctl stop dnsmasq```
```sudo systemctl stop hostapd```

2. Configure static IP on the box

Add the following to /etc/dhcpcd.conf

```
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
```

3. Configure DHCP server

Restart the dhcp daemon:

```sudo service dhcpcd restart```

Add the DHCP range to /etc/dnsmasq.conf:

```dhcp-range=192.168.4.2,192.168.4.100,255.255.255.0,24h```

And map a domain name to the host serving the content:

```address=/offline.code.org/192.168.4.1```

Start the dnsmasq service

```sudo systemctl start dnsmasq```

4. Configure the host access point

Create /etc/hostapd/hostapd.conf file. Add the following:

```
country_code=US
interface=wlan0
ssid=CODEORG
channel=9
auth_algs=1
wpa=2
wpa_passphrase=[PASSWORD]
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP CCMP
rsn_pairwise=CCMP
```

In /etc/default/hostapd, set DAEMON_CONF:

```DAEMON_CONF="/etc/hostapd/hostapd.conf"```

5. Start the wireless AP

```
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
```

Disable rfkill to unblock the Wifi:

```sudo rfkill unblock wifi```

Reboot and the wireless AP should be visible!
