#!/usr/bin/env python3
"""
Script to launch an OpenFOAM batch task on Qarnot's platform.
"""

import os

import qarnot
from qarnot.scheduling_type import OnDemandScheduling

# =============================== SETUP VARIABLES =============================== #
# ================================ CHANGE NEEDED ================================ #

CLIENT_TOKEN = os.getenv("QARNOT_TOKEN")  # If your token is in your env.
CLIENT_TOKEN = "MY_SECRET_TOKEN"          # To comment or change
PROFILE = "YOUR_PROFILE"                  # Example: "openfoam"

# =============================================================================== #
DIR_TO_SYNC = "motorbike"
INPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-in"
OUTPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-out"
TASK_NAME = f"RUN case - {DIR_TO_SYNC}"

OPENFOAM_VERSION = "v2412"
NB_INSTANCES = 1
SETUP_CLUSTER_NB_SLOTS = 26
INSTANCE_TYPE = "28c-128g-intel-dual-xeon2680v4-ssd"

RUN_SCRIPT = "Allrun"

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

task.snapshot(1800)  # Define interval time in seconds when /job will be saved to your bucket.

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
