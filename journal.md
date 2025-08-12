# Wheelchair Project Journal!
---
TITLE: Customized AI Electric Wheelchair

AUTHOR: PRISCA CHIEN (U0741Q95Y02)

DESCRIPTION: my own motorized wheelchair with ai

CREATE DATE: July 27

---

> Prisca: 82 hours

> Updated until: Aug 10

---

### 🗓️ July 27 - 12 hrs
- Researched components for wheelchair
- Looking for the cheapest price for all components (this actually took such a long time)
- Searching YT tutorials and looking at companies who've made electric wheelchairs for inspiration when designing my own parts for the electric wheelchair

---

### 🗓️ July 28 - 15 hrs
- More research done on components for wheelchair (yes more research there was a lot I didn't know like TVS diodes, schottky diodes, and when to use capacitors)
- Finalizing which electronics should be module and which should be embedded on the board
- Found all links to buy components I need for this project
- Took dimensions of wheelchair to brainstrom 3d printable ideas

---

### 🗓️ July 29 - 17 hrs
- Started PCB schematic
- Finsihed PCB schematic
- Iteration 1 of the schematic
![img](https://hc-cdn.hel1.your-objectstorage.com/s/v3/4b4b8b8afdccffbccfdec6a6b5717c06559c7f5f_img_4016.jpg)

---

### 🗓️ July 30 - 15 hrs
- Planned structure and placement of PCB components
  - Power components will be on the outside on opposite sides of each other. The power inputs will be on the left and the power outputs (eg, motors) will be on the right side
  - ATMEGA2560 will go in the middle as it is the microcontroller most used. The other microcontrollers, including Raspberry Pi connecting pins and ESP32 chipset are placed on the 
- Finished PCB Wiring (I will start using more modules cuz this wiring was insane to do)
- What it started out looking like
![img](https://hc-cdn.hel1.your-objectstorage.com/s/v3/f4f6b399066dbb6df82e7c2efb8668861b58bc5c_img_4015.jpg)

---

### 🗓️ July 31 - 14 hrs
- Updated schematic and wiring connection pins, added mounting holes and mounting hole pads
- Deciding whether to use copper pours or thick wiring
- Designed and cadded all 3d printable parts based on my wheelchair
  - Armrest mount with magnets
  - Walker handle and locking mech (copied fromy my wheelchair)
  - Battery box to hold 24V battery
  - PCB walls. I am leaving the front and back open to cool it down faster
  - Control panel with all six buttons and joystick. Will add breadboard in
  - Wiring will go from the PCB through the armrest mount to the panel
- Created GitHub repo and submitted everything!
- Rough design work for cadding parts
![img](https://hc-cdn.hel1.your-objectstorage.com/s/v3/43a9d2fc1330624c16ef6537d5dcf59f4a01176e_screenshot_2025-08-01_at_1.18.18___am.png)

---

### 🗓️ August 6 - 3 hrs
- Made wheelchair CAD and fitted it to IRL dimensions

---

### 🗓️ August 7-9 - 6 hrs
- Learned about thermal vias, netclasses, copper pours, etc of anything to cool the PCB down
- Created netclasses for +5V, +12V, and +24V
- Updated all power traces with the best wire size possible. If the trace is not wide enough (eg, +24V needs to be 5mm but I can only afford 3mm of space), I will put copper pours over it to disperse the heat around
- Rewired +5V, +12V, +24V, and GND to fit around all components such that no errors or warnings are seen when I run the DMC
- In the case that the ATMEGA2560 gets too hot, I plan to strap down a 24V to the PCB walls and 

---

### 🗓️ August 10 - 2 hrs
- Finished putting the copper pours over the +24v and +12V wiring
- Front PCB of copper pour is for +12V
- Back PCB of copper pour is for +24V
- Updated journal
