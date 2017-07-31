#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import urllib
import urllib2
import time
import datetime
import os

roomidlist = []
readlogpath = "../"
writelogpath = "./log/"
reqAddrUrl= "http://54.222.218.126/ping2/suntian/display_roomid_hd_onl.php?"

class Project:

	def __init__(self):
		print "--- init ---"
		self.printLocalTime()

	def start(self):
		print "--- start ---"
		self.date = time.strftime("%Y-%m-%d", time.localtime())
		self.makefile()
		self.readLogerFile()
		self.writeRoomIdInFile()
		self.delRepeatInFile()

	def printLocalTime(self):
		mytime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		print mytime

	def makefile(self):
		file = writelogpath
		if not os.path.exists(file):
			os.mkdir(file)

	def readLogerFile(self):
		filename = readlogpath+"loger.log."+self.date
		print "--- open file %s success ---"%filename
		f = open(filename, "r")  
		while True:  
		    line = f.readline()  
		    if line:  
		        line=line.strip()
		        if line.find('level=classtest')>0 and line.find('flash=1 camera=1')>0:
			        p=line.find('roomid')
			        q=line[p:-1].find(' ')
			        roomid = line[p:q+p].strip('roomid=')
			        ##print roomid
			        ##roomid = 9304335 ##假的roomid,正式使用时删掉本行
			        onlineclass_roomid = self.getRoomId(roomid)
			        ##print onlineclass_roomid
			        roomidlist.append(onlineclass_roomid)    
		    else:  
		        break
		f.close()
        
	def getRoomId(self, roomid):
		##调接口读取返回值
		Reqaddr= reqAddrUrl+"id=%s"%roomid
		##print Reqaddr
		str_key="Onlineclass RoomID : "
		res = urllib2.Request(Reqaddr) 
		uh = urllib2.urlopen(res)
		reqstr = uh.read().strip()

		##解析返回页面，取出onlineclass_roomid
		line=reqstr.strip(' </br>').strip('</h2>')
		##print line
		p=line.find(str_key)
		if(p<0):			
			pass
		else:
			onlineclass_roomid=line[p:-1].strip(str_key)
			return onlineclass_roomid
	
	def writeRoomIdInFile(self):
		filename = writelogpath+"roomid."+self.date
		f = open(filename, 'w')
		for roomid in roomidlist:
			if roomid is None:
				continue
			else:
                                f.write(roomid)
				f.write('\n')
		f.close()
		print "--- write file %s success ---"%filename

	def delRepeatInFile(self):
		##读有重复值的文件
		filename = writelogpath+"roomid."+self.date
		roomid_set = set()
		f = open(filename, 'r')
		while True:  
		    line = f.readline()  
		    if line:
		        line=line.strip()
		        roomid_set.add(line)
		    else:  
		        break
		f.close()

		##写入无重复值文件
		filename = writelogpath+"no_repeat_roomid."+self.date
		f = open(filename, 'w')
		for roomid in roomid_set:
			f.write(roomid)
			f.write('\n')
		f.close()
		print "--- write no repeat file %s success ---"%filename




if __name__ == "__main__":
	if len(sys.argv) < 1:  
		print "No action specified."  
		sys.exit()  
	readlogpath = sys.argv[1]
	reqAddrUrl = sys.argv[2]
	project = Project()
	project.start()
	project.printLocalTime();  
