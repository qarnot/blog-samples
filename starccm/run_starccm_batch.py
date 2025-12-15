"""
Script to launch a detailed StarCCM task, in Batch mode, on Qarnot's platform
"""

import qarnot
from qarnot.scheduling_type import OnDemandScheduling, FlexScheduling, ReservedScheduling
import os

from dotenv import load_dotenv
load_dotenv()

# =============================== SETUP VARIABLES =================================== #

# =============================== Mandatory Variables =============================== #

CLIENT_TOKEN=os.getenv("QARNOT_TOKEN")         # If your token is in a .env. You can also execute, in your terminal, 'export QARNOT_TOKEN='your_token''.
PROFILE="starccm-qarnot"                         # Example : 'starccm-qarnot'

STARCCM_VERSION="19.04.009"                    # StarCCM version 19.04.009
STARCCM_PRECISION="mixed"                      # Precision supported by the version you are using

DIR_TO_SYNC = 'starccm_cylindre_test'          # Name for your model's directory with your .sim model
INPUT_BUCKET_NAME =  f"{DIR_TO_SYNC}-in"    
OUTPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-out"
TASK_NAME = f"RUN test StarCCM_MAR - {DIR_TO_SYNC}" 

INSTANCE_TYPE = 'xeon'                         # xeon is the default choice. Otherwise, put 'epyc'.
if INSTANCE_TYPE == 'xeon':
    SETUP_CLUSTER_NB_SLOTS = 26                # Number of processes per node in the mpihost file. "24" is optimal for xeon.
    instance_type="28c-128g-intel-dual-xeon2680v4-ssd" 
elif INSTANCE_TYPE == 'epyc':
    SETUP_CLUSTER_NB_SLOTS = 94                # Number of processes per node in the mpihost file. A maximum of "94" is suggested for epyc.       
    instance_type = "96c-512g-amd-epyc9654-ssd"

NB_INSTANCES = 4                               # Number of instances and STARCCM_CMD according to single node or multi-node simulation
TOTAL_PROCESSES = SETUP_CLUSTER_NB_SLOTS * NB_INSTANCES

if NB_INSTANCES == 1: 
   STARCCM_CMD=f"starccm+ -power -batch -np {TOTAL_PROCESSES} run cylindre_complet_extrusion_both_demi_DP_reconstruit_init_c4056f43d7.sim"
elif NB_INSTANCES >= 2:
     STARCCM_CMD=f"starccm+ -power -batch -mpi openmpi -mpiflags \"--mca btl ^openib,tcp --mca pml ucx --mca osc ucx --map-by l3cache --bind-to core\" -machinefile /job/mpihosts -np {TOTAL_PROCESSES} run cylindre_complet_extrusion_both_demi_DP_reconstruit_init_c4056f43d7.sim"


# =============================== Optional Variables =============================== #

#OUTPUT_FILTER = r"^.*\.sim$"                  # Optional : Regex filter to select which outputfiles you want to keep. Here, an example with .sim
#SNAPSHOT_FILTER = r"^.*\.sim$"                # Optional : Regex filter to select which files are copied during your snapshots

USE_MAX_EXEC_TIME = "false"                    # Optional : Set to true to activate the configuration of maximum cluster execution time. 
MAX_EXEC_TIME = "8h"                           # Optional : Maximum cluster execution time (ex: '8h', 'h' for hours or 'd' for days) if USE_MAX_EXEC_TIME is true" 

POST_PROCESSING_CMD = ""                       # Optional : Post processing command, ran after simulation if not empty.

# =============================== TASK CONFIGURATION ==================================== #

# =============================== Mandatory Configuration =============================== #

# Create a connection, from which all other objects will be derived
conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

# Print available profiles with you account
avail_profile = [profile for profile in conn.profiles_names() if 'starccm' in profile]
print(f'Available profiles for your account : {avail_profile}')

# Create task
task = conn.create_task(TASK_NAME, PROFILE, NB_INSTANCES)

# Create the input bucket and synchronize with a local folder
# If needed, you can put the absolute path to your model`s directory instead of DIR_TO_SYNC
input_bucket = conn.create_bucket(INPUT_BUCKET_NAME)
input_bucket.sync_directory(DIR_TO_SYNC)
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
output_bucket = conn.create_bucket(OUTPUT_BUCKET_NAME)
task.results = output_bucket

# Specify StarCCM version, SSH, number of cores per node, etc. 
task.constants['DOCKER_TAG'] = STARCCM_VERSION 
task.constants['STARCCM_PRECICION'] = STARCCM_PRECISION
task.constants['STARCCM_CMD'] = STARCCM_CMD
task.constants["SETUP_CLUSTER_NB_SLOTS"] = SETUP_CLUSTER_NB_SLOTS
task.hardware_constraints = [qarnot.hardware_constraint.SpecificHardware(instance_type)]

# Scheduling type
task.scheduling_type=OnDemandScheduling()
# task.scheduling_type=FlexScheduling()
# task.scheduling_type=ReservedScheduling()               # If your company has reserved nodes
# task.targeted_reserved_machine_key = instance_type      # Uncomment if your company has reserved nodes


# =============================== Optional Configuration =============================== #

#task.snapshot(900)                                       # Define interval time in seconds when /job will be saved to your bucket.
#task.snapshots_whitelist  = SNAPSHOT_FILTER
#task.results_whitelist  = OUTPUT_FILTER

#task.constants['POST_PROCESSING_CMD'] = POST_PROCESSING_CMD
#task.constants['USE_SIMULATION_MAXIMUM_EXECUTION_TIME'] = USE_MAX_EXEC_TIME
#task.constants['SIMULATION_MAXIMUM_EXECUTION_TIME'] = MAX_EXEC_TIME

# =============================== LAUNCH YOUR TASK ! =================================== #

print('Submitting task on Qarnot')
task.submit()

# =============================== MONITORING AND RESULTS =============================== #

# The following will download results to the OUTPUT_BUCKET_NAME directory
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

