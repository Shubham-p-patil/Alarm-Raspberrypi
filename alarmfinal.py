import time
import pygame
from datetime import date
import RPi.GPIO as GPIO
from threading import Thread

GPIO.setmode(GPIO.BCM)

flag_vibrate=0

GPIO.setup(19,GPIO.OUT)

def vibration_func(*args):
    global flag_vibrate
    GPIO.output(19,True)
    time.sleep(2)
    GPIO.output(19,False)
    time.sleep(2)
    if flag_vibrate==1:
        vibration_func()


vibratet=Thread(target=vibration_func)

#Get Todays Date And Weekday Number
today = date.today()
day = date.isoweekday(today)
    
#Get Current Time In Hours And Minutes

def currentTime():
	hour = time.strftime("%H")
	current_hour = int(hour)
	minutes = time.strftime("%M")
	current_minutes = int(minutes)
	current_status = time.strftime("%p")
##	print current_hour , current_minutes , current_status
	return current_hour , current_minutes , current_status

(current_hour , current_minutes , current_status) = currentTime()

#Get User Input At Which He Wants Alarm To Be Set

def getUserInput(hour_user_input , minutes_user_input , status_user_input):
	if status_user_input == 'PM' and hour_user_input < 12 :
		hour_user_input = hour_user_input + 12
	if status_user_input =='AM' and hour_user_input == 12 :
		hour_user_input = 0
		minutes_user_input = 0
	return int(hour_user_input) , int(minutes_user_input) , status_user_input

#Alarm Sound Regarding Functions

def alarm_sounder():
        global flag_vibrate
        global vibratet
        flag_vibrate=1
        vibratet.start()
	pygame.mixer.init()
	pygame.mixer.get_init()
	pygame.mixer.music.load('/home/pi/Downloads/PillowIoTClient/123.mp3')
	pygame.mixer.music.play(-1)


def alarm_stopper():
        global flag_vibrate
        flag_vibrate=0
	pygame.mixer.music.stop()
	pygame.mixer.quit()

#Get The Time Remaining For Alarm

def alarm_timeleft(hour_user_input , minutes_user_input , status_user_input):
	hours_left=0
	minutes_left=0
	if (status_user_input  == 'AM' and current_status == 'AM') or (status_user_input  == 'PM' and current_status == 'PM'):
		print "First if"
		if (current_hour >= hour_user_input) and (current_minutes >= minutes_user_input):
			print "First if"
			tot_minutes = current_hour*60 + current_minutes - hour_user_input*60 - minutes_user_input
			tot_minutes = 24*60 - tot_minutes
			hours_left = tot_minutes/60
			minutes_left = tot_minutes%60
		elif (current_hour ==  hour_user_input) and (current_minutes == minutes_user_input) :
			hours_left = 24
			minutes_left = 0
		else :
                        print "first 3"
                        print hour_user_input,minutes_user_input,current_hour,current_minutes
			tot_minutes = hour_user_input*60 + minutes_user_input - current_hour*60 - current_minutes
			print tot_minutes
			hours_left = tot_minutes/60
			minutes_left = tot_minutes%60
	if (status_user_input  == 'PM' and current_status == 'AM') :
		print "second if"
		tot_minutes = hour_user_input*60 + minutes_user_input - current_hour*60 - current_minutes
		hours_left = tot_minutes/60
		minutes_left = tot_minutes%60
	if (status_user_input  == 'AM' and current_status == 'PM'):
		print "Third if"
		tot_minutes = 24*60 + hour_user_input*60 + minutes_user_input - current_hour*60 - current_minutes
		hours_left = tot_minutes/60
		minutes_left = tot_minutes%60
	print "Time Remaining : %s hrs %s minutes" %(hours_left , minutes_left)

#Alarm Snoozing

def alarm_snoozer(client_sock):
        (hour_input , minutes_input , status) = currentTime() 
	tot_minutes_user_input = 10 + minutes_input + hour_input*60
	hour_user = tot_minutes_user_input/60 
	minutes_user =  tot_minutes_user_input%60
	if status == 'AM' and hour_user == 12 :
		status = 'PM'
	if status == 'PM' and hour_user == 24 :
		hour_user = 0
		status = 'AM'
	print hour_user , minutes_user
	global flag_vibrate
        flag_vibrate=0
	pygame.mixer.music.stop()
	pygame.quit()
	flag = True
	alarmCheck(hour_user,minutes_user,status,flag,client_sock)
	return

#Comparing With Current Time

def compareWithCurrentTime(hour_input,minutes_input,status_input):
	#print "It Came Here"
	(current_hour , current_minutes , current_status) = currentTime()
	if status_input == 'AM' and current_status == 'AM':
		if hour_input == current_hour and minutes_input == current_minutes :
			return True
	elif status_input  == 'PM' and current_status == 'PM':
		if hour_input == current_hour and minutes_input == current_minutes :
			return True
	return False
    
#####################################--------------Alarm Ready---------------#########################################
def alarmCheck(hour_user_input,minutes_user_input,status_user_input,flag,client_socket):
        print (hour_user_input,minutes_user_input,status_user_input,flag,client_socket)
        (hour_input,minutes_input,status)= getUserInput(int(hour_user_input) , int(minutes_user_input) , status_user_input)
        alarm_timeleft(hour_input , minutes_input , status)
        while True :
                #print "First"
                if compareWithCurrentTime(hour_input,minutes_input,status) :
                        while True :
                                #print "Second"
                                print flag
                                if flag :
                                        alarm_sounder()
                                        client_socket.send("alarmrang\n")
                                        print flag
                                        flag = False
                                else :
                                        print "Alarm is off"
                                        return
