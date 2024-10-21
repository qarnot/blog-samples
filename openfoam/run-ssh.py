#!/usr/bin/env python3

# Import the Qarnot SDK
import qarnot
import os

# Create a connection, from which all other objects will be derived
# Enter client token here

conn = qarnot.connection.Connection(client_token="MY_SECRET_TOKEN")

# -------------------------------------------------------------------------- #
NB_NODES = 2
DOCKER_SSH = '<MY_SSH_KEY>'
OPENFOAM_VERSION = "v2106"
# -------------------------------------------------------------------------- #

# Create a task
task = conn.create_task("OpenFOAM-SSH Test",
                        "openfoam-ssh", NB_NODES)


# Create the input bucket and synchronize with a local folder
# Insert a local folder directory
input_bucket = conn.create_bucket("openfoam-in")
input_bucket.sync_directory("input")

# Attach the bucket to the task
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
task.results = conn.create_bucket("openfoam-out")

task.constants['DOCKER_TAG'] = OPENFOAM_VERSION
task.constants['DOCKER_SSH'] = DOCKER_SSH

# Define checkpoint
task.snapshot(60)

# Submit the task
task.submit()

# The following will print the state of the task to your console
# It will also print the command to connect through ssh to the task when it's ready
LAST_STATE = ''
SSH_TUNNELING_DONE = False
while not SSH_TUNNELING_DONE:
    if task.state != LAST_STATE:
        LAST_STATE = task.state
        print(f"** {LAST_STATE}")

    # Wait for the task to be FullyExecuting
    if task.state == 'FullyExecuting':
        # If the ssh connexion was not done yet and the list active_forward is available (len!=0)
        forward_list = task.status.running_instances_info.per_running_instance_info[0].active_forward
        if not SSH_TUNNELING_DONE and len(forward_list) != 0:
            ssh_forward_port = forward_list[0].forwarder_port
            ssh_forward_host = forward_list[0].forwarder_host
            cmd = f"ssh -o StrictHostKeyChecking=no openfoam@{ssh_forward_host} -p {ssh_forward_port}"
            print(cmd)
            SSH_TUNNELING_DONE = True

    # Display errors on failure
    if task.state == 'Failure':
        print(f"** Errors: {task.errors[0]}")
        SSH_TUNNELING_DONE = True
