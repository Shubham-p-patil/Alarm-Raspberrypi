from bluetooth import *
import  alsaaudio
import time
import pygame
import pyaudio
import RPi.GPIO as GPIO
from threading import Thread
import alarmfinal


#Declaration of variables and setting up gpio pins

GPIO.setmode(GPIO.BCM)
flag_vibration=0
vibration_on=0
myDelay=13
vibration_thread=None
alarm_thread=None
GPIO.setup(19,GPIO.OUT)


## @function for controlling the vibration motors

def vibration(*args):
    global flag_vibration
    global vibration_on
    if vibration_on==1:
        GPIO.output(19,True)
        time.sleep(2)
        GPIO.output(19,False)
        time.sleep(2)
        if flag_vibration==1:
            vibration()

## @function for putting a stop to music    

def stop_commands():
    pygame.mixer.music.stop()
    pygame.mixer.music.quit()

## @function which will take inputs from your app and set the commands for setting ON and OFF

def connect_bluetooth():
    global vibration_on
    global flag_vibration
        
    #server_sock.close()
    print('Connection code to bluetooth')
    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(("",1))
    server_sock.listen(1)
    print("Waiting for connection on RFCOMM channel")
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)
    try:
        while True:
            data = client_sock.recv(1024)
            print("received [%s]" % data)
            try:
                command,value = data.split(":")
            except RuntimeError:
                print "Command reception error"
            print command
            
            if command == 'alarm':
                global alarm_thread
                print "Inside_alarm"
                sub_com,alarm_no,hrs,mins,status=value.split(',')
                print   sub_com,alarm_no,hrs,mins,status
                if sub_com == 'set':
                    flag=True
                    alarm_thread=Thread(target=alarm.alarmCheck,args=(hrs,mins,status,flag,client_sock,))
                    alarm_thread.start()
            elif command == 'dismiss':
                alarm.alarm_stopper()
            elif command == 'snooze':
                alarm_thread=Thread(target=alarm.alarm_snoozer,args=(client_sock,))
                alarm_thread.start()
            elif command == 'volume' :
                vol = alsaaudio.Mixer('PCM')
                if value == 'check':
                    client_socket.send(vol.get_volume())
                else:
                    volume=int(value)
                    vol.setvolume(volume)
            elif command=='vibrate':
                if value=='true':
                    vibration_on=1
                    GPIO.output(19,True)
                    time.sleep(2)
                    GPIO.output(19,False)
                else:
                    vibration_on=0
                    GPIO.output(19,False)

    except IOError:
        pass

    print("Disconnected")

    client_sock.close()
    server_sock.close()
    print("All done")
    connect_bluetooth()

t1 = Thread(target=connect_bluetooth)
t2 = Thread(target=vibration)

t1.start()

    

#thread 1
    #bluetooth server + Alarm commands
