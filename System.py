#!/usr/bin/env python3
#-- coding: utf-8 --

import RPi.GPIO as GPIO #Importe la bibliothèque pour contrôler les GPIOs
import time
import os
import netifaces
import psutil
from threading import Timer
from blinkt import set_pixel, set_brightness, show, clear

class System:

	def __init__(self):
		
		print("#################################")
		print("########### System Tools ########")
		print("#################################")

		GPIO.setmode(GPIO.BCM)  	#Standard GPIO Number
		GPIO.setwarnings(False)
		
		set_brightness(0.1)

		self.__TEMPERATURE_LED = 0
		self.__CPU_LED = 1
		self.__MEMORY_LED = 2
		self.__WEB_SERVER_LED = 3
		self.__INTERNET_LED = 4

		self.__BLINKS = 5		#Number of blinks in init step
		self.__DELAY_BLINK = 0.05 	#s

		self.__localIP = None
		
		#Display settings
		cpus = psutil.cpu_count(logical=True)
		print("CPUs : "+str(cpus))
		
		cpuFreq = psutil.cpu_freq()
		print("Frequence : "+str(cpuFreq.current)+" MHz")
		print("Frequence min : "+str(cpuFreq.min)+" MHz")
		print("Frequence max : "+str(cpuFreq.max)+" MHz")
		print("Boot time : "+str(psutil.boot_time())+" s")
		users = psutil.users()
		
		print("Users : ")
		for u in users:
			print(">>> name : "+u.name)	
		print(self.temperatures())

	def temperatures(self):

		"""Temperatures handler"""
		self.__lowTemp = 40.0
		self.__highTemp = 43.0

		currentTemperature = float(psutil.sensors_temperatures()['cpu_thermal'][0][1])  			
		#print(shwtemp())
		if(currentTemperature <= self.__lowTemp):
			set_pixel(self.__TEMPERATURE_LED, 0,255 , 0)
		elif(currentTemperature <= self.__highTemp and currentTemperature > self.__lowTemp ):
			set_pixel(self.__TEMPERATURE_LED, 255, 127, 0)
		else:
			set_pixel(self.__TEMPERATURE_LED, 255, 0, 0)
		show()

		return currentTemperature

	def webServer(self):
		response = None

		if(self.__localIP != None):
			response = os.system("ping -c 1 "+str(self.__localIP))

			if(response == False): #webServer is enable
				set_pixel(self.__WEB_SERVER_LED, 0, 255, 0)
			else:
				set_pixel(self.__WEB_SERVER_LED, 255, 0, 0)
			

		set_pixel(self.__WEB_SERVER_LED, 255, 0, 0)
		return response

	def network(self):
		"""Network handler"""
		self.__key_network = 2 #key of dict when network is used
		self.__interfaces = []

		eth0 = netifaces.ifaddresses("eth0")
		wlan0 = netifaces.ifaddresses("wlan0")

		if(self.__key_network in eth0):
			self.__interfaces.append(["eth0", netifaces.ifaddresses("eth0")[2][0]['addr']])
		if(self.__key_network in wlan0):
			self.__interfaces.append(["wlan0", netifaces.ifaddresses("wlan0")[2][0]['addr']])		

		if(len(self.__interfaces) == 0):				#Any interface
			set_pixel(self.__INTERNET_LED, 255,0, 0)
		elif(len(self.__interfaces) == 2):				#All interfaces
			set_pixel(self.__INTERNET_LED, 0, 255, 0)
			self.__localIP = self.__interfaces[0][1]
		else:											#Only one interface
			if(self.__interfaces[0][0] == "wlan0"):
				set_pixel(self.__INTERNET_LED, 255, 127, 0)
			else:	#eth0
				set_pixel(self.__INTERNET_LED, 0, 255, 0)
			self.__localIP = self.__interfaces[0][1]
		show()
		return self.__interfaces

	def blinkAll(self):

		"""All leds blinks"""
		clear()

		for step in range(0,self.__BLINKS):
			
			set_pixel(self.__TEMPERATURE_LED,0, 255, 0)
			set_pixel(self.__CPU_LED,0, 255, 0) 
			set_pixel(self.__WEB_SERVER_LED,0, 255, 0) 
			set_pixel(self.__INTERNET_LED,0, 255, 0) 
			set_pixel(self.__MEMORY_LED,0, 255, 0) 
			show()
			time.sleep(self.__DELAY_BLINK)
			set_pixel(self.__TEMPERATURE_LED,0, 0, 0)
			set_pixel(self.__CPU_LED,0, 0, 0) 
			set_pixel(self.__WEB_SERVER_LED,0, 0, 0) 
			set_pixel(self.__INTERNET_LED,0, 0, 0) 
			set_pixel(self.__MEMORY_LED,0, 0, 0) 
			show()
			time.sleep(self.__DELAY_BLINK)

	def cpu(self):

		""" Check CPU value"""
		self.__lowCPU = 10.0
		self.__highCPU = 60.0

		cpu = int(psutil.cpu_percent())

		if(cpu <= self.__lowCPU):
			set_pixel(self.__CPU_LED, 0,255 , 0)
		elif(cpu <= self.__highCPU and cpu > self.__lowCPU ):
			set_pixel(self.__CPU_LED, 255, 127, 0)
		else:
			set_pixel(self.__CPU_LED, 255, 0, 0)
		show()
		
		return cpu

	def memory(self):

		"""Check memory usage"""
		
		self.__lowMemory = 20.0
		self.__highMemory = 70.0

		raw_memory = psutil.virtual_memory()		
	
		available = round(raw_memory.available/1024.0/1024.0,1)
		used = round(raw_memory.used/1024.0/1024.0,1)
		all = round(raw_memory.total/1024.0/1024.0,1)
		percent = raw_memory.percent

		#print("Memory : "+str(used)+" / "+str(all)+" MB ("+str(percent)+"%)")

		if(percent <= self.__lowMemory):
			set_pixel(self.__MEMORY_LED, 0,255 , 0)
		elif(percent <= self.__highMemory and percent > self.__lowMemory ):
			set_pixel(self.__MEMORY_LED, 255, 127, 0)
		else:
			set_pixel(self.__MEMORY_LED, 255, 0, 0)
		
		show()
		return percent
		#print(raw_memory+" "+available+" "+all) 
def main():

	sys = System()
	sys.blinkAll()
	#sys.cpu()
	#sys.memory()
	
	time.sleep(1)

	while(1):
	
		print(sys.temperatures())
		print(sys.cpu())
		print(sys.memory())
		print(sys.network())
		print(sys.webServer())
		time.sleep(1)

if(__name__ == "__main__"):
	
	main()

