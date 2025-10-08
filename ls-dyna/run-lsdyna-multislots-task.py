"""Script to run an LS-DYNA task on a pool on Qarnot cloud"""

import qarnot
from qarnot.scheduling_type import OnDemandScheduling, ReservedScheduling
import os, sys

# =============================== Setup Variables =============================== #
# To change
CLIENT_TOKEN="MY_SECRET_TOKEN"                 # To retrieve on tasq.qarnot.com/settings/access-token
CLIENT_TOKEN=os.getenv("QARNOT_TOKEN")         # Using an env variable
POOL_UUID = "POOL_UUID"                        # Pool UUID print by your pool creation script

# Change the following if needed
DIR_TO_SYNC = "dyna_drop_test"                 # This is the local directory that will be uploaded to you input bucket
INPUT_BUCKET_NAME =  f"{DIR_TO_SYNC}-in"
OUTPUT_BUCKET_NAME = f"{DIR_TO_SYNC}-out"
TASK_NAME = f"RUN test on LS-DYNA pool - {DIR_TO_SYNC}" 

DYNA_CMD = "mpiexec -np 1 lsdyna_sp_mpp.e i=EXP_SC_DROP.key memory=1200M" # More info bellow

# Copy these settings from the pool parameters. Do not change otherwise.
NB_INSTANCES = 1
SLOTS = 2  
# =============================================================================== #

# Create a connection, from which all other objects will be derived
conn = qarnot.connection.Connection(client_token=CLIENT_TOKEN)

# Print FullyExecuting pools on your account
print("FullyExecuting pools:\n",[pool.uuid for pool in conn.all_pools() if pool.state == "FullyExecuting"])

# Récupération de la pool
try : 
    pool = conn.retrieve_pool(POOL_UUID)
except :
    print("Pool not found, use a listed pool above or wait for your pool to be FullyExecuting")
    sys.exit(1)

# Create task in the pool
task = conn.create_task(TASK_NAME, pool, NB_INSTANCES)

# Create the input bucket and synchronize with a local folder
input_bucket = conn.create_bucket(INPUT_BUCKET_NAME)
input_bucket.sync_directory(DIR_TO_SYNC)
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
output_bucket = conn.create_bucket(OUTPUT_BUCKET_NAME)
task.results = output_bucket


# CMD - To use with lsdyna_sp or lsdyna_dp
## SMP : lsdyna_sp.e i=input.k ncpu=1 memory=1200M
## MPP : mpiexec -np 1 lsdyna_sp_mpp.e i=input.k memory=1200M
## Leave it empty to launch your simulaiton through lsrun on web desktop 
task.constants["MECHANICAL_CMD"] = DYNA_CMD

# Optional parameters
# Number of cores perslots e.g. "13" out of 28 cores. Default value is NBCORE / SLOTS
# task.constants['CORES_PER_SLOT'] = "13"

# Define interval time in seconds when your simulation will be saved to your bucket.
# task.snapshot(900)

task.submit()


# ---------- Optional ----------
## -- To comment/delete if not usefull
# Hang until success and then download results
OUTPUT_DIR = "dyna_drop_test_out"
SUCCESS = False
while not SUCCESS:
    # Wait for the task to be FullyExecuting
    if task.state == 'Success':
        task.download_results(OUTPUT_DIR, True)
        SUCCESS = True

