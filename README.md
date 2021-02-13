## supervisor.py
A simple supervisord like python script for monitoring a process
### Usage
```
usage: supervisor.py [-h] -c COMMAND [-i [INTERVAL]] [-w [WAIT]] [-r [RETRY]] [-l [{debug,info,warning,error}]]

A simple supervisord like python script for monitoring a process

optional arguments:
  -h, --help            show this help message and exit
  -c COMMAND, --command COMMAND
                        Full path to script or command to supervise. eg: ./script.sh or "free -m"
  -i [INTERVAL], --interval [INTERVAL]
                        Check process is alive every N seconds
  -w [WAIT], --wait [WAIT]
                        Seconds to wait between attempts to restart process
  -r [RETRY], --retry [RETRY]
                        Number of attempts to retry if proccess stops, default value 0 means always restart
  -l [{debug,info,warning,error}], --loglevel [{debug,info,warning,error}]
                        set output log level, (default level is: info)
```
