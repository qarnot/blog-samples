#!/usr/bin/env python3
"""
Advanced example to run a customer image based on roce.base.
"""

import os

import qarnot
from qarnot.scheduling_type import OnDemandScheduling, FlexScheduling, ReservedScheduling

# =============================== SETUP VARIABLES =============================== #
# ================================ CHANGE NEEDED ================================ #

CLIENT_TOKEN = os.getenv("QARNOT_TOKEN") or "MY_SECRET_TOKEN"  # Replace the fallback if QARNOT_TOKEN is not exported.
PROFILE = "docker-cluster-roce"  # RoCE profile, use 'docker-cluster-roce-ssh' or 'docker-cluster-roce-vnc' to use ssh or vnc advanced workflows

# =============================================================================== #
NB_INSTANCES = 2  # 2-node cluster used by this MPI connectivity demo.
TASK_NAME = "RUN advanced RoCE base MPI demo"

DOCKER_SRV = "https://containers.qarnot.com"   # Qarnot Container Registry endpoint.
DOCKER_REPO = "<registry_id>/roce-base-demo"   # Repository containing your custom roce.base child image.
DOCKER_TAG = "<customer-image-tag>"            # Tag pushed to your private Qarnot registry.
DOCKER_REGISTRY_LOGIN = "<your_qarnot_email>"  # Login used to pull the private registry image.
DOCKER_REGISTRY_SECRET = (
    os.getenv("QARNOT_CONTAINER_REGISTRY_KEY") or "<your_container_registry_key>"
)

DIR_TO_SYNC = "mpi_test"  # Local input directory synchronized to the task input bucket.
INPUT_BUCKET_NAME = "roce-base-demo-in"
OUTPUT_BUCKET_NAME = "roce-base-demo-out"

DOCKER_CMD_MASTER = "/bin/bash -lc '/qarnot/utils/roce_wrapper | tee master.logs'"  # The master only starts roce_wrapper.
DOCKER_CMD_WORKER = "/bin/bash -lc '/qarnot/utils/roce_wrapper'"  # Workers only start roce_wrapper too.

# ============================== INSTANCE OPTIONS =============================== #
INSTANCE_TYPE = '96c'            # 28c is the default choice. Otherwise, select '96c'.
if INSTANCE_TYPE == '28c':
    SETUP_CLUSTER_NB_SLOTS = 26   # Number of processes per node in the mpihost file. "26" is optimal for xeon.
    instance_type="28c-128g-intel-dual-xeon2680v4-ssd" 
elif INSTANCE_TYPE == '96c':
    SETUP_CLUSTER_NB_SLOTS = 94   # Number of processes per node in the mpihost file. "94" is optimal for epyc.       
    instance_type = "96c-512g-amd-epyc9654-ssd"

# =============================== DEBUG OPTIONS ================================ #

USE_QARNOT_DEBUG = "false"  # Optional: set to true to echo the shell commands executed by roce_wrapper.
# SSH
DOCKER_SSH = ""  # Optional: paste your public SSH key here.
# VNC
USE_VNC = "false"  # Optional: enable VNC when using a profile that exposes it.
VNC_PASSWORD = ""  # Password for the VNC server. Must be less than 8 chars (additional ones will be ignored). If none, a random one will be assigned and log in task's stdout.
# Keep the cluster alive
USE_KEEP_RUNNING_AFTER_SIMULATION = "false"  # Optional: keep the cluster alive after the COMMANDS for debugging.

# ================================ MPI OPTIONS ================================= #
QARNOT_MPI_ARGS = "--bind-to core --map-by l3cache" # MPI flags

# =============================== WRAPPER COMMANDS =============================== #

PRE_SIMULATION_COMMAND = "test -x /share/run_mpi_demo.sh"  # Quick check that the staged script is executable from /share.
SIMULATION_COMMAND = (
    "/bin/bash -lc 'set -o pipefail && "
    "/bin/bash /share/run_mpi_demo.sh 2>&1 | tee /share/mpi-demo.stdout.log'"  # Main command with stdout capture.
)
POST_SIMULATION_COMMAND = (
    "echo 'Advanced MPI demo finished successfully' | tee /share/post_simulation.log"  # Simple post-step recorded in /share.
)

# ============================== FAILURE MANAGEMENT ============================== #

USE_SIMULATION_MAXIMUM_EXECUTION_TIME = "true"  # Optional: set to true to cap the full wrapper execution time.
SIMULATION_MAXIMUM_EXECUTION_TIME = "1h"  # Optional: use 'h' for hours or 'd' for days.
QARNOT_KILLALL_TIMEOUT_SEC = "120"  # Optional: grace period before a hard kill after timeout.
SOFT_ERROR_LOGS_STR = "ERROR|Fatal|Segmentation fault|MPI demo failed"  # Optional: patterns forcing failure even if the solver returns 0.

# ============================== FILES SYNCHRONIZED ============================== #

# Settings to copy from simulation directory (/share) to bucket linked directory (/job).
##  /job  is the dir where buckets are downloaded at start and uploaded to your bucket by the snapshots.
## /share is the dir where the simulation is executing. Fastest disk and shared directories between nodes.
USE_QARNOT_CLUSTER_DIRECTORY = "true"
LOCAL_FILES_COPY_FEATURE = "true"  # Set to true to upload periodically from the /share folder.
LOCAL_FILES_COPY_INTERVAL_SEC = "300"  # Set the upload interval in seconds.
LOCAL_FILES_COPY_REGEX = ""  # Files to upload whitelist, leave empty to upload everything.

SNAPSHOT_INTERVAL_SEC = 300  # Define interval time in seconds when /job will be saved to your bucket.
# =============================== TASK CONFIGURATION =============================== #


conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)
task = conn.create_task(TASK_NAME, PROFILE, NB_INSTANCES)

input_bucket = conn.create_bucket(INPUT_BUCKET_NAME)
input_bucket.sync_directory(DIR_TO_SYNC)
task.resources.append(input_bucket)

output_bucket = conn.create_bucket(OUTPUT_BUCKET_NAME)
task.results = output_bucket

task.constants["DOCKER_SRV"] = DOCKER_SRV
task.constants["DOCKER_REPO"] = DOCKER_REPO
task.constants["DOCKER_TAG"] = DOCKER_TAG
task.constants["DOCKER_REGISTRY_LOGIN"] = DOCKER_REGISTRY_LOGIN
task.constants["DOCKER_REGISTRY_PASSWORD"] = "${QARNOT_SECRET__DOCKER_REGISTRY_PASSWORD}"
task.constants["QARNOT_SECRET__DOCKER_REGISTRY_PASSWORD"] = DOCKER_REGISTRY_SECRET

task.constants["DOCKER_CMD_MASTER"] = DOCKER_CMD_MASTER
task.constants["DOCKER_CMD_WORKER"] = DOCKER_CMD_WORKER

task.constants["USE_QARNOT_DEBUG"] = USE_QARNOT_DEBUG
task.constants["USE_VNC"] = USE_VNC
task.constants["VNC_PASSWORD"] = VNC_PASSWORD
task.constants["USE_KEEP_RUNNING_AFTER_SIMULATION"] = USE_KEEP_RUNNING_AFTER_SIMULATION
if DOCKER_SSH:
    task.constants["DOCKER_SSH"] = DOCKER_SSH

task.constants["QARNOT_MPI_ARGS"] = QARNOT_MPI_ARGS

task.constants["SETUP_CLUSTER_NB_SLOTS"] = SETUP_CLUSTER_NB_SLOTS
task.hardware_constraints = [qarnot.hardware_constraint.SpecificHardware(instance_type)]

task.constants["PRE_SIMULATION_COMMAND"] = PRE_SIMULATION_COMMAND
task.constants["SIMULATION_COMMAND"] = SIMULATION_COMMAND
task.constants["POST_SIMULATION_COMMAND"] = POST_SIMULATION_COMMAND

task.constants["USE_SIMULATION_MAXIMUM_EXECUTION_TIME"] = (
    USE_SIMULATION_MAXIMUM_EXECUTION_TIME
)
task.constants["SIMULATION_MAXIMUM_EXECUTION_TIME"] = (
    SIMULATION_MAXIMUM_EXECUTION_TIME
)
task.constants["QARNOT_KILLALL_TIMEOUT_SEC"] = QARNOT_KILLALL_TIMEOUT_SEC
task.constants["SOFT_ERROR_LOGS_STR"] = SOFT_ERROR_LOGS_STR

task.constants["USE_QARNOT_CLUSTER_DIRECTORY"] = USE_QARNOT_CLUSTER_DIRECTORY
task.constants["LOCAL_FILES_COPY_FEATURE"] = LOCAL_FILES_COPY_FEATURE
task.constants["LOCAL_FILES_COPY_INTERVAL_SEC"] = LOCAL_FILES_COPY_INTERVAL_SEC
task.constants["LOCAL_FILES_COPY_REGEX"] = LOCAL_FILES_COPY_REGEX
task.snapshot(SNAPSHOT_INTERVAL_SEC)

task.scheduling_type = OnDemandScheduling()
# task.scheduling_type = FlexScheduling()
# task.scheduling_type = ReservedScheduling()
# task.targeted_reserved_machine_key = instance_type      # Uncomment if your company has reserved nodes

# =============================== LAUNCH YOUR TASK! =============================== #

task.submit()
print("Task submitted on Qarnot")

# =============================== MONITORING AND RESULTS =============================== #

# LAST_STATE = ""
# TASK_ENDED = False

# while not TASK_ENDED:
#     if task.state != LAST_STATE:
#         LAST_STATE = task.state
#         print(f"** {LAST_STATE}")

#     if task.state == "Success":
#         print(f"** {LAST_STATE}")
#         # Optional: download the output bucket locally when you need a local copy.
#         task.download_results(OUTPUT_BUCKET_NAME, True)
#         TASK_ENDED = True

#     if task.state == "Failure":
#         print(f"** Errors: {task.errors[0]}")
#         TASK_ENDED = True
