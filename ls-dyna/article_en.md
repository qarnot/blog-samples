Ansys LS-DYNA is a general-purpose finite element program capable of simulating complex real-world problems. It is highly optimized for outstanding performance on CPUs and is widely used across various industries, including automotive, aerospace, defense, and manufacturing, to analyze high-speed, short-duration events such as crash tests, drop tests, impacts, and explosions.

Engineers and researchers rely on LS-DYNA to virtually prototype and validate systems, reducing the need for costly physical trials. The software supports advanced material models and is renowned for its stability in handling highly non-linear deformations and fluid-structure interactions.

## Licensing

To run an LS-DYNA simulation on Qarnot, you must grant Qarnot access to your license. For more details, please contact our team at <a href="mailto:support-compute@qarnot-computing.com" target="_blank">support-compute@qarnot-computing.com</a>.

From this point forward, we will assume that your license configuration with us is already complete.

## Versions

The versions of Ansys LS-DYNA available on Qarnot are listed in our <a href="https://qarnot.com/en/software/ansys-ls-dyna-qarnot" target="_blank">catalogue</a>.

If you are interested in another version, please send us an email at <a href="mailto:support-compute@qarnot-computing.com" target="_blank">support-compute@qarnot-computing.com</a>.

## Launching a task on Qarnot

There are two ways to launch a task on Qarnot:
- Via our web interface <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a>
- Using a script with an SDK

The rest of this blog post focuses on launching using Python scripts for increased automation and speed.

## Prerequisites

Before launching a calculation with the Python SDK, a few steps are required:
- <a href="https://app.qarnot.com/register" target="_blank">Create an account</a>
- Retrieve your <a href="https://app.qarnot.com/settings/access-token" target="_blank">API authentication token</a>
- <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/installation.html" target="_blank">Install the Qarnot Python SDK</a>
- Know your Qarnot profile, for example `ls-dyna-qarnot-vnc-wan`

> **Note**: In addition to the Python SDK, Qarnot also provides SDKs for <a href="https://doc.tasq.qarnot.com/documentation/sdk-csharp/" target="_blank">C#</a> and <a href="https://doc.tasq.qarnot.com/documentation/sdk-nodejs/" target="_blank">Node.js</a>, as well as a Command Line Interface (<a href="https://doc.tasq.qarnot.com/documentation/cli/man/ManIndex.html" target="_blank">CLI</a>).

## Test case

Here is an example of how to run an LS-DYNA use case on the platform. This assumes that:

- You have access to an LS-DYNA license.
- Your use case includes a mesh/input file (for example, `EXP_SC_DROP.key`) in a folder within your working directory.

In this tutorial, we will use a folder named `dyna_drop_test/`. Place your `.key` simulation files into this folder.

Once done, your file structure should look like this:

<pre>
.
├── dyna_drop_test/
│   └── EXP_SC_DROP.key
└── run-lsdyna-test.py
</pre>

## Running a standalone test case

Once everything is configured, you can run the `run-lsdyna-test.py` script below. In this script, you can:
- Replace `MY_SECRET_TOKEN` with your actual authentication token.
- Select the directory you want to synchronize with your bucket.
- Modify the command execution parameters (`LSDYNA_CMD`). For instance:
  - SMP mode: `lsdyna_sp.e i=input.k ncpu=1 memory=1200M`
  - MPP mode: `mpiexec -np 1 lsdyna_sp_mpp.e i=input.k memory=1200M`

Once everything is set up, use the script below to launch the calculation on Qarnot.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/ls-dyna/run-lsdyna-test.py"
     data-filename="run-lsdyna-test.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

To run this script, simply execute `python3 run-lsdyna-test.py` in your terminal.

> **Good to know:** This script also features VNC connectivity. If VNC is enabled, it waits for the task to start execution and displays a direct browser connection link to access the interactive web desktop.

## Results

You should now have a `dyna_drop_test_out` folder in your local working directory and the same output folder on the <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC app</a> containing all output files.

Your results will be stored in your output bucket and can be retrieved in three ways:
- Via the web platform: download directly from the Bucket section.
- As shown in the Python script: using the <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/api/compute/task.html#qarnot.task.Task.download_results" target="_blank">download_results</a> function.
- Or via one of the <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">open-source S3 bucket management applications</a>.

For a large number of files or more than 5GB of data, we recommend using rclone (Linux) or Cyberduck (Windows). Both are <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">open-source S3 management tools</a>.
