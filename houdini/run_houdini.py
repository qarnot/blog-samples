#!/usr/bin/env python3

# Import the Qarnot SDK
import qarnot

# Connect to the Qarnot platform
conn = qarnot.connection.Connection(client_token="MY_SECRET_TOKEN")

# Create a task
task = conn.create_task('Houdini', 'houdini', 1)

# Create a resource bucket and add input files
bucket = conn.retrieve_or_create_bucket("input_houdini")
bucket.sync_directory('input')

# Attach the bucket to the task
task.resources.append(bucket)

# Create a result bucket and attach it to the task
task.results = conn.create_bucket("output_houdini")

# Task constants are the main way of controlling a task's behaviour
task.constants['RENDER_TYPE'] = 'USD' #Accepted values are [HIP,USD,IFD] depending on your input file
task.constants['INPUT_FILE'] = 'cornell_box.usd'
task.constants['RESOLUTION'] = '1920x1080'
task.constants['OUTPUT_FILE'] = 'output/cornell.%04d.png'
task.constants['FRAME_RANGE'] = '1,9'
task.constants['VERBOSE_LEVEL']='4'

# License server informations
task.constants['LICENSE_SERVER_IP']='MY LICENSE SERVER IP'
task.constants['LICENSE_SERVER_HOSTNAME']='MY LICENSE SERVER HOSTNAME'
task.constants['LICENSE_SERVER_PORT']='MY LICENSE SERVER PORT'

# Submit the task to the Api, that will launch it on the cluster
task.submit()