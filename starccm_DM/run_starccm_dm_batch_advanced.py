"""
Script to launch a detailed STAR-CCM+ Design Manager study in batch mode on Qarnot.
"""

import os

import qarnot
from qarnot.scheduling_type import OnDemandScheduling

# =============================== SETUP VARIABLES =============================== #
# ================================ CHANGE NEEDED ================================ #

CLIENT_TOKEN = os.getenv("QARNOT_TOKEN") # If your token is in your env.
CLIENT_TOKEN = "MY_SECRET_TOKEN"         # To comment or change
PROFILE = "YOUR_PROFILE"                 # Example: "starccm-qarnot"

# =============================================================================== #

DIR_TO_SYNC = "exhaust_opti"
INPUT_BUCKET_NAME = "industrial-exhaust-opti-in"
OUTPUT_BUCKET_NAME = "industrial-exhaust-opti-advanced-out"
TASK_NAME = "RUN STAR-CCM+ Design Manager batch advanced - industrial exhaust"

STARCCM_VERSION = "20.04.008"
STARCCM_PRECISION = "double"

# =============================== TOPOLOGY OPTIONS =============================== #

# 96c single-node example
# Use one AMD 96-core machine and keep 2 cores free for the OS, MPI exchanges,
# and background processes that help keep the solver responsive.

NB_INSTANCES = 1
SETUP_CLUSTER_NB_SLOTS = 94   # Number of processes per node in the mpihost file.
INSTANCE_TYPE = "96c-512g-amd-epyc9654-ssd" 
QARNOT_TOTAL_CLUSTER_CORES = 94 

# Single-node run on one Xeon. The multi-node-only -machinefile and -mpiflags
# options are intentionally omitted here.
STARCCM_CMD = (
    f"starlaunch jobmanager --command starccm+ -batch industrialExhaust_optimization.dmprj "
    "-preallocpower -passtodesign -power -licpath $CDLMD_LICENSE_FILE "
    "-mpi openmpi"
    f"-np {QARNOT_TOTAL_CLUSTER_CORES} --slots 0 --resourcefile /job/mpihosts"
)

# =============================== TASK CONFIGURATION =============================== #

conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

avail_profile = [profile for profile in conn.profiles_names() if "starccm" in profile]
print(f"Available profiles for your account: {avail_profile}")

task = conn.create_task(TASK_NAME, PROFILE, NB_INSTANCES)

input_bucket = conn.create_bucket(INPUT_BUCKET_NAME)
input_bucket.sync_directory(DIR_TO_SYNC)
task.resources.append(input_bucket)

output_bucket = conn.create_bucket(OUTPUT_BUCKET_NAME)
task.results = output_bucket

task.constants["STARCCM_CMD"] = STARCCM_CMD
task.constants["DOCKER_TAG"] = STARCCM_VERSION
task.constants["STARCCM_PRECISION"] = STARCCM_PRECISION
task.constants["SETUP_CLUSTER_NB_SLOTS"] = SETUP_CLUSTER_NB_SLOTS
task.hardware_constraints = [qarnot.hardware_constraint.SpecificHardware(INSTANCE_TYPE)]

# Scheduling type
task.scheduling_type=OnDemandScheduling()
# task.scheduling_type=FlexScheduling()
# task.scheduling_type=ReservedScheduling()               # If your company has reserved nodes
# task.targeted_reserved_machine_key = instance_type      # Uncomment if your company has reserved nodesù$=kèi

# =============================== Optional Configuration =============================== #

task.snapshot(1800)                                       # Define interval time in seconds when /job will be saved to your bucket.

# =============================== LAUNCH YOUR TASK =============================== #

print("Submitting task on Qarnot")
print(f"STARCCM_CMD: {STARCCM_CMD}")
task.submit()

# =============================== MONITORING AND RESULTS =============================== #

last_state = ""
task_ended = False

while not task_ended:
    current_state = task.state
    if current_state != last_state:
        last_state = current_state
        print(f"** {last_state}")

    if current_state == "Success":
        task.download_results(OUTPUT_BUCKET_NAME, True)
        task_ended = True
    elif current_state == "Failure":
        print(f"** Errors: {task.errors[0]}")
        task_ended = True
