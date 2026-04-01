
import qarnot
from qarnot.scheduling_type import OnDemandScheduling, FlexScheduling, ReservedScheduling
import os

from dotenv import load_dotenv
load_dotenv()

# =============================== SETUP VARIABLES =============================== #

# =============================== Mandatory Variables =============================== #

CLIENT_TOKEN=os.getenv("QARNOT_TOKEN")              # If your token is in a .env. You can also execute, in your terminal, 'export QARNOT_TOKEN='your_token''.
PROFILE="your-converge-profile"                     # Example : 'converge-qarnot'
SSH_PUBLIC_KEY="YOUR_SSH_PUBLIC_KEY"

NB_INSTANCES = 2                                    # Number of instances in your cluster.
CONVERGE_VERSION="5.0.2"                            # Converge 5.0.2, for example
                        
PATH_TO_DIR = 'path/to/your/input'                  # Path to your model's directory. 
DIR_TO_SYNC = 'wind_test'                           # Exact name for your model's directory, at the same level from where you will launch the task
INPUT_BUCKET_NAME =  f"{DIR_TO_SYNC}-in"    
OUTPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-out"
TASK_NAME = f"RUN test Converge - {DIR_TO_SYNC}" 

INSTANCE_TYPE = 'xeon'                              # xeon is the default choice. Otherwise, put 'epyc'.
if INSTANCE_TYPE == 'xeon':
    SETUP_CLUSTER_NB_SLOTS = 26
    instance_type="28c-128g-intel-dual-xeon2680v4-ssd" # Number of processes per node in the mpihost file. "24" is optimal for xeon.
elif INSTANCE_TYPE == 'epyc':
    SETUP_CLUSTER_NB_SLOTS = 94                     # Number of processes per node in the mpihost file. "94" is optimal for xeon.       
    instance_type = "96c-512g-amd-epyc9654-ssd"

# =============================== Optional Variables =============================== #

#OUTPUT_FILTER = r"(?i).*\.h3d$"                    # Optional : Regex filter to select which outputfiles you want to keep. Here, an example with .h3d
#SYNC_FILTER = OUTPUT_FILTER                        # Optional : Regex filter to select which files are copied during your snapshots

USE_MAX_EXEC_TIME = "false"                         # Optional : Set to true to activate the configuration of maximum cluster execution time. 
MAX_EXEC_TIME = "8h"                                # Optional : Maximum cluster execution time (ex: '8h', 'h' for hours or 'd' for days) if USE_MAX_EXEC_TIME is true" 

# =============================== TASK CONFIGURATION =============================== #

# =============================== Mandatory Configuration =============================== #

# Create a connection, from which all other objects will be derived
conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

# Print available profiles with you account
avail_profile = [profile for profile in conn.profiles_names() if 'converge' in profile]
print(f'Available profiles for your account : {avail_profile}')

# Create task
task = conn.create_task(TASK_NAME, PROFILE, NB_INSTANCES)

# Create the input bucket and synchronize with a local folder
input_bucket = conn.create_bucket(INPUT_BUCKET_NAME)
input_bucket.sync_directory(PATH_TO_DIR)
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
output_bucket = conn.create_bucket(OUTPUT_BUCKET_NAME)
task.results = output_bucket

# Calculate total amount of processes/cores for your simulation
task.constants['NB_PROCESSES'] = NB_INSTANCES * SETUP_CLUSTER_NB_SLOTS 

# Specify other task configurations
task.constants['DOCKER_SSH'] = SSH_PUBLIC_KEY
task.constants['CONVERGE_INPUT_DIRECTORY_NAME'] = DIR_TO_SYNC
task.constants['DOCKER_TAG'] = CONVERGE_VERSION
task.constants["SETUP_CLUSTER_NB_SLOTS"] = SETUP_CLUSTER_NB_SLOTS
task.hardware_constraints = [qarnot.hardware_constraint.SpecificHardware(instance_type)]

# Scheduling type
task.scheduling_type=OnDemandScheduling()
# task.scheduling_type=FlexScheduling()
# task.scheduling_type=ReservedScheduling()               # If your company has reserved nodes
# task.targeted_reserved_machine_key = instance_type      # Uncomment if your company has reserved nodes


# =============================== Optional Configuration =============================== #

#task.snapshot(50)
#task.snapshots_whitelist  = SYNC_FILTER
#task.results_whitelist  = OUTPUT_FILTER

#task.constants['USE_SIMULATION_MAXIMUM_EXECUTION_TIME'] = USE_MAX_EXEC_TIME
#task.constants['SIMULATION_MAXIMUM_EXECUTION_TIME'] = MAX_EXEC_TIME

# Settings to copy from simulation directory (/share) to bucket linked directory (/job).
##  /job  is the dir where buckets are downloaded at start and uploaded to your bucket by the snapshots.
## /share is the dir where the simulation is executing. Fastest disk and shared directories between nodes.

#task.constants['LOCAL_FILES_COPY_FEATURE'] = "true"       # Set to true to upload periodically from the /share folder
#task.constants['LOCAL_FILES_COPY_INTERVAL_SEC'] = "1800"  # Set the upload interval in seconds
#task.constants['LOCAL_FILES_COPY_REGEX'] = ""             # Filters the files to upload, leave empty to upload everything


# =============================== LAUNCH YOUR TASK ! =============================== #

print('Submitting task on Qarnot')
task.submit()
