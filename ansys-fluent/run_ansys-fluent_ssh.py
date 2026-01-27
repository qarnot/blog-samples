#!/usr/bin/env python3
"""
Script to launch a detailed Fluent task, in Batch mode, on Qarnot's platform
"""

import qarnot
from qarnot.scheduling_type import OnDemandScheduling, FlexScheduling, ReservedScheduling

import os

# =============================== SETUP VARIABLES =============================== #
# ================================ CHANGE NEEDED ================================ #

CLIENT_TOKEN=os.getenv("QARNOT_TOKEN")         # If your token is in a .env. You can also execute, in your terminal, 'export QARNOT_TOKEN='your_token''.
CLIENT_TOKEN="MY_SECRET_TOKEN"                 # To comment or change
PROFILE="ansys-fluent-e-corp"                  # Set to your profile 
SSH_PUBLIC_KEY="YOUR_SSH_PUBLIC_KEY"

# =============================================================================== #
DIR_TO_SYNC = 'aircraft'                       # Name for your model's directory
INPUT_BUCKET_NAME =  f"{DIR_TO_SYNC}-in"    
OUTPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-out"
TASK_NAME = f"RUN case - {DIR_TO_SYNC}" 

FLUENT_VERSION = "2025R2"
NB_INSTANCES = 2                               # Number of instances in your cluster. Xeon 28cores are the default instances.
FLUENT_CMD = ""       

INSTANCE_TYPE = 'xeon'                         # xeon is the default choice. Otherwise, put 'epyc'.
if INSTANCE_TYPE == 'xeon':
    SETUP_CLUSTER_NB_SLOTS = 26
    instance_type="28c-128g-intel-dual-xeon2680v4-ssd" # Number of processes per node in the mpihost file. "24" is optimal for xeon.
elif INSTANCE_TYPE == 'epyc':
    SETUP_CLUSTER_NB_SLOTS = 94                # Number of processes per node in the mpihost file. "94" is optimal for epyc.       
    instance_type = "96c-512g-amd-epyc9654-ssd"

# =============================== Optional Variables =================================== #

# SNAPSHOT_FILTER = r"^.*\.dat(?:\.h5|\.gz)?$"      # Optional : Filters for data files only to track simulation progress (increments).
SNAPSHOT_FILTER = ""
# RESULTS_FILTER = r"^.*\.(dat|trn)(?:\.h5|\.gz)?$" # Optional : Collects solver data and logs; excludes .cas files as they are already available locally.
RESULTS_FILTER = ""

USE_MAX_EXEC_TIME = "false"                    # Optional : Set to true to activate the configuration of maximum cluster execution time. 
MAX_EXEC_TIME = "1h"                           # Optional : Maximum cluster execution time (ex: '8h', 'h' for hours or 'd' for days) if USE_MAX_EXEC_TIME is true" 

POST_PROCESSING_CMD = ""                       # Optional : Post processing command, ran after simulation if not empty.
WAIT_FOR_LICENSE_AVAILABILITY = "false"        # Optional : Set to true to add a blocking wait at the beginning of the simulation when licenses are overused.

# =============================== TASK CONFIGURATION =============================== #

# Create a connection
conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

# Create a task
task = conn.create_task(TASK_NAME, PROFILE, NB_INSTANCES)

# Create the input bucket and synchronize with a local folder
input_bucket = conn.create_bucket(INPUT_BUCKET_NAME)
input_bucket.sync_directory(DIR_TO_SYNC)  # Replace with absolute path to your folder if needed
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
output_bucket = conn.create_bucket(OUTPUT_BUCKET_NAME)
task.results = output_bucket

# Fluent Command
task.constants['FLUENT_CMD'] = FLUENT_CMD
task.constants["DOCKER_TAG"] = FLUENT_VERSION
task.constants['DOCKER_SSH'] = SSH_PUBLIC_KEY
task.constants["SETUP_CLUSTER_NB_SLOTS"] = SETUP_CLUSTER_NB_SLOTS
task.hardware_constraints = [qarnot.hardware_constraint.SpecificHardware(instance_type)]

# Scheduling type
task.scheduling_type=OnDemandScheduling()
# task.scheduling_type=FlexScheduling()
# task.scheduling_type=ReservedScheduling()               # If your company has reserved nodes
# task.targeted_reserved_machine_key = instance_type      # Uncomment if your company has reserved nodes

# =============================== Optional Configuration =============================== #

task.snapshot(1800)                                       # Define interval time in seconds when /job will be saved to your bucket.
task.snapshot_whitelist = SNAPSHOT_FILTER
task.results_whitelist  = RESULTS_FILTER

task.constants['POST_PROCESSING_CMD'] = POST_PROCESSING_CMD
task.constants['USE_SIMULATION_MAXIMUM_EXECUTION_TIME'] = USE_MAX_EXEC_TIME
task.constants['SIMULATION_MAXIMUM_EXECUTION_TIME'] = MAX_EXEC_TIME

task.constants['WAIT_FOR_LICENSE_AVAILABILITY'] = WAIT_FOR_LICENSE_AVAILABILITY

# =============================== LAUNCH YOUR TASK ! =================================== #

task.submit()
print('Task submitted on Qarnot')

# The following will print the state of the task to your console
# It will also print the command to connect through ssh to the task when it's ready, and download your results to your bucket when your task is Done/Succesfull.
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
    
     # Wait for the task to be FullyExecuting
    if task.state == 'Success':
        print(f"** {LAST_STATE}")
        task.download_results(OUTPUT_BUCKET_NAME, True)
        SSH_TUNNELING_DONE = True

    # Display errors on failure
    if task.state == 'Failure':
        print(f"** Errors: {task.errors[0]}")
        SSH_TUNNELING_DONE = True
    

