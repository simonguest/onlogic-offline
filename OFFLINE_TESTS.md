# Offline Test

## Simple Page

* Mount the SSD: 

`sudo mount -t ext4 /dev/sda /mnt/sda`
* Navigate to the offline test directory:

`cd /mnt/sda/offline-test/simple`
* Start the python server:

`python -m http.server`
* Browse to http://192.168.4.1:8000 on Chromebook

## Websocket Test

* Navigate to the websocket test directory:

`cd /mnt/sda/offline-test/websocket`



