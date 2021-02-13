#!/usr/bin/python3
# Author Shyam Jos <shyamjos.com> 

import subprocess
import time
import sys
import logging
import argparse

#Configure CLI options
parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='A simple supervisord like python script for monitoring a process')
parser.add_argument('-c','--command', help='Full path to script or command to supervise. eg: ./script.sh or "free -m"', required=True)
parser.add_argument('-i','--interval', help='Check process is alive every N seconds', nargs='?', const=1, type=int, default=1)
parser.add_argument('-w','--wait', help='Seconds to wait between attempts to restart process', nargs='?' , const=1, type=int, default=1)
parser.add_argument('-r','--retry', help='Number of attempts to retry if process stops, default value 0 means always restart', nargs='?', const=0, type=int, default=0)
parser.add_argument('-l','--loglevel', help='set output log level, (default level is: %(default)s)', nargs='?', const='info', choices=["debug", "info", "warning", "error"], default='info')
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

#Logging configuration
logger = logging.getLogger('supervisor.py')
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%d-%m-%y %H:%M:%S')
#set logging level
level = logging.getLevelName(args.loglevel.upper())
logger.setLevel(level)                               

#Keep count of process restarts
RESTART_COUNT = 0

#Supervisor function
def do_supervise(args):
    #Set restart counter as global variable
    global RESTART_COUNT
    #Set max restart count(default: always restart)
    max_restart = args.retry
    logger.info("supervisor.py starting process: %s", args.command)
    try:
        #start the process and monitor
        proc = subprocess.Popen(args.command, shell=True)
        logger.info("Process started!")
        while proc.poll() is None:
            #Check process is alive every N seconds
            time.sleep(args.interval)
            logger.debug("Process is alive!")
    except KeyboardInterrupt:
        print ("Got Keyboard interrupt. Exiting...")
        proc.kill()
        sys.exit(1)

    #Restart until max_restart or always restart when max_restart == 0 (default)
    if RESTART_COUNT < max_restart or max_restart == 0:
        logger.error('process exited with status code:  %s', proc.poll())
        logger.info("Waiting %s seconds before restarting process again!", args.wait)
        try:
            time.sleep(args.wait)
            logger.info("Restarting Process!")
            #Keep track of process restarts
            RESTART_COUNT +=1
            do_supervise(args)
        except KeyboardInterrupt:
            print ("Got Keyboard interrupt. Exiting...")
            sys.exit(1)
    else:
        #exit if max retries is reached
        logger.error('process exited with status code:  %s', proc.poll())
        logger.error("Max retries reached!, Total Restarts: %s", RESTART_COUNT)
        sys.exit(1)
#Start process
do_supervise(args)    
        
        
