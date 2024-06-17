#!/usr/bin/env python3

# Import the Qarnot SDK
import sys
import argparse
import qarnot
import subprocess

# Connect to the Qarnot platform
conn = qarnot.Connection(client_token = '<<<MY_SECRET_TOKEN>>>')

# Create a task
task = conn.create_task('Hello World - SSH-Spark', 'docker-cluster-network-ssh', 3)

# Create a resource bucket and add input files
input_bucket = conn.create_bucket('ssh-spark-in')
input_bucket.sync_directory('input/')

# Attach the bucket to the task
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
task.results = conn.create_bucket('ssh-spark-out')

# Task constants are the main way of controlling a task's behaviour
task.constants['DOCKER_SSH'] = '<<<PUBLIC_SSH_KEY>>>'
task.constants['DOCKER_REPO'] = "qarnotlab/spark"
task.constants['DOCKER_TAG'] = "v3.1.2"
task.constants['DOCKER_CMD_MASTER'] = "/bin/bash \
                                      /opt/start-master.sh ${INSTANCE_COUNT} /opt/log.sh"
task.constants['DOCKER_CMD_WORKER'] = "/bin/bash -c '/opt/start-worker.sh /opt/log.sh && sleep infinity'"

# Submit the task to the Api, that will launch it on the cluster
task.submit()
error_happened = False

# Initial values for forward port and ssh tunneling bool
ssh_forward_port = None
ssh_tunneling_done = False

# Get optional terminal app name from argument
parser = argparse.ArgumentParser()
parser.add_argument("--terminal", type=str,
                    help="Unix terminal app to be used for ssh connexion", 
                    default = 'gnome-terminal', required=False)
args = parser.parse_args()

# If not provided by the user it will be set to gnome-terminal by default
terminal = args.terminal

done = False
while not done:

    # Wait for the task to be FullyExecuting
    if task.state == 'FullyExecuting' :
    
        # If the ssh connexion was not done yet and the list active_forward is available (len!=0)
        active_forward = task.status.running_instances_info.per_running_instance_info[0].active_forward
        if not ssh_tunneling_done and len(active_forward)!=0:
            ssh_forward_port = active_forward[0].forwarder_port

            # Once the port has been fetched, spawn a new terminal with the ssh command
            cmd = 'ssh -L <<<PORT>>>:localhost:6060 -o StrictHostKeyChecking=no root@forward01.qarnot.net -p '+ str(ssh_forward_port)

            # if --terminal was set to off, bypass this and connect manually with ssh
            if terminal != 'off':
                ssh_cmd = [terminal,'-e',cmd]
                subprocess.call(ssh_cmd)
            else:
                print("\n** Run this command in your terminal to connect via ssh **\n", cmd,
                        "\n**********************************************************")

            # set this var to True in order to not run ssh again
            ssh_tunneling_done = True
            
    # sync ouptput files of the qarnot machine with the bucket,
    # then the bucket with your local directory
    task.instant()
    done = task.wait(5)
    task.download_results('outputs')
