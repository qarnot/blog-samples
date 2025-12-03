"""
Script to launch a detailed Openfoam task, in Batch mode, on Qarnot's platform
"""

import qarnot
from qarnot.scheduling_type import OnDemandScheduling, FlexScheduling, ReservedScheduling
import os

from dotenv import load_dotenv
load_dotenv()

# =============================== SETUP VARIABLES =============================== #

# =============================== Mandatory Variables =============================== #

CLIENT_TOKEN=os.getenv("QARNOT_TOKEN")         # If your token is in a .env. You can also execute, in your terminal, 'export QARNOT_TOKEN='your_token''.
PROFILE="openfoam"                        

NB_INSTANCES = 2                               # Number of instances in your cluster.
OPENFOAM_VERSION="v2412"                       # Openfoam v2412

PATH_TO_DIR = '/home/chloe.pilon/Documents/BENCH/Openfoam/motorBike-38'     # Path to your model's directory
DIR_TO_SYNC = 'motorBike-38'                    # Name for your model's directory
INPUT_BUCKET_NAME =  f"{DIR_TO_SYNC}-in"    
OUTPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-out"
TASK_NAME = f"RUN test Openfoam - {DIR_TO_SYNC}" 

OPENFOAM_CMD = "Allrun"    

INSTANCE_TYPE = 'xeon'                         # xeon is the default choice. Otherwise, put 'epyc'.
if INSTANCE_TYPE == 'xeon':
    SETUP_CLUSTER_NB_SLOTS = 26
    instance_type="28c-128g-intel-dual-xeon2680v4-ssd" # Number of processes per node in the mpihost file. "24" is optimal for xeon.
elif INSTANCE_TYPE == 'epyc':
    SETUP_CLUSTER_NB_SLOTS = 94                   # Number of processes per node in the mpihost file. "94" is optimal for epyc.       
    instance_type = "96c-512g-amd-epyc9654-ssd"

# =============================== Optional Variables =============================== #

SNAPSHOT_FILTER = r"log\..*"                   # Optional : Regex filter to select which outputfiles you want to keep. Here, an example with filtering .log
RESULTS_FILTER = r"log\..*"                     # Optional : Regex filter to select which files are copied during your snapshots

USE_MAX_EXEC_TIME = "false"                    # Optional : Set to true to activate the configuration of maximum cluster execution time. 
MAX_EXEC_TIME = "1h"                           # Optional : Maximum cluster execution time (ex: '8h', 'h' for hours or 'd' for days) if USE_MAX_EXEC_TIME is true" 

POST_PROCESSING_CMD = ""                       # Optional : Post processing command, ran after simulation if not empty.

# =============================== TASK CONFIGURATION =============================== #

# =============================== Mandatory Configuration =============================== #

# Create a connection, from which all other objects will be derived
conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)


# Create task
task = conn.create_task(TASK_NAME, PROFILE, NB_INSTANCES)

# Create the input bucket and synchronize with a local folder
input_bucket = conn.create_bucket(INPUT_BUCKET_NAME)
input_bucket.sync_directory(PATH_TO_DIR)
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
output_bucket = conn.create_bucket(OUTPUT_BUCKET_NAME)
task.results = output_bucket

# Specify Altair CMD, version, number of cores per node, etc. 
## Historically, at Qarnot, the Altair Hyperworks Suite was named "Altair Mechanical" at Qarnot. We kept the variable value, but don't worry - It is Altair Hyperworks!
task.constants['RUN_SCRIPT'] = OPENFOAM_CMD
task.constants['DOCKER_TAG'] = OPENFOAM_VERSION
task.constants["SETUP_CLUSTER_NB_SLOTS"] = SETUP_CLUSTER_NB_SLOTS
task.hardware_constraints = [qarnot.hardware_constraint.SpecificHardware(instance_type)]

# Scheduling type
task.scheduling_type=OnDemandScheduling()
# task.scheduling_type=FlexScheduling()
# task.scheduling_type=ReservedScheduling()               # If your company has reserved nodes
# task.targeted_reserved_machine_key = instance_type      # Uncomment if your company has reserved nodes



# =============================== Optional Configuration =============================== #

task.snapshot(1800)                                     # Define interval time in seconds when /job will be saved to your bucket.
task.snapshots_whitelist  = SNAPSHOT_FILTER
task.results_whitelist  = RESULTS_FILTER

task.constants['POST_PROCESSING_CMD'] = POST_PROCESSING_CMD
task.constants['USE_SIMULATION_MAXIMUM_EXECUTION_TIME'] = USE_MAX_EXEC_TIME
task.constants['SIMULATION_MAXIMUM_EXECUTION_TIME'] = MAX_EXEC_TIME

# Settings to copy from simulation directory (/share) to bucket linked directory (/job).
##  /job  is the dir where buckets are downloaded at start and uploaded to your bucket by the snapshots.
## /share is the dir where the simulation is executing. Fastest disk and shared directories between nodes.

task.constants['LOCAL_FILES_COPY_FEATURE'] = "true"       # Set to true to upload periodically from the /share folder
task.constants['LOCAL_FILES_COPY_INTERVAL_SEC'] = "1800"  # Set the upload interval in seconds
task.constants['LOCAL_FILES_COPY_REGEX'] = ""             # Filters the files to upload, leave empty to upload everything


# =============================== LAUNCH YOUR TASK ! =============================== #

print('Submitting task on Qarnot')
task.submit()

# The following will download result to the OUTPUT_DIR 
# It will also print the state of the task to your console
LAST_STATE = ''
TASK_ENDED = False
while not TASK_ENDED:
    if task.state != LAST_STATE:
        LAST_STATE = task.state
        print(f"** {LAST_STATE}")

    # Wait for the task to be FullyExecuting
    if task.state == 'Success':
        print(f"** {LAST_STATE}")
        task.download_results(OUTPUT_BUCKET_NAME, True)
        TASK_ENDED = True

    # Display errors on failure
    if task.state == 'Failure':
        print(f"** Errors: {task.errors[0]}")
        TASK_ENDED = True

# =============================== DOWNLOAD RESULTS =============================== #

# Download results when "Success" state is reached
SUCCESS = False
while not SUCCESS:
    # Wait for the task to be FullyExecuting
    if task.state == 'Success':
        task.download_results(OUTPUT_BUCKET_NAME, True)
        SUCCESS = True








