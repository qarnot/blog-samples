"""
Script to launch a detailed Altair task, in SSH mode, on Qarnot's platform
"""


import qarnot
from qarnot.scheduling_type import OnDemandScheduling, FlexScheduling, ReservedScheduling
import os

from dotenv import load_dotenv
load_dotenv()

# =============================== SETUP VARIABLES =============================== #

# =============================== Mandatory Variables =============================== #

CLIENT_TOKEN=os.getenv("QARNOT_TOKEN")         # If your token is in a .env. You can also execute, in your terminal, 'export QARNOT_TOKEN='your_token''.
PROFILE="YOUR_PROFILE_SSH"                     # Example : 'altair-hyperworks-qarnot-vnc-wan'
SSH_PUBLIC_KEY="YOUR_SSH_PUBLIC_KEY"
#ALM_HHWU_TOKEN='YOUR_ALM_HHWU_TOKEN'           # If your licence is hosted on Altair-One 

NB_INSTANCES = 1                               # Number of instances in your cluster.
ALTAIR_VERSION="2024.1"                        # Altair Hyperwork 2024.1 
                        
DIR_TO_SYNC = 'altair_block_test'              # Exact name for your model's directory containg your .rad (Radioss) or .fem (Optistruct) model
INPUT_BUCKET_NAME =  f"{DIR_TO_SYNC}-in"    
OUTPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-out"
TASK_NAME = f"RUN test Altair - {DIR_TO_SYNC}" 

INSTANCE_TYPE = 'xeon'                         # xeon is the default choice. Otherwise, put 'epyc'.
if INSTANCE_TYPE == 'xeon':
    SETUP_CLUSTER_NB_SLOTS = 26
    instance_type="28c-128g-intel-dual-xeon2680v4-ssd" # Number of processes per node in the mpihost file. "24" is optimal for xeon.
elif INSTANCE_TYPE == 'epyc':
    SETUP_CLUSTER_NB_SLOTS = 94                   # Number of processes per node in the mpihost file. "94" is optimal for epyc.       
    instance_type = "96c-512g-amd-epyc9654-ssd"

# =============================== Optional Variables =============================== #

#OUTPUT_FILTER = r"(?i).*\.h3d$"                # Optional : Regex filter to select which outputfiles you want to keep. Here, an example with .h3d
#SYNC_FILTER = OUTPUT_FILTER                    # Optional : Regex filter to select which files are copied during your snapshots

USE_MAX_EXEC_TIME = "false"                    # Optional : Set to true to activate the configuration of maximum cluster execution time. 
MAX_EXEC_TIME = "8h"                           # Optional : Maximum cluster execution time (ex: '8h', 'h' for hours or 'd' for days) if USE_MAX_EXEC_TIME is true" 

POST_PROCESSING_CMD = ""                       # Optional : Post processing command, ran after simulation if not empty.
                                               # Use '$optistruct --help' or '$radioss --help' on ssh to understand all the possible flags, or contact our team to help you optimize your case.

# =============================== TASK CONFIGURATION =============================== #

# =============================== Mandatory Configuration =============================== #

# Create a connection, from which all other objects will be derived
conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

# Print available profiles with you account
avail_profile = [profile for profile in conn.profiles_names() if 'altair' in profile]
print(f'Available profiles for your account : {avail_profile}')

# Create task
task = conn.create_task(TASK_NAME, PROFILE, NB_INSTANCES)

# Insert your Altair One token to access your licence, if applicable
#task.constants['ALM_HHWU_TOKEN'] = ALM_HHWU_TOKEN

# Create the input bucket and synchronize with a local folder
input_bucket = conn.create_bucket(INPUT_BUCKET_NAME)
input_bucket.sync_directory(DIR_TO_SYNC)
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
output_bucket = conn.create_bucket(OUTPUT_BUCKET_NAME)
task.results = output_bucket

# Specify Altair version, SSH, number of cores per node, etc. 
task.constants['DOCKER_TAG'] = ALTAIR_VERSION 
task.constants['DOCKER_SSH'] = SSH_PUBLIC_KEY
task.constants["SETUP_CLUSTER_NB_SLOTS"] = SETUP_CLUSTER_NB_SLOTS
task.hardware_constraints = [qarnot.hardware_constraint.SpecificHardware(instance_type)]

# Scheduling type
task.scheduling_type=OnDemandScheduling()
# task.scheduling_type=FlexScheduling()
# task.scheduling_type=ReservedScheduling()               # If your company has reserved nodes
# task.targeted_reserved_machine_key = instance_type      # Uncomment if your company has reserved nodes


# =============================== Optional Configuration =============================== #

#task.snapshot(1800)                                     # Define interval time in seconds when /job will be saved to your bucket.
#task.snapshots_whitelist  = SYNC_FILTER
#task.results_whitelist  = OUTPUT_FILTER

#task.constants['POST_PROCESSING_CMD'] = POST_PROCESSING_CMD
#task.constants['USE_SIMULATION_MAXIMUM_EXECUTION_TIME'] = USE_MAX_EXEC_TIME
#task.constants['SIMULATION_MAXIMUM_EXECUTION_TIME'] = MAX_EXEC_TIME

# Settings to copy from simulation directory (/share) to bucket linked directory (/job).
##  /job  is the dir where buckets are downloaded at start and uploaded to your bucket by the snapshots.
## /share is the dir where the simulation is executing. Fastest disk and shared directories between nodes.

#task.constants['LOCAL_FILES_COPY_FEATURE'] = "true"       # Set to true to upload periodically from the /share folder
#task.constants['LOCAL_FILES_COPY_INTERVAL_SEC'] = "1800"  # Set the upload interval in seconds
#task.constants['LOCAL_FILES_COPY_REGEX'] = ""             # Filters the files to upload, leave empty to upload everything


# =============================== LAUNCH YOUR TASK ! =============================== #

task.submit()
print('Submitting task on Qarnot')

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
            cmd = f"ssh -o StrictHostKeyChecking=no root@{ssh_forward_host} -p {ssh_forward_port}"
            print(cmd)
            SSH_TUNNELING_DONE = True

    # Display errors on failure
    if task.state == 'Failure':
        print(f"** Errors: {task.errors[0]}")
        SSH_TUNNELING_DONE = True

# =============================== DOWNLOAD RESULTS =============================== #

# Download results when "Success" state is reached
SUCCESS = False
while not SUCCESS:
    # Wait for the task to be FullyExecuting
    if task.state == 'Success':
        task.download_results(OUTPUT_BUCKET_NAME, True)
        SUCCESS = True







