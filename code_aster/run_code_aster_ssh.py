"""
Script to launch a simple code-aster, in SSH mode, task on Qarnot's platform
"""

import qarnot
from qarnot.scheduling_type import OnDemandScheduling, FlexScheduling, ReservedScheduling
import os

# =============================== Setup Variables =============================== #

# =============================== Mandatory Variables =============================== #
CLIENT_TOKEN=os.getenv("QARNOT_TOKEN")         # If your token is in a .env. You can also execute, in your terminal, 'export QARNOT_TOKEN='your_token''.
PROFILE="code-aster-ssh"                           # Qarnot profile to use. Use "code-aster" to not have interenet acces and no ssh connectivity.
SSH_PUBLIC_KEY="YOUR_SSH_PUBLIC_KEY"           # Your SSH public key to acces your remote Qarnot cluster.

NB_INSTANCES = 1                               # Number of instances in your cluster.
CODE_ASTER_VERSION="16.7"                      # Code_Aster version

DIR_TO_SYNC = 'etudepoutre2D'                  # Exact name for your model's directory.
INPUT_BUCKET_NAME =  f"{DIR_TO_SYNC}-in"    
OUTPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-out"
TASK_NAME = f"RUN test Code_Aster - {DIR_TO_SYNC}" 

CA_EXPORT_FILE = "etudepoutre2D.export"        # Your Code_Aster .export file. 

INSTANCE_TYPE = 'xeon'                         # "xeon" is the default choice. Otherwise, put "epyc".
if INSTANCE_TYPE == 'xeon':
    SETUP_CLUSTER_NB_SLOTS = 26                # Number of processes per node in the mpihost file. "26" is optimal for xeon.
    instance_type="28c-128g-intel-dual-xeon2680v4-ssd"
elif INSTANCE_TYPE == 'epyc':
    SETUP_CLUSTER_NB_SLOTS = 94                # Number of processes per node in the mpihost file. "94" is optimal for epyc.       
    instance_type = "96c-512g-amd-epyc9654-ssd"

# =============================== Optional Variables =============================== #
#OUTPUT_FILTER = r"(?i).*\.txt$"               # Optional : Regex filter to select which outputfiles you want to keep. Here, an example with .txt
#SYNC_FILTER = OUTPUT_FILTER                   # Optional : Regex filter to select which files are copied during your snapshots

POST_PROCESSING_CMD = ""                       # Optional : Post processing command, ran after simulation if not empty.

# =============================== TASK CONFIGURATION =============================== #

# =============================== Mandatory Configuration =============================== #

# Create a connection, from which all other objects will be derived
conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

# Print available profiles with you account
print([profile for profile in conn.profiles_names() if 'code-aster' in profile])

# Create task
task = conn.create_task(TASK_NAME, PROFILE, NB_INSTANCES)

# Create the input bucket and synchronize with a local folder
input_bucket = conn.create_bucket(INPUT_BUCKET_NAME)
input_bucket.sync_directory(DIR_TO_SYNC)
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
output_bucket = conn.create_bucket(OUTPUT_BUCKET_NAME)
task.results = output_bucket

# Required settings
task.constants["CA_EXPORT_FILE"] = CA_EXPORT_FILE
task.constants['DOCKER_TAG'] = CODE_ASTER_VERSION
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

# Settings to copy from simulation directory (/share) to bucket linked directory (/job).
##  /job  is the dir where buckets are downloaded at start and uploaded to your bucket by the snapshots.
## /share is the dir where the simulation is executing. Fastest disk and shared directories between nodes.

#task.constants['LOCAL_FILES_COPY_FEATURE'] = "true"       # Set to true to upload periodically from the /share folder
#task.constants['LOCAL_FILES_COPY_INTERVAL_SEC'] = "1800"  # Set the upload interval in seconds
#task.constants['LOCAL_FILES_COPY_REGEX'] = ""             # Filters the files to upload, leave empty to upload everything

# =============================== LAUNCH YOUR TASK ! =============================== #

# You are ready to submit your task!
print('Submitting task on Qarnot')
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
            cmd = f"ssh -o StrictHostKeyChecking=no root@{ssh_forward_host} -p {ssh_forward_port}"
            print(cmd)
            SSH_TUNNELING_DONE = True

    # Display errors on failure
    if task.state == 'Failure':
        print(f"** Errors: {task.errors[0]}")
        SSH_TUNNELING_DONE = True
