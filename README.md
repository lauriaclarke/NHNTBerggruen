# Neither Here Nor There

Installation at the Berggruen Institute, Spring 2023 


----

## Device Information

| sticker name | ip address | hostname | username | password |
|--------------|------------|----------|----------|----------| 
| SE1  |  192.168.1.101	| se1 | se | se |
| SE2  |  192.168.1.102	| se2 | se | se |
| SE3  |  192.168.1.103	| se3 | se | se |
| SE4  |  192.168.1.104	| se4 | se | se |
| none |  192.168.1.105	| se5 | se | se |


----

## Instructions

0. make sure you're on the hotspot WiFi
    - SSID: NHNTLocal
    - PW: nhntl0cal

1. make sure configuration files are pushed to github
    - check you're in the top level of the repo <your path>/NHNTBerggruen
    - run the following commands to commit:
        > ```git add .```

        > ```git commit -m "you changes"```

        > ```git push origin main```



2. run updater script
    - if you forget how to use it you can run the help command
        > ```python3 run/runnhnt.py --help```
    - check you're in the top level of the repo then run the updater script
    - example for updating se4 and se5:
        > ```python3 run/runnhnt.py -c update -d se4 se5```
    - example for updating all devices:
        > ```python3 run/runnhnt.py -c update -d all```
    - press enter as asked
    - make sure the commit hash matches as expected 

3. ssh into the devices you want to start
    > ```ssh se@<device>.local```
    - for example to ssh into se4:
    > ```ssh se@se4.local```
    
4. run the python script to start them
    > ```python3 Documents/NHNTBerggruen/python/nhnt.py```

5. give the start command
    - use ultrasonic protocol on waver and send "start"

6. make sure they start
    - you need to do a little hand holding for the start command and the first exchange
    - if one misses the start, press ctrl-C on all of them and re-start until you get a clean state where they're all going
    - once they've done one exchange it should be fine to run for a long while

7. conversation transcripts
    - the conversation will be saved as a log file on each device
    - these are just timestamped...the time is probably really wrong, but the date should be OK
    - ssh into the device you want
    - ssh into the device and look for the logs you want, or just copy all of them
    - to copy all: 
        >```scp -r se@<device>.local:/home/se/Documents/NHNTBerggruen/logs <destination path>```
    - to copy one: 
        >```scp se@<device>.local:/home/se/Documents/NHNTBerggruen/logs/<filename> <destination path>```
 