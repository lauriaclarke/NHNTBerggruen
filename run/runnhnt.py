# scp config files
# scp python file
# ssh into devices
# run python
# check for errors?

import argparse
from paramiko import SSHClient
from scp import SCPClient

def copyConfigFile(device):
    fileName = "config/" + device + ".yaml"
    fileNameDest = "/home/" + device + "/NHNTBerggruen/config/" + device + ".yaml"
    ipAddress = device + '.local'

    print("copying " + fileName + " to " + device + "@" + ipAddress)

    client = SSHClient()
    client.load_system_host_keys()
    client.connect(ipAddress, username=device, password=device)
    with SCPClient(client.get_transport()) as scp:
        scp.put(fileName, )
    scp.close()

def updateGitRepo(device):
    ipAddress = device + '.local'

    client = SSHClient()
    client.load_system_host_keys()
    client.connect(ipAddress, username=device, password=device)
    
    cmd = "if test -d /home/" + device + "/Documents/NHNTBerggruen; then echo \"1\"; fi"
    ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(cmd)

    output = ssh_stdout.readlines()
    
    if output[0].strip() == '1':
        print("updating NHNTBerggruen GitHub repo")
        input("press ENTER to continue operation or ctrl-C to cancel")

        cmd = "cd /home/" + device + "/Documents/NHNTBerggruen; git fetch https://github.com/lauriaclarke/NHNTBerggruen.git"
        ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(cmd)
    else:
        print("cloning NHNTBerggruen GitHub repo")
        input("press ENTER to continue operation or ctrl-C to cancel")
        
        cmd = "git clone https://github.com/lauriaclarke/NHNTBerggruen.git" 
        ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(cmd)

    client.close()


def  runNHNT(device):
    ipAddress = device + '.local'

    client = SSHClient()
    client.load_system_host_keys()
    client.connect(ipAddress, username=device, password=device)
    
    cmd = "if test -d /home/" + device + "/Documents/NHNTBerggruen; then echo \"1\"; fi"
    ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(cmd)

    output = ssh_stdout.readlines()
    
    if output[0].strip() == '1':
        print("starting NHNT on " + device)
        input("press ENTER to continue operation or ctrl-C to cancel")

        cmd = "cd /home/" + device + "/Documents/NHNTBerggruen; python3 python/nhnt.py"
        ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(cmd)
        output = ssh_stdout.readlines()
        print(output)
    else:
        print("coult not find the program, please rerun this using: -c update")
 

    client.close()

def main():
    allDevices = ['se1', 'se2', 'se3', 'se4']

    # parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--cmd', '-c', default='run', choices=['config', 'run', 'update'], help="specify the command you would like to use, defaults to run")
    parser.add_argument('--devices', '-d', nargs='+', default='all', choices=['all', 'se1', 'se2', 'se3', 'se4'], help="specify which devices to use, defaults to all")
    args = parser.parse_args()

    # copy config files
    if args.cmd == 'config':
        print("would you like to copy CONFIG files to " + str(args.devices) + "?")
        input("press ENTER to continue operation or ctrl-C to cancel")

        # iterate across all devices executing command
        if args.devices == 'all':
            for pi in allDevices:
                copyConfigFile(pi)
        else:
            for pi in args.devices:
                copyConfigFile(pi)

    # update git repo
    if args.cmd == 'update':
        if args.devices == 'all':
            for pi in allDevices:
                updateGitRepo(pi)
        else:
            for pi in args.devices:
                updateGitRepo(pi)

    # run the stuff
    if args.cmd == 'run':
        if args.devices == 'all':
            for pi in allDevices:
                runNHNT(pi)
        else:
            for pi in args.devices:
                runNHNT(pi)




if __name__ == "__main__":
    main()
