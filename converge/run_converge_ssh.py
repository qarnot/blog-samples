"""
Script to launch a detailed Converge task, in SSH mode, on Qarnot's platform
"""

import qarnot
from qarnot.scheduling_type import OnDemandScheduling, FlexScheduling, ReservedScheduling

# =============================== SETUP VARIABLES =================================== #

# =============================== Mandatory Variables =============================== #

CLIENT_TOKEN="YOUR_QARNOT_TOKEN"                   # You can also insert your token in a .env, export it in your terminal or use the .conf file directly. 
PROFILE="YOUR_PROFILE"                             # Example : 'converge-qarnot'
SSH_PUBLIC_KEY="YOUR_SSH_PUBLIC_KEY"

NB_INSTANCES = 2                                   # Number of instances

CONVERGE_VERSION="5.0.2"                           # Here, Converge 5.0.2

MODEL_NAME = 'SI8_engine_intake_flowbench_2_mm_steady_RANS' # Name for your model's directory inside 'input_converge'
INPUT_BUCKET_NAME =  "CONVERGE-in"    
OUTPUT_BUCKET_NAME = "CONVERGE-out"
TASK_NAME = "RUN test - CONVERGE" 

INSTANCE_TYPE = 'xeon'                              # xeon is the default choice. Otherwise, put 'epyc'.
if INSTANCE_TYPE == 'xeon':
    NB_PROCESSES = 26                               # Number of processes per node in the mpihost file. "24" is optimal for xeon.
    instance_type="28c-128g-intel-dual-xeon2680v4-ssd" 
elif INSTANCE_TYPE == 'epyc':
    NB_PROCESSES = 94                               # Number of processes per node in the mpihost file. A maximum of "94" is suggested for epyc.       
    instance_type = "96c-512g-amd-epyc9654-ssd"

# =============================== Optional Variables =============================== #

#OUTPUT_FILTER = "^.*\.json$"                      # Optional : Regex filter to select which outputfiles you want to keep. Here, an example with .json
#SNAPSHOT_FILTER = "^.*\.json$"                    # Optional : Regex filter to select which files are copied during your snapshots

USE_MAX_EXEC_TIME = "false"                         # Optional : Set to true to activate the configuration of maximum cluster execution time. 
MAX_EXEC_TIME = "8h"                                # Optional : Maximum cluster execution time (ex: '8h', 'h' for hours or 'd' for days) if USE_MAX_EXEC_TIME is true" 

POST_PROCESSING_CMD = ""                            # Optional : Post processing command, ran after simulation if not empty.

# =============================== TASK CONFIGURATION =============================== #

# =============================== Mandatory Configuration ========================== #

# Create a connection, from which all other objects will be derived
conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

# Print available profiles with you account
avail_profile = [profile for profile in conn.profiles_names() if 'converge' in profile]
print(f'Available profiles for your account : {avail_profile}')

# Create task
task = conn.create_task(TASK_NAME, PROFILE, NB_INSTANCES)

# Create the input bucket and synchronize with a local folder
# If needed, you can put the absolute path to your model`s directory instead of DIR_TO_SYNC
input_bucket = conn.create_bucket(INPUT_BUCKET_NAME)
input_bucket.sync_directory(MODEL_NAME)
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
output_bucket = conn.create_bucket(OUTPUT_BUCKET_NAME)
task.results = output_bucket

# Insert your SSH key
task.constants['DOCKER_SSH'] = SSH_PUBLIC_KEY

# Specify Converge version, SSH, number of processes, etc. 
task.constants['DOCKER_TAG'] = CONVERGE_VERSION 
task.constants['CONVERGE_INPUT_DIRECTORY_NAME'] = MODEL_NAME
task.constants['NB_PROCESSES'] = NB_PROCESSES
task.hardware_constraints = [qarnot.hardware_constraint.SpecificHardware(instance_type)]

# Scheduling type
task.scheduling_type=OnDemandScheduling()
# task.scheduling_type=FlexScheduling()
# task.scheduling_type=ReservedScheduling()               # If your company has reserved nodes
# task.targeted_reserved_machine_key = instance_type      # Uncomment if your company has reserved nodes


# =============================== Optional Configuration ============================== #

#task.snapshot(900)                                       # Define interval time in seconds when /job will be saved to your bucket.
#task.snapshots_whitelist  = SNAPSHOT_FILTER
#task.results_whitelist  = OUTPUT_FILTER

#task.constants['POST_PROCESSING_CMD'] = POST_PROCESSING_CMD
#task.constants['USE_SIMULATION_MAXIMUM_EXECUTION_TIME'] = USE_MAX_EXEC_TIME
#task.constants['SIMULATION_MAXIMUM_EXECUTION_TIME'] = MAX_EXEC_TIME

# ================================ LAUNCH YOUR TASK ! ================================= #

task.submit()
print('Submitting task on Qarnot')

# =============================== MONITORING AND RESULTS =============================== #

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

