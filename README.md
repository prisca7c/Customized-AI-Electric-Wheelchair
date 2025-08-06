# Customized-AI-Electric-Wheelchair

>PRISCA CHIEN | U0741Q95Y02
>
>July 27 2025
---

Manual wheelchair turned electric! This wheelchair uses electronic components such as modules and a PCB to make this wheelchair much for user interactive (and helps make life easier when you can't walk). 
I built this custom wheelchair because electric wheelchairs cost too much. Also it would be a great gift to my grandpa as he has Parkinson's disease. It has most of the functions on a regular wheelchair (motors, sound, speed, SOS, etc) AND I will be using AI as a healthcare tool in this project. 

---

## Full 3D Model of Wheelchair with Electronics (will not have those cuffs IRL 💀)
![img](https://hc-cdn.hel1.your-objectstorage.com/s/v3/166f4aef03582ae01d89af806c910cd2c8c8cbac_screenshot_2025-08-06_at_12.11.10___pm.png)
## Control Panel and Wiring through Armrest
![img](https://hc-cdn.hel1.your-objectstorage.com/s/v3/e304be568c29bdc4a652c7d5ae69012f8eb845de_screenshot_2025-08-06_at_12.06.34___pm.png)
## Walker Handle and Lock Mechanism (my actual wheelchair can pull down the backrest)
![img](https://hc-cdn.hel1.your-objectstorage.com/s/v3/5c77c485590658636347bab8060a6aa8834254e4_screenshot_2025-08-06_at_12.06.42___pm.png)
## PCB Walls and Battery Box will be connected via straps to the 4 bars of the wheelchair legs
![img](https://hc-cdn.hel1.your-objectstorage.com/s/v3/9ef42af1dc72892254d0cdadde1c66c3e4e380e8_screenshot_2025-08-06_at_12.07.19___pm.png)
## PCB Protection (elevated so I can cool it easily and also connect heatsinks and thermal pads and stuff. ALso the walls are connected with straps to legs of wheelchair)
![img](https://hc-cdn.hel1.your-objectstorage.com/s/v3/807179f9a7847059bade0cff423d6ac2a8ea9139_screenshot_2025-08-01_at_12.14.26___am.png)
## PCB Schematic
![img](https://hc-cdn.hel1.your-objectstorage.com/s/v3/db5fbfbd7e0bc10afd8826d6d762fca40e77c986_screenshot_2025-07-31_at_6.03.55___pm.png)
## PCB Wiring Diagram
![img](https://hc-cdn.hel1.your-objectstorage.com/s/v3/d84d50014f3c763e20f84c45d50b902c72ce6dd0_screenshot_2025-07-31_at_6.04.13___pm.png)
## 3D View of PCB
![img](https://hc-cdn.hel1.your-objectstorage.com/s/v3/6ea45630e6804680592502100d09f40aed760abd_screenshot_2025-07-31_at_11.53.10___pm.png)
## Battery Box
![img](https://hc-cdn.hel1.your-objectstorage.com/s/v3/ed4c907d60fad636032d58342cff35c47ba04015_screenshot_2025-07-31_at_6.32.34___pm.png)
## Close-up of PCB Wall
![img](https://hc-cdn.hel1.your-objectstorage.com/s/v3/66d154698feb9bb12a59409ecfde0acb4c023f62_screenshot_2025-07-31_at_6.35.55___pm.png)
## User Control Panel (external modules connected here)
![img](https://hc-cdn.hel1.your-objectstorage.com/s/v3/22308247853b5489cdd5da76ab8be6df6bacaa96_screenshot_2025-07-31_at_10.06.07___pm.png)
## Handle with Lock Mechanism
![img](https://hc-cdn.hel1.your-objectstorage.com/s/v3/5a6ffb811a8e9d410a96445789bcb36389fe2946_screenshot_2025-07-31_at_10.58.33___pm.png)
## Close-up of Lock Mechanism (will superglue spring and magnet)
![img](https://hc-cdn.hel1.your-objectstorage.com/s/v3/5c3626e06f13cada701cf539a6c7b979acdeacb6_screenshot_2025-07-31_at_11.15.45___pm.png)
## Wire Support on Armrest
![img](https://hc-cdn.hel1.your-objectstorage.com/s/v3/3f076fdad0a60809efd0247c3fd230b4fd30fb90_screenshot_2025-07-31_at_11.17.25___pm.png)

---

# Bill of Materials (BOM)

| Reference | Qty | Description | Footprint | Purchase Link | Status |
|-----------|-----|-------------|-----------|---------------|---------|
| C1,C2,C3,C4,C6,C20,C23,C25 | 8 | Polarized Capacitor | CP_Radial_D5.0mm_P2.50mm | [AliExpress](https://www.aliexpress.com/item/1005002524973878.html) | |
| C5,C7,C8,C9,C10,C11,C12,C13,C14,C15,C16,C17,C18,C19,C22,C24 | 16 | Ceramic Capacitor | C_0603_1608Metric | [AliExpress](https://www.aliexpress.com/item/33000528620.html) | |
| C21 | 1 | Ceramic Capacitor (45°) | C_0603_1608Metric | [AliExpress](https://www.aliexpress.com/item/33000528620.html) | |
| D1 | 1 | TVS Diode | D_SMA | [AliExpress](https://www.aliexpress.com/item/1005002276080010.html) | |
| D2,D3,D4,D5,D8,D9,D10,D11,D12,D13,D14,D15,D16,D17,D18,D19 | 16 | Schottky Diode | D_SMA | [AliExpress](https://www.aliexpress.com/item/4001272645647.html) | |
| D6,D7 | 2 | LED | LED_D5.0mm | - | ✅ Have |
| F1 | 1 | Fuse | Fuse_BelFuse_0ZRE0005FF | - | ✅ Have |
| J1 | 1 | Buck Converter 24V→5V | PinSocket_1x04_P2.54mm | [AliExpress](https://www.aliexpress.com/item/1005006648976219.html) | |
| J2 | 1 | Buck Converter 24V→12V | FanPinHeader_1x04_P2.54mm | [AliExpress](https://www.aliexpress.com/item/1005004705881343.html) | |
| J3 | 1 | ICSP Programming Header | PinHeader_2x03_P2.54mm | - | ✅ Have |
| J4 | 1 | USB Serial | PinHeader_1x06_P1.00mm | - | ✅ Have |
| J5 | 1 | Raspberry Pi Zero | Harwin_M20-7812045_2x20 | [AliExpress](https://www.aliexpress.com/item/1005005792181612.html) | |
| J8 | 1 | Microphone | PinHeader_1x03_P1.00mm | [AliExpress](https://www.aliexpress.com/item/4001293896057.html) | |
| J9 | 1 | TFT 3.5" Display | PinHeader_1x14_P1.00mm | [AliExpress](https://www.aliexpress.com/item/1005008990800806.html) | |
| J10 | 1 | MPU6050 IMU | PinSocket_1x08_P2.54mm | [AliExpress](https://www.aliexpress.com/item/1005005682188615.html) | |
| J11 | 1 | DS3231 RTC | PinSocket_1x06_P2.54mm | [AliExpress](https://www.aliexpress.com/item/1005007143542894.html) | |
| J12 | 1 | Ultrasonic Sensor 1 | PinHeader_1x04_P1.00mm | - | ✅ Have |
| J13 | 1 | Ultrasonic Sensor 2 | PinHeader_1x04_P1.00mm | - | ✅ Have |
| J14 | 1 | Ultrasonic Sensor 3 | PinHeader_1x04_P1.00mm | - | ✅ Have |
| J15 | 1 | GPS Module | PinHeader_1x04_P1.00mm | [AliExpress](https://www.aliexpress.com/item/1005006459556070.html) | |
| J16 | 1 | Joystick Control | PinHeader_1x05_P1.00mm | - | ✅ Have |
| J17 | 1 | Temperature Sensor 1 | PinHeader_1x03_P1.00mm | - | ✅ Have |
| J18 | 1 | Temperature Sensor 2 | PinHeader_1x03_P1.00mm | - | ✅ Have |
| J19 | 1 | Servo 1 | PinHeader_1x02_P1.00mm | - | ✅ Have |
| J20 | 1 | Servo 2 | PinHeader_1x02_P1.00mm | - | ✅ Have |
| J21 | 1 | Linear Actuator | PinHeader_1x02_P1.00mm | - | ✅ Have |
| J22 | 1 | Audio Amplifier (LM386) | PinHeader_1x06_P1.00mm | [AliExpress](https://www.aliexpress.com/item/1005007577064258.html) | |
| J23 | 1 | Speaker | PinHeader_1x02_P1.00mm | [AliExpress](https://www.aliexpress.com/item/1005007504226811.html) | |
| J24 | 1 | XT60-M Power Connector | AMASS_XT60-M | [AliExpress](https://www.aliexpress.com/item/1005008955682135.html) | |
| J25,J26 | 2 | Motor Power Terminals | TerminalBlock_Phoenix_MKDS | [AliExpress](https://www.aliexpress.com/item/1005003179482974.html) | |
| Q1,Q2,Q3,Q4 | 4 | BSS138 MOSFET | SOT-23 | [AliExpress](https://www.aliexpress.com/item/1005009546772808.html) | |
| R1-R26 | 26 | Resistor | R_0603_1608Metric | - | ✅ Have |
| SW1 | 1 | SPST Switch | SW_PUSH-12mm | [AliExpress](https://www.aliexpress.com/item/1005006921918648.html) | |
| SW2-SW9 | 8 | Push Button | SW_PUSH-12mm | [AliExpress](https://www.aliexpress.com/item/1005007791349282.html) | |
| U1 | 1 | LM7805 Voltage Regulator | TO-220-3_Vertical | [AliExpress](https://www.aliexpress.com/item/10000200087213.html) | |
| U2 | 1 | AMS1117-3.3 Regulator | SOT-223-3_TabPin2 | [AliExpress](https://www.aliexpress.com/item/1005005774011848.html) | |
| U3 | 1 | ATMEGA2560-16AU MCU | TQFP100-0.5-14X14MM | [Digi-Key](https://www.digikey.ca/en/products/detail/microchip-technology/ATMEGA2560-16AU/735455) | |
| U4,U5,U6,U7 | 4 | BTS7960B Motor Driver | DPAK127P1490X440-8N | [AliExpress](https://www.aliexpress.com/item/1005006757604804.html) | |
| U9,U10 | 2 | L298N Motor Driver | TO-220-15_P2.54x2.54mm | [AliExpress](https://www.aliexpress.com/item/1462773567.html) | |
| U11 | 1 | ESP32-C3-MINI WiFi Module | XCVR_ESP32-C3-MINI-1-N4 | [AliExpress](https://www.aliexpress.com/item/1005007446928015.html) | |
| Y1 | 1 | Crystal Oscillator | Crystal_HC49-4H_Vertical | [AliExpress](https://www.aliexpress.com/item/1005002830871853.html) | |



