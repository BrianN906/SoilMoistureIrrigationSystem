# Soil Moisture Irrigation System - May 2026

An automated soil irrigation system that monitors and maintains optimal soil moisture levels over extended periods of time with minimal human intervation and computer power consumption. By continuously reading soil moisture data in configurable intervals and activating a water pump only when the moisture falls below a set threshold, this system works towards reducing water waste and simplifying the work required by plantowners.

This project was developed with the hope of simplifying garden maintenance and promoting environmental sustainability through smart, need-based water consumption. Rather than relying on fixed schedules, this system responds to real-time soil conditions to ensure water is only delivered when needed.

<br> <!-- Break -->

<img width="5712" height="4284" alt="Overview_Image" src="https://github.com/user-attachments/assets/24965781-1bc2-46a9-a99f-c89148fca176" />
A general overview of the project.

## Structure and Design

This project utilizes an Arduino to power the irrigation system and to read in soil moisture data. Using a capacitive soil sensor, readings were taken when the soil was dry and when it was wet. These two values were used as reference points. Each time a raw value was collected from the sensor, it is converted into a percentage relative to these two values.

Although the 5V water pump was controlled through the Arduino, it was electrically powered by a power supply module that utilizes a 9V battery. Although the water pump is designed to function automatically with little human interaction, a NO button was added in the event that the user wanted manual operation.

Additionally, Three LEDs are used to show the status of the soil and device. Green means that the soil is within the accepted moisture levels and that the device is functioning properly. Red means that the soil is not within the accepted mositure level and that the pump is running. White means that the manual override button was pressed and that the pump is currently running.
<br>
<img width="5712" height="4284" alt="Circuit_Image" src="https://github.com/user-attachments/assets/28b8a5bd-9412-4469-a5e3-1ba374e2514e" />
An image of the circuitry of the project showing the three LEDs, Arduino, button, power supply module, and relay. The power supply module, attached to one end of the breadboard, is powered by a 9V battery.

<br> <!-- Break -->

<img width="5712" height="4284" alt="Pump_Image" src="https://github.com/user-attachments/assets/62f2b5ee-50c8-4b73-aabf-6d0d40ad245f" />

An image of the water pump system and soil sensor. The pump is inside of the large water container (left), which supplies the water whenever needed by the pump. The water bottle (middle) is used to hold the tubing above the soil and does not provide any water to the system. It can be replaced with a rod or any support. The soil (right) is placed below the end of the tube and contains the capacitive soil sensor.

<br> <!-- Break -->

## Functionality Procedure
Upon the execution of the program, a CSV for the data is created if it does not yet exist. Every 20 minutes (or another set time by the user), the soil sensor takes a reading and calculates a moisture percentage relative to the original wet and dry values taken. This value is always recorded to the CSV and categorized as READ. In the event that the percentage does not fall within the accepted range, the program notifies the user of this, and the water pump automatically runs for a certain time set by the user. 10 seconds after, the new post-pump value is recorded to the CSV and categorized as PUMP. 

When the button is manually pressed by the user, the next iteration of the pump reading is skipped and the water pump is turned on for a certain time set by the user. 10 seconds after, the new post-pump value is recorded to the CSV and categorized as MANUAL.

<br> <!-- Break -->

https://github.com/user-attachments/assets/b10e69f4-deb9-45ba-bf2f-da3c5f5cfd0b

<img width="933" height="627" alt="pump log automatic" src="https://github.com/user-attachments/assets/71f7e59d-186c-458e-8e58-97324b2233f1" />
A demonstration of the water pump running when the soil moisture level does not fall within the accepted range. Under the video is a screenshot of the program log after the automatic pump (PUMP). At the bottom of the screenshot is the post-pump data value recorded to the CSV.

<br> <!-- Break -->

https://github.com/user-attachments/assets/dee26139-2375-4e87-aaa1-28e678ff8a83

<img width="922" height="682" alt="pump log manual" src="https://github.com/user-attachments/assets/ea4fb707-c6fe-45d1-b163-ea2302958a54" />

A demonstration of the water pump running when the manual override button is pressed. Under the video is a screenshot of the program log after the manual pump (MANUAL). At the bottom of the screenshot is the post-pump data value recorded to the CSV.

<br> <!-- Break -->

## Code Explanation
The Python script is responsible for recording the data onto the CSV and keeping the sensor readings consistent. After creating a CSV file, the program constantly tracks the time. Once 20 minutes have passed from the last read, the Python script writes READ to serial, which the Arduino takes and sends the sensor reading with the same. With this READ from the Arduino, the Python script logs it to the CSV as such. If that reading falls below the accepted moisture range, Python sends PUMP, which tells the Arduino to run the pump, wait 10 seconds, then take a new reading labeled as PUMP, which the Python script records to the CSV as such. This also resets the 20-minute timer so that the next automatic reading occurs 20 minutes after the post-pump value is recorded. Additionally, when the button is pressed, the Arduino runs the pump and waits similarly to the PUMP procedure, but instead returns the value as MANUAL, which the Python script records it to the CSV as. This also resets the 20-minute timer, like before.


