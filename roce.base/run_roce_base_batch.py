#!/usr/bin/env python3
"""
Minimal example to run a customer image based on roce.base.
"""

import os

import qarnot
from qarnot.scheduling_type import OnDemandScheduling

# =============================== SETUP VARIABLES =============================== #
# ================================ CHANGE NEEDED ================================ #

CLIENT_TOKEN = os.getenv("QARNOT_TOKEN") or "MY_SECRET_TOKEN"  # Replace the fallback if QARNOT_TOKEN is not exported.
PROFILE = "docker-cluster-roce"  # RoCE profile without VNC or SSH for a minimal batch submission.

# =============================================================================== #
NB_INSTANCES = 2  # 2-node cluster used by this MPI connectivity demo.
TASK_NAME = "RUN RoCE base MPI demo"

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
# Default nodes are 28 cores Intel Xeon, see the advanced script to use 96 cores. 
SETUP_CLUSTER_NB_SLOTS = 26   # Number of processes per node in the mpihost file. "26" is optimal for the default Xeon.
# =============================== WRAPPER COMMANDS =============================== #

PRE_SIMULATION_COMMAND = "test -x /share/run_mpi_demo.sh"  # Quick check that the staged script is executable from /share.
SIMULATION_COMMAND = "/bin/bash /share/run_mpi_demo.sh"  # Main MPI connectivity demo command.
POST_SIMULATION_COMMAND = (
    "echo 'MPI demo finished successfully' | tee /share/post_simulation.log"  # Simple post-step recorded in /share.
)

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

task.constants["SETUP_CLUSTER_NB_SLOTS"] = SETUP_CLUSTER_NB_SLOTS

task.constants["PRE_SIMULATION_COMMAND"] = PRE_SIMULATION_COMMAND
task.constants["SIMULATION_COMMAND"] = SIMULATION_COMMAND
task.constants["POST_SIMULATION_COMMAND"] = POST_SIMULATION_COMMAND

task.constants["USE_QARNOT_CLUSTER_DIRECTORY"] = USE_QARNOT_CLUSTER_DIRECTORY
task.constants["LOCAL_FILES_COPY_FEATURE"] = LOCAL_FILES_COPY_FEATURE
task.constants["LOCAL_FILES_COPY_INTERVAL_SEC"] = LOCAL_FILES_COPY_INTERVAL_SEC
task.constants["LOCAL_FILES_COPY_REGEX"] = LOCAL_FILES_COPY_REGEX
task.snapshot(SNAPSHOT_INTERVAL_SEC)

task.scheduling_type = OnDemandScheduling()

# =============================== LAUNCH YOUR TASK! =============================== #

task.submit()
print("Task submitted on Qarnot")
