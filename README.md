# Neither Here Nor There

Installation at the Berggruen Institute, Spring 2023 

----

## Instructions

1. make sure configuration files are pushed to github
    - check you're in the top level of the repo
    - git add .
    - git commit -m "you changes"
    - git push origin main

2. run update script
    - check you're in the top level of the repo
    - python3 run/runnhnt.py -c update -d <devices you want to update>
    - press enter as asked
    - make sure the commit hash matches as expected 

3. ssh into the devices you want to start
    - ssh se@<device>.local
    
4. run the python script to start them
    - python3 Documents/NHNTBerggruen/python/nhnt.py 

5. give the start command
    - use ultrasonic protocol on waver

6. make sure they start
    - you need to do a little hand holding for the start command and the first exchange
    - if one misses the start, press ctrl-C on all of them and re-start until you get a clean state where they're all going
    - once they've done one exchange it should be fine to run for a long while

7. conversation transcripts
    - the conversation will be saved as a log file on each device
    - these are just timestamped...the time is probably really wrong, but the date should be OK
    - ssh into the device you want
    - cd Documents/NHNTBerggruen/logs
    - ls to find the one you want, or just copy all of them
    - run scp from your computer: scp -r se@<device>.local:/home/se/Documents/NHNTBerggruen/logs <path to where you want them on your computer>
 