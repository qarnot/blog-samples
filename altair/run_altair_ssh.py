import qarnot
from qarnot.scheduling_type import OnDemandScheduling, FlexScheduling, ReservedScheduling
import os

from dotenv import load_dotenv
load_dotenv()

# =============================== Setup Variables =============================== #

CLIENT_TOKEN="MY_SECRET_TOKEN"                 # To retrieve on your HPC or Tasq account
CLIENT_TOKEN=os.getenv("QARNOT_TOKEN")         # Using an env variable
PROFILE="YOUR_PROFILE_SSH"                     # Example : 'altair-hyperworks-qarnot-vnc-wan'
SSH_PUBLIC_KEY="YOUR_SSH_PUBLIC_KEY"

NB_INSTANCES = 2                               # Number of instances in your cluster.
ALTAIR_VERSION="2024.1"                        # Altair Hyperwork 2024.1 
                        
DIR_TO_SYNC = 'altair_block_test'              # Exact name for your model's directory (for example "model_dir", if Radioss) or file with extension (for exemple "model.fem", if Optistruct)
INPUT_BUCKET_NAME =  f"{DIR_TO_SYNC}-in"    
OUTPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-out"
OUTPUT_FILTER = r"(?i).*\.3ds$"                # Optional : Regex filter to select which outputfiles you want to keep. Here, an example with .h3d

TASK_NAME = f"RUN test Altair - {DIR_TO_SYNC}" 
USE_MAX_EXEC_TIME = "false"                    # Optional : Set to true to activate the configuration of maximum cluster execution time. 
MAX_EXEC_TIME = "8h"                           # Optional : Maximum cluster execution time (ex: '8h', 'h' for hours or 'd' for days) if USE_MAX_EXEC_TIME is true" 

INSTANCE_TYPE = 'Xeon'                         # Xeon is the default choice. Otherwise, put 'Epyc'.
if INSTANCE_TYPE == 'Xeon':
    SETUP_CLUSTER_NB_SLOTS = 26
    instance_type="28c-128g-intel-dual-xeon2680v4-ssd" # Number of processes per node in the mpihost file. "24" is optimal for xeon.
elif INSTANCE_TYPE == 'EPYC':
    SETUP_CLUSTER_NB_SLOTS = 94                   # Number of processes per node in the mpihost file. "94" is optimal for xeon.       
    instance_type = "96c-512g-amd-epyc9654-ssd"

POST_PROCESSING_CMD = ""                       # Optional : Post processing command, ran after simulation if not empty.
                                               # Use '$optistruct --help' or '$radioss --help' on ssh to understand all the possible flags, or contact our team to help you optimize your case.

# =============================== Lauching a Task =============================== #

# Create a connection, from which all other objects will be derived
conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

# Print available profiles with you account
print([profile for profile in conn.profiles_names() if 'altair' in profile])

# Create task
task = conn.create_task(TASK_NAME, PROFILE, NB_INSTANCES)

# Create the input bucket and synchronize with a local folder
input_bucket = conn.create_bucket(INPUT_BUCKET_NAME)
input_bucket.sync_directory(DIR_TO_SYNC)
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
output_bucket = conn.create_bucket(OUTPUT_BUCKET_NAME)
task.results = output_bucket
task.results_whitelist  = OUTPUT_FILTER

# Required settings
## Historically, at Qarnot, the Altair Hyperworks Suite was named "Altair Mechanical" at Qarnot. We kept the variable value, but don't worry - It is Altair Hyperworks!
task.constants['DOCKER_TAG'] = ALTAIR_VERSION
task.constants["SETUP_CLUSTER_NB_SLOTS"] = SETUP_CLUSTER_NB_SLOTS
task.hardware_constraints = [qarnot.hardware_constraint.SpecificHardware(instance_type)]

# Optional settings
task.constants['POST_PROCESSING_CMD'] = POST_PROCESSING_CMD
task.constants['USE_SIMULATION_MAXIMUM_EXECUTION_TIME'] = USE_MAX_EXEC_TIME
task.constants['SIMULATION_MAXIMUM_EXECUTION_TIME'] = MAX_EXEC_TIME

# Settings to copy from simulation directory (/share) to bucket linked directory (/job).
##  /job  is the dir where buckets are downloaded at start and uploaded to your bucket by the snapshots.
## /share is the dir where the simulation is executing. Fastest disk and shared directories between nodes.
task.constants['LOCAL_FILES_COPY_FEATURE'] = "true"       # Set to true to upload periodically from the /share folder
task.constants['LOCAL_FILES_COPY_INTERVAL_SEC'] = "1800"  # Set the upload interval in seconds
task.constants['LOCAL_FILES_COPY_REGEX'] = ""             # Filters the files to upload, leave empty to upload everything

# Scheduling type
task.scheduling_type=OnDemandScheduling()
# task.scheduling_type=FlexScheduling()
# task.scheduling_type=ReservedScheduling()               # If your company has reserved nodes
# task.targeted_reserved_machine_key = instance_type      # Uncomment if your company has reserved nodes

# You are ready to submit your task!
task.submit()





