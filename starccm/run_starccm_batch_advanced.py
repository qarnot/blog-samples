#!/usr/bin/env python3
"""
Script to launch a detailed STAR-CCM+ batch task on Qarnot's platform.
"""

import os

import qarnot
from qarnot.scheduling_type import OnDemandScheduling, FlexScheduling, ReservedScheduling

# =============================== SETUP VARIABLES =============================== #
# ================================ CHANGE NEEDED ================================ #

CLIENT_TOKEN = os.getenv("QARNOT_TOKEN") # If your token is in your env.
CLIENT_TOKEN = "MY_SECRET_TOKEN"         # To comment or change
PROFILE = "YOUR_PROFILE"                 # Example: "starccm-qarnot"

# =============================================================================== #
DIR_TO_SYNC = "cylindre"
INPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-in"
OUTPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-advanced-out"
TASK_NAME = f"RUN advanced case - {DIR_TO_SYNC}"

STARCCM_VERSION = "20.04.008"
STARCCM_PRECISION = "double"
SIMULATION_FILE = "cylindre_complet_extrusion_both_demi_DP_reconstruit_init.sim"

# =============================== TOPOLOGY OPTIONS =============================== #

# 96c single-node example
NB_INSTANCES = 1
SETUP_CLUSTER_NB_SLOTS = 94
INSTANCE_TYPE = "96c-512g-amd-epyc9654-ssd"
QARNOT_TOTAL_CLUSTER_CORES = 94
STARCCM_CMD = (
    "starccm+ -power -batch -mpi openmpi "
    f"-np {QARNOT_TOTAL_CLUSTER_CORES} run {SIMULATION_FILE}"
)

# 2x28c multi-node example
# Uncomment this block instead to use two Intel 28-core machines.
#
# NB_INSTANCES = 2
# SETUP_CLUSTER_NB_SLOTS = 26
# INSTANCE_TYPE = "28c-128g-intel-dual-xeon2680v4-ssd"
# QARNOT_TOTAL_CLUSTER_CORES = 52
# STARCCM_CMD = (
#     "starccm+ -power -batch -mpi openmpi "
#     f"-np {QARNOT_TOTAL_CLUSTER_CORES} "
#     '-mpiflags "--mca btl ^openib,tcp --mca pml ucx --mca osc ucx" '
#     f"-machinefile /job/mpihosts run {SIMULATION_FILE}"
# )

# =============================== Optional Variables =============================== #

# SNAPSHOT_FILTER = r"^.*\.sim$"              # Optional: keep only .sim files in snapshots.
SNAPSHOT_FILTER = ""
# RESULTS_FILTER = r"^.*\.sim$"               # Optional: keep only .sim files in final results.
RESULTS_FILTER = ""

USE_MAX_EXEC_TIME = "false"                   # Optional: set to true to cap cluster execution time.
MAX_EXEC_TIME = "8h"                          # Optional: use 'h' for hours or 'd' for days.

POST_PROCESSING_CMD = ""                      # Optional: post-processing command run after the solver.

# =============================== TASK CONFIGURATION =============================== #

conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

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
task.scheduling_type = OnDemandScheduling()
# task.scheduling_type = FlexScheduling()
# task.scheduling_type = ReservedScheduling()           # If your company has reserved nodes
# task.targeted_reserved_machine_key = INSTANCE_TYPE    # Uncomment if your company has reserved nodes

# =============================== Optional Configuration =============================== #

task.snapshot(1800)  # Define interval time in seconds when /job will be saved to your bucket.
task.snapshot_whitelist = SNAPSHOT_FILTER
task.results_whitelist = RESULTS_FILTER

task.constants["POST_PROCESSING_CMD"] = POST_PROCESSING_CMD
task.constants["USE_SIMULATION_MAXIMUM_EXECUTION_TIME"] = USE_MAX_EXEC_TIME
task.constants["SIMULATION_MAXIMUM_EXECUTION_TIME"] = MAX_EXEC_TIME

# =============================== LAUNCH YOUR TASK! =============================== #

task.submit()
print("Task submitted on Qarnot")
print(f"STARCCM_CMD: {STARCCM_CMD}")

# =============================== MONITORING AND RESULTS =============================== #

LAST_STATE = ""
TASK_ENDED = False

while not TASK_ENDED:
    if task.state != LAST_STATE:
        LAST_STATE = task.state
        print(f"** {LAST_STATE}")

    if task.state == "Success":
        print(f"** {LAST_STATE}")
        task.download_results(OUTPUT_BUCKET_NAME, True)
        TASK_ENDED = True

    if task.state == "Failure":
        print(f"** Errors: {task.errors[0]}")
        TASK_ENDED = True
