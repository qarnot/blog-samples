Ansys Fluent is a powerful Computational Fluid Dynamics (CFD) software that simulates fluid flow, heat transfer, and other related phenomena. It is widely used across various industries, including aerospace, automotive, energy, and environmental engineering.

Researchers, engineers, and designers rely on Fluent to analyze complex fluid behavior, optimize designs, and improve performance. The software uses numerical methods to solve the partial differential equations that govern fluid flow, providing accurate predictions and analysis for real-world applications.

## Licensing

To run a Fluent simulation on Qarnot, you must grant Qarnot access to your license. For more details, please contact our team at <a href="mailto:support-compute@qarnot-computing.com" target="_blank">support-compute@qarnot-computing.com</a>.

From this point forward, we will assume that your license configuration with us is already complete.

## Versions

The versions of Ansys Fluent available on Qarnot are listed in our <a href="https://qarnot.com/en/software/ansys-fluent-qarnot" target="_blank">catalogue</a>.

If you are interested in another version, please send us an email at <a href="mailto:support-compute@qarnot-computing.com" target="_blank">support-compute@qarnot-computing.com</a>.

## Launching a task on Qarnot

There are two ways to launch a task on Qarnot:
- Via our web interface <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a>
- Using a script with a SDK

To launch a task via the web interface, you can follow this <a href="https://app.supademo.com/demo/cmdpsrrgz2skb9f96zxlzrzdf?utm_source=link" target="_blank">step-by-step tutorial</a>.

<div style="position: relative; box-sizing: content-box; max-height: 80vh; max-height: 80svh; width: 100%; aspect-ratio: 1.81; padding: 40px 0 40px 0;">
  <iframe src="https://app.supademo.com/embed/cmdpsrrgz2skb9f96zxlzrzdf?embed_v=2&utm_source=embed" loading="lazy" title="How to start an Ansys Fluent simulation on Qarnot" allow="clipboard-write" frameborder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>

The rest of this blog post focuses on launching using Python scripts for increased automation and speed.

## Prerequisites

Before launching a calculation with the Python SDK, a few steps are required:
- <a href="https://app.qarnot.com/register" target="_blank">Create an account</a>
- Retrieve your <a href="https://app.qarnot.com/settings/access-token" target="_blank">API authentication token</a>
- <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/installation.html" target="_blank">Install the Qarnot Python SDK</a>
- Know your Qarnot profile, for example `ansys-fluent-e-corp` and `ansys-fluent-e-corp-vnc`

> **Note**: In addition to the Python SDK, Qarnot also provides SDKs for <a href="https://doc.tasq.qarnot.com/documentation/sdk-csharp/" target="_blank">C#</a> and <a href="https://doc.tasq.qarnot.com/documentation/sdk-nodejs/" target="_blank">Node.js</a>, as well as a Command Line Interface (<a href="https://doc.tasq.qarnot.com/documentation/cli/man/ManIndex.html" target="_blank">CLI</a>).

## Launching an MPI test

The Ansys-Fluent MPI test can run without a license. To start an MPI test on Qarnot, copy the following code into a Python script. Make sure to paste your authentication token (retrieve it <a href="http://app.qarnot.com/settings/access-token" target="_blank">here</a>) into the script instead of `MY_SECRET_TOKEN` to launch the task on Qarnot.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/ansys-fluent/run_ansys-fluent_mpi-test.py"
     data-filename="run_ansys-fluent_mpi-test.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

> **Good to know:** When you create a task with `conn.create_task`, you must specify its name, the profile you want to use, and in the case of a cluster, the number of instances you wish to run.

## Test case

Here is an example of how to run an Ansys-Fluent use case on the platform. This assumes that:

- You have access to a license.
- Your use case includes data and a `.jou` file in a folder within your working directory.

If needed, here is the generic use case <a href="https://pages.qarnot.com/hubfs/%5BMARCOM%5D%20Blog%20site%20HPC/aircraft_wing_14m.zip" target="_blank">aircraft_wing_14m</a>. You can download and extract it into an `aircraft/` directory.

Once done, your file structure should look like this:

<pre>
.
├── aircraft/
│   ├── run.jou
│   ├── aircraft_wing_14m.cas
│   └── aircraft_wing_14m.dat
└── run-ansys-fluent.py
</pre>

## Launching the test case

Once everything is configured, it's time to run the `run-ansys-fluent.py` script below. In this script, you can:
- Replace `MY_SECRET_TOKEN` with your actual authentication token.
- Select the directory you want to synchronize with your bucket.
- Modify the `FLUENT_CMD` if necessary.

Once everything is set up, use the script below to launch the calculation on Qarnot.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/ansys-fluent/run_ansys-fluent.py"
     data-filename="run-ansys-fluent.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

You now know how to launch an Ansys-Fluent task on Qarnot!

## Batch launch script

The script below allows you to explore more advanced features of the platform for batch launching.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/ansys-fluent/run_ansys-fluent_batch.py"
     data-filename="run_fluent_batch.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

## Launching a fluent task with SSH connectivity enabled

Here is an example of how to run an Ansys-Fluent use case with SSH enabled on the platform. You will need an SSH public key (you can create one following this <a href="https://qarnot.com/documentation/use-ssh" target="_blank">tutorial</a>).

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/ansys-fluent/run_ansys-fluent_ssh.py"
     data-filename="run_fluent_ssh.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

To launch the calculation on Qarnot, copy the code above into a Python script in your working directory. Ensure you have:

- Copied your authentication token into the script (replacing `MY_SECRET_TOKEN`)
- Copied your SSH key into `DOCKER_SSH`

And now, you can run `python3 run_fluent_ssh.py`.

> **Note:** The profile used has changed to `ansys-fluent-ssh`.

Once connected to the master node, you can launch a simulation on your cluster with this command:

> `fluent 3ddp -g mpi=openmpi -pinfiniband -cnf=/job/mpihosts -i run.jou`

Where `mpi=openmpi -pinfiniband -cnf=/job/mpihosts` are the necessary MPI parameters for a multi-node simulation.

## Results

You should now have an `aircraft-out` folder in your local working directory and the same `aircraft-out` on the <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC app</a> containing all output files.

You can directly view certain images and log files generated by the simulation in your output bucket via the <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC app</a>.

Your results will be stored in the `aircraft-out` bucket and can be retrieved in three ways:
- Via the web platform: download directly from the Bucket section.
- As shown in the Python script: using the <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/api/compute/task.html#qarnot.task.Task.download_results" target="_blank">download_results</a> function.
- Or via one of the <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">open-source S3 bucket management applications</a>.

For a large number of files or more than 5GB of data, we recommend using rclone (Linux) or Cyberduck (Windows). Both are <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">open-source S3 management tools</a>.