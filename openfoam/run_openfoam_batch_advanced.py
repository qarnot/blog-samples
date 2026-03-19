#!/usr/bin/env python3
"""
Script to launch a detailed OpenFOAM batch task on Qarnot's platform.
"""

import os

import qarnot
from qarnot.scheduling_type import OnDemandScheduling, FlexScheduling, ReservedScheduling

# =============================== SETUP VARIABLES =============================== #
# ================================ CHANGE NEEDED ================================ #

CLIENT_TOKEN = os.getenv("QARNOT_TOKEN")  # If your token is in your env.
CLIENT_TOKEN = "MY_SECRET_TOKEN"          # To comment or change
PROFILE = "openfoam"

# =============================================================================== #
DIR_TO_SYNC = "motorbike"
INPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-in"
OUTPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-advanced-out"
TASK_NAME = f"RUN advanced case - {DIR_TO_SYNC}"

OPENFOAM_VERSION = "v2412"
RUN_SCRIPT = "Allrun"

# =============================== TOPOLOGY OPTIONS =============================== #

# 96c single-node example
NB_INSTANCES = 1
SETUP_CLUSTER_NB_SLOTS = 94
INSTANCE_TYPE = "96c-512g-amd-epyc9654-ssd"

# 2x28c multi-node example
# Uncomment this block instead to use two Intel 28-core machines.
#
# NB_INSTANCES = 2
# SETUP_CLUSTER_NB_SLOTS = 26
# INSTANCE_TYPE = "28c-128g-intel-dual-xeon2680v4-ssd"

# =============================== Optional Variables =============================== #

SNAPSHOT_FILTER = ""        # r"processor\d+" - Optional : Regex filter to select which outputfiles you want to keep. Here, an example with filtering .processor
RESULTS_FILTER = ""         # r"processor\d+" - Optional : Regex filter to select which files are copied during your snapshots

USE_MAX_EXEC_TIME = "false" # Optional : Set to true to activate the configuration of maximum cluster execution time. 
MAX_EXEC_TIME = "1h"        # Optional : Maximum cluster execution time (ex: '8h', 'h' for hours or 'd' for days) if USE_MAX_EXEC_TIME is true" 

POST_PROCESSING_CMD = ""    # Optional : Post processing command, ran after simulation if not empty.

# Settings to copy from simulation directory (/share) to bucket linked directory (/job).
##  /job  is the dir where buckets are downloaded at start and uploaded to your bucket by the snapshots.
## /share is the dir where the simulation is executing. Fastest disk and shared directories between nodes.
LOCAL_FILES_COPY_FEATURE = "true"       # Set to true to upload periodically from the /share folder
LOCAL_FILES_COPY_INTERVAL_SEC = "1800"  # Set the upload interval in seconds
LOCAL_FILES_COPY_REGEX = ""             # Filters the files to upload, leave empty to upload everything

# Define interval time in seconds when /job will be saved to your bucket.
SNAPSHOT_INTERVAL = 1800

# =============================== TASK CONFIGURATION =============================== #

conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

task = conn.create_task(TASK_NAME, PROFILE, NB_INSTANCES)

input_bucket = conn.create_bucket(INPUT_BUCKET_NAME)
input_bucket.sync_directory(DIR_TO_SYNC)
task.resources.append(input_bucket)

output_bucket = conn.create_bucket(OUTPUT_BUCKET_NAME)
task.results = output_bucket

task.constants["RUN_SCRIPT"] = RUN_SCRIPT
task.constants["DOCKER_TAG"] = OPENFOAM_VERSION
task.constants["SETUP_CLUSTER_NB_SLOTS"] = SETUP_CLUSTER_NB_SLOTS
task.hardware_constraints = [qarnot.hardware_constraint.SpecificHardware(INSTANCE_TYPE)]

task.scheduling_type = OnDemandScheduling()
# task.scheduling_type = FlexScheduling()
# task.scheduling_type = ReservedScheduling()           # If your company has reserved nodes
# task.targeted_reserved_machine_key = INSTANCE_TYPE    # Uncomment if your company has reserved nodes

# =============================== Optional Configuration =============================== #

task.snapshot_whitelist = SNAPSHOT_FILTER
task.results_whitelist = RESULTS_FILTER

task.constants["POST_PROCESSING_CMD"] = POST_PROCESSING_CMD
task.constants["USE_SIMULATION_MAXIMUM_EXECUTION_TIME"] = USE_MAX_EXEC_TIME
task.constants["SIMULATION_MAXIMUM_EXECUTION_TIME"] = MAX_EXEC_TIME

task.snapshot(SNAPSHOT_INTERVAL)

task.constants["LOCAL_FILES_COPY_FEATURE"] = LOCAL_FILES_COPY_FEATURE
task.constants["LOCAL_FILES_COPY_INTERVAL_SEC"] = LOCAL_FILES_COPY_INTERVAL_SEC
task.constants["LOCAL_FILES_COPY_REGEX"] = LOCAL_FILES_COPY_REGEX

# =============================== LAUNCH YOUR TASK! =============================== #

task.submit()
print("Task submitted on Qarnot")

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
