STAR-CCM+ is a widely used multiphysics simulation software for Computational Fluid Dynamics, heat transfer, and, more broadly, the analysis of complex engineering systems. It can run robust computations both in batch mode and interactively on high-performance computing resources.

On Qarnot, STAR-CCM+ can be launched via the web interface or with Python scripts based on the SDK. In this article, we will:
- present a simple script for batch launching
- present a more detailed batch script
- and then a script to launch a task with SSH connectivity

## Licensing

To run a STAR-CCM+ simulation on Qarnot, you must grant Qarnot access to your license. For more details, please contact our team at <a href="mailto:support-compute@qarnot-computing.com" target="_blank">support-compute@qarnot-computing.com</a>.

From this point forward, we will assume that your license configuration with us is already complete.

## Versions

The versions of STAR-CCM+ available on Qarnot are listed in our <a href="https://qarnot.com/en/software/starccm-qarnot" target="_blank">catalogue</a>.

If you need another version, please send us an email at <a href="mailto:support-compute@qarnot-computing.com" target="_blank">support-compute@qarnot-computing.com</a>.

## Launching a task on Qarnot

There are two ways to launch a task on Qarnot:
- Via our web interface <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a>
- Using a script with an SDK

To launch a task via the web interface, you can follow this <a href="https://app.supademo.com/demo/cmdfq02do1rg46n9n60b4xcmt?utm_source=link" target="_blank">step-by-step tutorial</a>.

<div style="position: relative; box-sizing: content-box; max-height: 80vh; max-height: 80svh; width: 100%; aspect-ratio: 1.81; padding: 40px 0 40px 0;">
  <iframe src="https://app.supademo.com/embed/cmdfq02do1rg46n9n60b4xcmt?embed_v=2&utm_source=embed" loading="lazy" title="How to start a STAR-CCM+ simulation on Qarnot" allow="clipboard-write" frameborder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>

If you would rather visualize your session using remote desktop, you can also follow this <a href="https://app.supademo.com/demo/cmeu0wtk95zglv9kqbysic0ix?utm_source=link" target="_blank">dedicated tutorial</a>.

<div style="position: relative; box-sizing: content-box; max-height: 80vh; max-height: 80svh; width: 100%; aspect-ratio: 1.81; padding: 40px 0 40px 0;">
  <iframe src="https://app.supademo.com/embed/cmeu0wtk95zglv9kqbysic0ix?embed_v=2&utm_source=embed" loading="lazy" title="How to visualize a STAR-CCM+ simulation with remote desktop on Qarnot" allow="clipboard-write" frameborder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>

The rest of this blog post focuses on launching with Python scripts for increased automation and speed.

## Prerequisites

Before launching a calculation with the Python SDK, a few steps are required:
- <a href="https://app.qarnot.com/register" target="_blank">Create an account</a>
- Retrieve your <a href="https://app.qarnot.com/settings/access-token" target="_blank">API authentication token</a>
- <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/installation.html" target="_blank">Install the Qarnot Python SDK</a>
- Know your Qarnot profile, for example `starccm-qarnot` for batch mode and `starccm-qarnot-ssh` for SSH access

> **Note**: In addition to the Python SDK, Qarnot also provides SDKs for <a href="https://doc.tasq.qarnot.com/documentation/sdk-csharp/" target="_blank">C#</a> and <a href="https://doc.tasq.qarnot.com/documentation/sdk-nodejs/" target="_blank">Node.js</a>, as well as a Command Line Interface (<a href="https://doc.tasq.qarnot.com/documentation/cli/man/ManIndex.html" target="_blank">CLI</a>).

## Test case

Here is an example of how to run a STAR-CCM+ use case on the platform. This assumes that:

- You have access to a license.
- Your use case includes a `.sim` file in a folder within your working directory.

In the examples below, we use the file `cylindre_complet_extrusion_both_demi_DP_reconstruit_init.sim` stored in a `cylindre/` directory.
If needed, you can directly download the example file here: <a href="https://communication.qarnot.com/hubfs/%5BMARCOM%5D%20Blog%20site%20HPC/cylindre_complet_extrusion_both_demi_DP_reconstruit_init_c4056f43d7.sim" target="_blank">cylindre_complet_extrusion_both_demi_DP_reconstruit_init.sim</a>

Once done, your file structure should look like this:

<pre>
.
├── cylindre/
│   └── cylindre_complet_extrusion_both_demi_DP_reconstruit_init.sim
├── run_starccm_batch.py
├── run_starccm_batch_advanced.py
└── run_starccm_ssh.py
</pre>

## Launching the test case

Once everything is configured, it is time to run the `run_starccm_batch.py` script below. In this script, you need to:
- Replace `MY_SECRET_TOKEN` with your actual authentication token
- Select the directory you want to synchronize with your bucket
- Adjust the STAR-CCM+ version if needed

Once everything is ready, use the `run_starccm_batch.py` script below to launch the calculation on Qarnot.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/starccm/run_starccm_batch.py"
     data-filename="run_starccm_batch.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

You now know how to launch a STAR-CCM+ batch task on Qarnot!

## Advanced batch script

The script below allows you to explore more advanced topologies, especially a `96c` AMD node or a `2x28c` multi-node configuration.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/starccm/run_starccm_batch_advanced.py"
     data-filename="run_starccm_batch_advanced.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

## Launching a STAR-CCM+ task with SSH connectivity enabled

Here is an example of how to run a STAR-CCM+ use case with SSH enabled on the platform. You will need an SSH public key (you can create one by following this <a href="https://qarnot.com/documentation/use-ssh" target="_blank">tutorial</a>).

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/starccm/run_starccm_ssh.py"
     data-filename="run_starccm_ssh.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

To launch the calculation on Qarnot, copy the code above into a Python script in your working directory. Make sure you have:

- Copied your authentication token into the script, replacing `MY_SECRET_TOKEN`
- Copied your SSH public key into `DOCKER_SSH`

Then you can run `python3 run_starccm_ssh.py`.

> **Note:** the profile used must be your dedicated SSH profile, for example `starccm-qarnot-ssh`.

Once connected to the master node, you can launch a STAR-CCM+ simulation on your cluster with one of the following commands:

> `starccm+ -power -batch run cylindre_complet_extrusion_both_demi_DP_reconstruit_init.sim`

> `starccm+ -power -batch -mpi openmpi -mpiflags "--mca btl ^openib,tcp --mca pml ucx --mca osc ucx" -machinefile /job/mpihosts run cylindre_complet_extrusion_both_demi_DP_reconstruit_init.sim`

Where `-mpi openmpi`, `-mpiflags ...`, and `-machinefile /job/mpihosts` are the parameters required for a multi-node simulation.

## Results

You should now have a `cylindre-out` folder in your local working directory after a simple batch launch, or a `cylindre-advanced-out` folder if you use the advanced script. The same output bucket is also available on the <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC app</a> with all files generated by the simulation.

You can directly view certain images and log files generated by the simulation in your output bucket via the <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC app</a>.

Your results will be stored in the output bucket defined in the script and can be retrieved in three ways:
- Via the web platform: download directly from the Bucket section
- As shown in the Python script: using the <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/api/compute/task.html#qarnot.task.Task.download_results" target="_blank">download_results</a> function
- Or via one of the <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">open-source S3 bucket management applications</a>

For a large number of files or more than 5GB of data, we recommend using rclone (Linux) or Cyberduck (Windows). Both are <a href="https://qarnot.com/documentation/manage-data-dedicated-ui" target="_blank">open-source S3 management tools</a>.
