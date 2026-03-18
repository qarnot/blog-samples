#!/usr/bin/env python3
"""
Script to launch a STAR-CCM+ batch task on Qarnot's platform.
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
DIR_TO_SYNC = "cylindre"
INPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-in"
OUTPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-out"
TASK_NAME = f"RUN case - {DIR_TO_SYNC}"

STARCCM_VERSION = "20.04.008"
STARCCM_PRECISION = "double"
NB_INSTANCES = 1
INSTANCE_TYPE = "28c-128g-intel-dual-xeon2680v4-ssd"

STARCCM_CMD = (
    "starccm+ -power -batch run "
    "cylindre_complet_extrusion_both_demi_DP_reconstruit_init.sim"
)

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
task.hardware_constraints = [qarnot.hardware_constraint.SpecificHardware(INSTANCE_TYPE)]

# Scheduling type
task.scheduling_type = OnDemandScheduling()

# Snapshots
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
