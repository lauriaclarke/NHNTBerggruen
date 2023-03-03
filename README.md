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
6. make sure they start
7. 