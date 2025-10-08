"""Script to run a LS-DYNA sample computation on Qarnot cloud"""

import qarnot
from qarnot.scheduling_type import OnDemandScheduling
import os

# =============================== Setup Variables =============================== #
# To change
CLIENT_TOKEN="MY_SECRET_TOKEN"                 # To retrieve on tasq.qarnot.com/settings/access-token
CLIENT_TOKEN=os.getenv("QARNOT_TOKEN")         # Using an env variable
PROFILE="YOUR_PROFILE"                         # Example : 'ls-dyna-qarnot-vnc-wan'

# Change the following if needed
VNC_PASSWORD = ""                              # Password for the VNC server. Must be less than 8 chars.
NB_INSTANCES = 1                               # Number of instances in your cluster.
ANSYS_VERSION="2025R2"                         # LS-DYNA 14.1 -> 2025R2

DIR_TO_SYNC = "dyna_drop_test"                 # This is the local directory that will be uploaded to you input bucket
INPUT_BUCKET_NAME =  f"{DIR_TO_SYNC}-in"
OUTPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-out"
TASK_NAME = f"RUN test LS-DYNA - {DIR_TO_SYNC}" 

DYNA_CMD = "mpiexec -np 1 lsdyna_sp_mpp.e i=EXP_SC_DROP.key memory=1200M" # More info bellow

# =============================================================================== #

# Create a connection, from which all other objects will be derived
conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

# Print available profiles with you account
print([profile for profile in conn.profiles_names() if 'dyna' in profile])

# Create task
task = conn.create_task(TASK_NAME, PROFILE, NB_INSTANCES)

# Create the input bucket and synchronize with a local folder
input_bucket = conn.create_bucket(INPUT_BUCKET_NAME)
input_bucket.sync_directory(DIR_TO_SYNC)
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
output_bucket = conn.create_bucket(OUTPUT_BUCKET_NAME)
task.results = output_bucket

# IMAGE
task.constants['DOCKER_TAG'] = ANSYS_VERSION

# CMD - To use with lsdyna_sp or lsdyna_dp
## SMP : lsdyna_sp.e i=input.k ncpu=1 memory=1200M
## MPP : mpiexec -np 1 lsdyna_sp_mpp.e i=input.k memory=1200M
## Leave it empty to launch your simulaiton through lsrun on web desktop 
task.constants["MECHANICAL_CMD"] = DYNA_CMD

# VNC - set to tru to enable desktop visualization
task.constants["VNC"] = "true"
# VNC_PASSWORD - Password for the VNC server. Must be less than 8 chars (additional ones will be ignored).
# If none, a random one will be assigned and log in task's stdout.
task.constants["VNC_PASSWORD"] = VNC_PASSWORD


# Optional parameters
# Number of processes per node in the mpihost file, e.g. "26" out of 28 cores.
# task.constants['SETUP_CLUSTER_NB_SLOTS'] = "26"

# Define interval time in seconds when /job will be saved to your bucket.
# task.snapshot(1800)

# Settings to copy from simulation directory (/share) to bucket linked directory (/job).
##  /job  is the dir where buckets are downloaded at start and uploaded to your bucket by the snapshots.
## /share is the dir where the simulation is executing. Fastest disk and shared directories between nodes.
task.constants['LOCAL_FILES_COPY_FEATURE'] = "true"       # Set to true to upload periodically from the /share folder
task.constants['LOCAL_FILES_COPY_INTERVAL_SEC'] = "1800"  # Set the upload interval in seconds
task.constants['LOCAL_FILES_COPY_REGEX'] = ""             # Filters the files to upload, leave empty to upload everything


# Scheduling type
# task.scheduling_type=OnDemandScheduling()
# task.scheduling_type=ReservedScheduling() # If your company has reserved nodes


task.submit()


# ---------- Optional ----------
## -- To comment delete if not usefull
# Print VNC web link
LAST_STATE = ''
VNC_UP = False
while not VNC_UP:
    if task.state != LAST_STATE:
        LAST_STATE = task.state
        print(f"** {LAST_STATE}")

    # Wait for the task to be FullyExecuting
    if task.state == 'FullyExecuting':
        # If the ssh connexion was not done yet and the list active_forward is available (len!=0)
        forward_list = task.status.running_instances_info.per_running_instance_info[0].active_forward
        if not VNC_UP and len(forward_list) != 0:
            for forward in forward_list:
                forward_host = forward.forwarder_host
                if forward_host != "gateway.qarnotservices.com":
                    print(f"Desktop link : https://{forward_host}/vnc.html?password={VNC_PASSWORD}\n")
                    VNC_UP = True


    # Display errors on failure
    if task.state == 'Failure':
        print(f"** Errors: {task.errors[0]}")
        VNC_UP = True

# Hang until success and then download results
OUTPUT_DIR = "dyna_drop_test_out"
SUCCESS = False
while not SUCCESS:
    # Wait for the task to be FullyExecuting
    if task.state == 'Success':
        task.download_results(OUTPUT_DIR, True)
        SUCCESS = True
