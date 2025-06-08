# Keyboard HID API Server (Tentative Name)

## Installation Steps

1. Click BOOTSEL and plug in device

2. Upload flash_nuke.uf2 before uploading the uf2 you really want to use
</br>https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html#resetting-flash-memory

3. Download MicroPython .uf2 file
<br />URL: https://circuitpython.org/board/raspberry_pi_pico_w/

4. Download library for HID, HTTP Server, and Requests.
<br />Download ZIP from URL below
<br />URL: https://circuitpython.org/libraries
<br /><b>MUST DOWNLOAD SAME VERSION IN STEP 1</b>

5. Upload MicroPython .uf2 to the Pico Storage
<br />Create lib folder and upload the following folders and file:
<br /></t></t>a. <b>adafruit_httpserver</b> folder
<br /></t></t>b. <b>adafruit_requests</b> folder
<br /></t></t>c. <b>adafruit_requests.mpy</b> file

6. Download Python Scripts for the HID Api Server
<br />Download the following files:
<br /></t></t>a. <b>boot.py</b> 
<br /></t></t>b. <b>code.py</b> 
<br /></t></t>c. <b>secrets.py</b>

7. Update secrets.py
<br />Please update the SSID and Password.

8. Upload python scripts in Pico Storage
<br />Upload the 3 files and in the Pico Storage

## Endpoint Guide
| Endpoint | HTTP Request Method | Description |
| ----- | ----- | ----- |
| :5000/set | POST | This is used to SET the string that the 'keyboard' will type. When using /set, make sure that there is a 'text' request body. |
| :5000/print |  | This is used to type in the saved string. |
| :5000/serial |  | This is used to print the saved string in serial monitor. The baud rate is 115200. |