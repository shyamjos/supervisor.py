#!/usr/bin/python3

import subprocess
import time
import sys
import logging
import time
import argparse

#Configure CLI options
parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='A simple supervisord like python script for monitoring a process')
parser.add_argument('-c','--command', help='Full path to script or command to supervise. eg: ./script.sh or "free -m"', required=True)
parser.add_argument('-i','--interval', help='Check process is alive every N seconds', nargs='?', const=1, type=int, default=1)
parser.add_argument('-w','--wait', help='Seconds to wait between attempts to restart process', nargs='?' , const=1, type=int, default=1)
parser.add_argument('-r','--retry', help='Number of attempts to retry if proccess stops, default value 0 means always restart', nargs='?', const=0, type=int, default=0)
parser.add_argument('-l','--loglevel', help='set output log level, (default level is: %(default)s)', nargs='?', const='info', choices=["debug", "info", "warning", "error"], default='info')
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

#Logging configuration
logger = logging.getLogger('supervisor.py')
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%d-%m-%y %H:%M')
#set logging level
level = logging.getLevelName(args.loglevel.upper())
logger.setLevel(level)                                

#Keep count of proccess restarts
RESTART_COUNT = 0

#Supervisor function
def do_supervise(args):
    #Set restart counter as global variable
    global RESTART_COUNT
    #Set max restart count(default: always restart)
    MAX_RESTART = args.retry
    logger.info("supervisor.py Starting..")
    #start the proccess in the background
    p = subprocess.Popen(args.command, shell=True)
    logger.info("Process started!")

    while p.poll() is None:
          #Poll process is alive every N seconds
          time.sleep(args.interval)
          logger.debug("Process is alive!")
    #Restart unit MAX_RESTART or always restart
    if RESTART_COUNT < MAX_RESTART or MAX_RESTART == 0:
       logger.error('process exited with status code:  %s', p.poll())
       logger.info("Waiting %s seconds before restarting proccess again!", args.wait)
       time.sleep(args.wait)
       logger.info("Restarting Proccess!")
       #Keep track of process restarts
       RESTART_COUNT +=1
       do_supervise(args)
    else:
        #exit if max retries is reached
        logger.error("Max retries reached!, Total Restarts: %s", RESTART_COUNT)
        sys.exit(1)
#Start process
do_supervise(args)    
        
        
