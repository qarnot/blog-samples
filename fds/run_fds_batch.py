#!/usr/bin/env python3
"""
Script to launch an FDS batch task on Qarnot's platform.
"""

import os

import qarnot
from qarnot.scheduling_type import OnDemandScheduling

# =============================== SETUP VARIABLES =============================== #
# ================================ CHANGE NEEDED ================================ #

CLIENT_TOKEN = os.getenv("QARNOT_TOKEN")  # If your token is in your env.
# CLIENT_TOKEN = "MY_SECRET_TOKEN"          # To comment or change

# =============================================================================== #
DIR_TO_SYNC = "temple"
INPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-in"
OUTPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-out"
TASK_NAME = f"RUN case - {DIR_TO_SYNC}"

PROFILE = "fds"
FDS_VERSION = "6.10.1"
INSTANCE_TYPE = "28c-128g-intel-dual-xeon2680v4-ssd" 

FDS_CMD = "export OMP_NUM_THREADS=2 && mpiexec -np 16 fds temple_16_MPI_PROC.fds"

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
