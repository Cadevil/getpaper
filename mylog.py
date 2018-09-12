import os
import time
import traceback
import sys

def logerexception(tp,val,td):
	etype = str(tp)
	evalue = str(val)
	etb = traceback.extract_tb(td)
	errormsg = "type: " + etype + "\n"
	errormsg += "value: " + evalue + "\n"
	errormsg += "traceback: " + str(etb) + "\n"
	writetofile(errormsg)


def logerinfor(msg):
	writetofile(msg)


def writetofile(errormsg):
	logfilepath = os.path.abspath('.') + "\\log"
	if not os.path.exists(logfilepath):
		os.mkdir(logfilepath)
		
	logfile = time.strftime("%Y%m%d", time.localtime()) + ".txt"
	fp = open(logfilepath + "\\" + logfile,"a")
	ISOTIMEFORMAT= "%Y-%m-%d %X"
	happeningtime =  time.strftime(ISOTIMEFORMAT, time.localtime())
	usermsg = ""
	usermsg += happeningtime + "\n-------------------------------\n"
	usermsg += errormsg
	fp.write(usermsg + "\n")
	fp.close()