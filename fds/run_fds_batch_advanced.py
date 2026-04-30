#!/usr/bin/env python3
"""
Script to launch a detailed FDS batch task on Qarnot's platform.
"""

import os

import qarnot
from qarnot.scheduling_type import OnDemandScheduling, FlexScheduling, ReservedScheduling

# =============================== SETUP VARIABLES =============================== #
# ================================ CHANGE NEEDED ================================ #

CLIENT_TOKEN = os.getenv("QARNOT_TOKEN")  # If your token is in your env.
# CLIENT_TOKEN = "MY_SECRET_TOKEN"          # To comment or change

# =============================================================================== #
DIR_TO_SYNC = "temple"
INPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-in"
OUTPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-advanced-out"
TASK_NAME = f"RUN advanced case - {DIR_TO_SYNC}"

FDS_VERSION = "6.10.1"

# =============================== CPU CHOICE =============================== #
# fds is the default profile
PROFILE = "fds"
# With it, you can use 28 cores or 96 cores CPUs
INSTANCE_TYPE = "28c-128g-intel-dual-xeon2680v4-ssd" # Or 96c-512g-amd-epyc9654-ssd

# This example case is partitioned for 16 MPI processes.
# To use CPUs with 16 cores or less, you need to use our "non-cluster" profiles
PROFILE = "fds-non-cluster"
# 8 ou 16c instance type
INSTANCE_TYPE = "16c-128g-amd-tr2950x-ssd" # Or 8c-32g-amd-rz2700x-ssd

# =============================== CMD SETUP =============================== #
QARNOT_TOTAL_CLUSTER_CORES = 16
FDS_CMD = f"export OMP_NUM_THREADS=2 && mpiexec -np {QARNOT_TOTAL_CLUSTER_CORES} fds temple_16_MPI_PROC.fds"

# =============================== Optional Variables =============================== #

SNAPSHOT_FILTER = ""        # Optional: regex filter to select which snapshot files are kept.
RESULTS_FILTER = ""         # Optional: regex filter to select which final result files are kept.

USE_MAX_EXEC_TIME = "false" # Optional: set to true to cap cluster execution time.
MAX_EXEC_TIME = "8h"        # Optional: use 'h' for hours or 'd' for days.

POST_PROCESSING_CMD = ""    # Optional: post-processing command run after the solver.

# Settings to copy from simulation directory (/share) to bucket linked directory (/job).
LOCAL_FILES_COPY_FEATURE = "true"       # Set to true to upload periodically from the /share folder.
LOCAL_FILES_COPY_INTERVAL_SEC = "1800"  # Set the upload interval in seconds.
LOCAL_FILES_COPY_REGEX = ".*"           # Filters the files to upload, leave empty to upload everything.

# Define interval time in seconds when /job will be saved to your bucket.
SNAPSHOT_INTERVAL = 1800

# =============================== TASK CONFIGURATION =============================== #

conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

task = conn.create_task(TASK_NAME, PROFILE, 1)

input_bucket = conn.create_bucket(INPUT_BUCKET_NAME)
input_bucket.sync_directory(DIR_TO_SYNC)
task.resources.append(input_bucket)

output_bucket = conn.create_bucket(OUTPUT_BUCKET_NAME)
task.results = output_bucket

task.constants["FDS_CMD"] = FDS_CMD
task.constants["DOCKER_TAG"] = FDS_VERSION
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
print(f"FDS_CMD: {FDS_CMD}")

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
