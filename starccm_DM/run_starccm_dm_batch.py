#!/usr/bin/env python3
"""
Script to launch a simple STAR-CCM+ Design Manager batch task on Qarnot's platform.
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
OUTPUT_BUCKET_NAME = "industrial-exhaust-opti-out"
TASK_NAME = "RUN industrial exhaust Design Manager"

STARCCM_VERSION = "20.04.008"
STARCCM_PRECISION = "double"
NB_INSTANCES = 1
INSTANCE_TYPE = "28c-128g-intel-dual-xeon2680v4-ssd"

# Single-node run on one Xeon. The multi-node-only -machinefile and -mpiflags
# options are intentionally omitted here.
STARCCM_CMD = (
    'starlaunch jobmanager --command '
    '"starccm+ -batch industrialExhaust_optimization.dmprj '
    '-preallocpower -passtodesign -power '
    '-licpath $CDLMD_LICENSE_FILE '
    '-mpi openmpi -np 26" '
    '--slots 0 --resourcefile /job/mpihosts'
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
task.scheduling_type = OnDemandScheduling()

# =============================== LAUNCH YOUR TASK =============================== #

task.submit()
print("Task submitted on Qarnot")
