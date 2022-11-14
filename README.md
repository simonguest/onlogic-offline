# OnLogic FR201 Instructions

This repo contains the initial prototype files and setup instructions for our OnLogic FR201 prototype.

The FR201 is a quad-core A72 Raspberry Pi CM4 with a custom daughter board with Ethernet, USB 2.0, USB 3.0, HDMI, and a USB-C port. The device has 8GB RAM, a 32Gb eMMC and a 256Gb SATA SSD.

## Flashing the device

The device has already been flashed with Raspberry Pi OS (64bit) as per [these](https://support.onlogic.com/documentation/factor/) instructions. If you ever need to re-flash the device (e.g., if you wanted to switch to Ubuntu) this page details all of the steps required.

## ssh

SSH is enabled on all ports (both wired ethernet and WiFi). To ssh to the box while connected to the WiFi AP, connect to 192.168.4.1.

## WiFi Access Point

The device has been configured as a WiFi access point, broadcasting on the **CODEORG_OFFLINE** SSID. To change any of the details of the AP, refer to [this page](./WIFI_AP.md).

## Connecting to the Internet

You'll need a physical ethernet cable (plugged into either port) for the device to access the internet. It's not possible for a WiFi card to be AP and client mode simultaneously.

## Devices

The 32Gb eMMC (/dev/mmcblk0p2) is mounted on /. This is the default mountpoint used for the OS.

The 256Gb SSD (/dev/sda) is mounted as /mnt/sda. This contains an older docker-based repo (for testing) and the offline scripts we used for testing in the office. I've updated the /etc/fstab to automount this volume on startup.

## WiFi AP Firmware

The default WiFi firmware supports using the device as an access point, but only up to 8 concurrent connections. During the initial prototyping of this device, I found a minimal version of the firmware with less features (that we would never use) but supporting up to 19 concurrent connections.

In /lib/firmware/brcm is a symbolic link to the WiFi firmware (brcmfmac43455-sdio.bin) that points to a minimal version contained in a separate directory (../cypress/cyfmac43455-sdio-minimal.bin). If the firmware ever gets automatically updated, this symbolic link will likely need recreating.

## New systemd Services

I have created two systemd services to start the test python web server on device startup.

The web-server.service (in /etc/systemd/system) runs a basic python web server (found in /mnt/sda/offline-test/websocket/web-server.sh).

The socket-server.service (in /etc/systemd/system) runs a basic python web socket server to echo back messages to the server web page.

Both of these services are set to start on device startup.

## Code.org running in Docker on the OnLogic FR201

I did some very limited testing of the Code.org repo running in a docker repo on the device. I used my docker repo (https://github.com/simonguest/codeorg-docker-dev) to run the test.

To get CDO bound to the network interfaces, I had to adjust /dashboard/config/environments/development.rb to bind to all interfaces:

```
-  config.hosts << "localhost-studio.code.org"
-  config.hosts << "localhost.code.org"
-  config.hosts << "localhost.hourofcode.com"
-  config.hosts << "localhost.codeprojects.org"
+  # config.hosts << "localhost-studio.code.org"
+  # config.hosts << "localhost.code.org"
+  # config.hosts << "localhost.hourofcode.com"
+  # config.hosts << "localhost.codeprojects.org"
+  # config.hosts << IPAddr.new("0.0.0.0/0")
+  config.hosts = nil
```

I also had to adjust /lib/cdo.rb to serve on offline-studio.code.org:

```
-      return "localhost#{sep}#{domain}" if rack_env?(:development)
+      # return "localhost#{sep}#{domain}" if rack_env?(:development)
+      return "offline#{sep}#{domain}" if rack_env?(:development)
```

Note: These were very hacky just to get the default code.org page served on the device.

