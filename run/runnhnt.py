import os
import datetime
import argparse
from paramiko import SSHClient
from scp import SCPClient
# from multiprocess import Process
# from multiprocessing import Pool
# from pssh.clients.ssh.parallel import ParallelSSHClient
# from pssh.exceptions import Timeout
# from gevent import joinall

USERNAME="se"
PASSWORD="se"


def copyConfigFile(device):
    fileName = "config/" + device + ".yaml"
    fileNameDest = "/home/se/Documents/NHNTBerggruen/config/" + device + ".yaml"
    ipAddress = device + '.local'

    print("---" + device + "---")
    print("copying " + fileName + " to " + device + "@" + ipAddress)

    client = SSHClient()
    client.load_system_host_keys()
    client.connect(ipAddress, username=USERNAME, password=PASSWORD)
    with SCPClient(client.get_transport()) as scp:
        scp.put(fileName, fileNameDest)
    scp.close()

def updateGitRepo(device):
    ipAddress = device + '.local'

    client = SSHClient()
    client.load_system_host_keys()
    client.connect(ipAddress, username=USERNAME, password=PASSWORD)
    
    cmd = "if test -d /home/se/Documents/NHNTBerggruen; then echo \"1\"; fi"
    ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(cmd)

    output = ssh_stdout.readlines()
     
    print("---" + device + "---")

    # check if output is an empty list or not 
    if output:
        print("updating NHNTBerggruen GitHub repo")
        input("press ENTER to continue operation or ctrl-C to cancel")

        cmd = "cd /home/se/Documents/NHNTBerggruen; git pull origin main"
        ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(cmd)
        output = ssh_stderr.readlines()
        print(output)
    else:
        print("cloning NHNTBerggruen GitHub repo")
        input("press ENTER to continue operation or ctrl-C to cancel")
        
        cmd = "cd /home/se/Documents/; git clone https://github.com/lauriaclarke/NHNTBerggruen.git" 
        ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(cmd)

        output = ssh_stderr.readlines()
        print(output)

    client.close()

# def runParallel(devices):
#     # make logfile

#     # os.makedirs("logs/" + device, exist_ok = True)
#     # t = datetime.datetime.now()
#     # filename = "logs/" + device + "/" + t.strftime("%m_%d_%H_%M_%S") + ".txt"
#     # logfile = open(filename, "w")

#     os.makedirs("logs/", exist_ok = True)
#     t = datetime.datetime.now()
#     filename = "logs/run" + t.strftime("%m_%d_%H_%M_%S") + ".txt"
#     logfile = open(filename, "w")

#     hosts = []
#     for d in devices:
#         hosts.append(d + '.local')
    
#     print(hosts)
   
#     client = ParallelSSHClient(hosts, user=USERNAME, password=PASSWORD)
    
#     cmd = "cd /home/se/Documents/NHNTBerggruen; python3 python/nhnt.py"
#     output = client.run_command(cmd)
    
    
#     # output = client.run_command(cmd, use_pty=True, read_timeout=1)

#     # stdout = []
#     # for host_out in output:
#     #     try:
#     #         for line in host_out.stdout:
#     #             stdout.append(line)
#     #     except Timeout:
#     #         pass

#     # # Closing channel which has PTY has the effect of terminating
#     # # any running processes started on that channel.
#     # for host_out in output:
#     #     host_out.client.close_channel(host_out.channel)
#     # # Join is not strictly needed here as channel has already been closed and
#     # # command has finished, but is safe to use regardless.
#     # client.join(output)
#     # # Can now read output up to when the channel was closed without blocking.
#     # rest_of_stdout = list(output[0].stdout)

#     # for host_output in output:
#     #     for line in host_output.stdout:
#     #         print(line)
    

#     # for host_output in output:
#     #     logfile.write("--------------------------------\n")
#     #     logfile.write("STDOUT\n")
#     #     for line in host_output.stdout:
#     #         logfile.write(line)
    
#     # for host_output in output:
#     #     logfile.write("--------------------------------\n")
#     #     logfile.write("STDERR\n")
#     #     for line in host_output.stderr:
#     #         logfile.write(line)
    
# def runNHNT(device):
#     ipAddress = device + '.local'

#     os.makedirs("logs/" + device, exist_ok = True)
#     t = datetime.datetime.now()
#     filename = "logs/" + device + "/" + t.strftime("%m_%d_%H_%M_%S") + ".txt"
#     logfile = open(filename, "w")

#     client = SSHClient()
#     client.load_system_host_keys()
#     client.connect(ipAddress, username=device, password=device)
    
#     cmd = "if test -d /home/" + device + "/Documents/NHNTBerggruen; then echo \"1\"; fi"
#     ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(cmd)
#     output = ssh_stdout.readlines()
    
#     if output[0].strip() == '1':
#         print("starting NHNT on " + device)
#         input("press ENTER to continue operation or ctrl-C to cancel")

#         cmd = "cd /home/" + device + "/Documents/NHNTBerggruen; python3 python/nhnt.py"

#         ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(cmd)

#         logfile.write("--------------------------------\n")
#         logfile.write("STDOUT\n")
#         for line in ssh_stdout.readlines():
#             logfile.write(line)

#         errorCount = 0
#         logfile.write("\n--------------------------------\n")
#         logfile.write("STDERR\n")
#         for line in ssh_stderr.readlines():
#             logfile.write(line)
#             errorCount += 1

#         if errorCount != 0:
#             print("ERROR: there was an error running the command!")
#             print("ERROR: please check logfile " + filename + " for more info")
        
#     else:
#         print("could not find the program, please rerun this using: -c update")
 
#     # TODO get logfile from device with conversation

#     client.close()

def parseArguments():
    # parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--cmd', '-c', default='run', choices=['config', 'run', 'update'], help="specify the command you would like to use, defaults to run")
    parser.add_argument('--devices', '-d', nargs='+', default='all', choices=['all', 'se1', 'se2', 'se3', 'se4', 'se5'], help="specify which devices to use, defaults to all")
    args = parser.parse_args()

    if args.devices[0] == 'all':
        devices = ['se1', 'se2', 'se3', 'se4', 'se5']
    else:
        devices = args.devices

    return devices, args.cmd

def main():

    devices, cmd = parseArguments()

    # copy config files
    if cmd == 'config':
        print("would you like to copy CONFIG files to " + str(devices) + "?")
        input("press ENTER to continue operation or ctrl-C to cancel")

        # iterate across all devices executing command
        for pi in devices:
            copyConfigFile(pi)

    # update git repo
    elif cmd == 'update':
        for pi in devices:
            updateGitRepo(pi)

    # run the stuff
    elif cmd == 'run':
        print("this doesn't work, stop trying")
        # runParallel(devices)
        # processes = []

        # with Pool(len(devices)) as p:
            # pr
        # for pi in devices:
            # processes.append(Process(runNHNT))
            # runNHNT(pi)

    else:
        print("not sure how we got here ooops!")
        exit()



if __name__ == "__main__":
    main()
