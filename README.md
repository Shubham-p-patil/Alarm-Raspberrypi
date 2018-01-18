# Alarm-Raspberrypi
Alarm Clock 

As the name suggest this project is for raspberry pi enthusiasts. A alarm clock script has been developed first for keyboard input and further modified to work with android app name bluetooth terminal. But provison has been made so that you can desgin your custom application for the same purpose. Recommended use of Raspberry pi 3 because of bluetooth adapter present inbuilt. Can be used with Raspberry pi 2 but an external adapter must be attached.

Instruction :-
1. Install Raspbian jessie image file and burn it on an SD card preferably 4GB
2. Make sure you have python and pip installed on it.
3. Now open CMD and enter :-

          $sudo apt-get update
          $sudo apt-get python-bluetooth
          $sudo apt-get pybluez
          $sudo pip install keyboard
          $sudo pip insatll alsaaudio
          $sudo pip install pygame
       
  Check if bluetooth is On:
  
          $sudo systemctl bluetooth status
          
  if not then manually start by:
  
          $sudo systemctl bluetooth start
 4. Now download the scripts from the repository
 5. Run the scripts using python idle
 6. Add to bash.rc to start it on powering on of raspberry pi
