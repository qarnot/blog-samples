#!/usr/bin/env python3

# Import Qarnot SDK
import qarnot

# Create a connection, from which all other objects will be derived
# Enter your client token here
conn = qarnot.connection.Connection(client_token="<<<MY_SECRET_TOKEN>>>")

# Create the task
task = conn.create_task("Photogrammetry - Meshroom", "meshroom", 1)


# Create the input bucket and synchronize with a local folder
# Insert a local folder directory
input_bucket = conn.retrieve_or_create_bucket("meshroom-in")
input_bucket.sync_directory("CuteB3")

# Attach the bucket to the task
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
task.results = conn.retrieve_or_create_bucket("meshroom-out")

# Specify the task's parameters
task.constants["INPUT_FOLDER"] = ""
task.constants["OUTPUT_FOLDER"] = "output-folder"
task.constants["LOGS_FOLDER"] = "logs"
# task.constants["DOCKER_TAG"] = "2021.1.0"
# task.constants['MESHROOM_EXTRA_FLAGS'] = ""

# Submit the task
task.run(output_dir="output")
