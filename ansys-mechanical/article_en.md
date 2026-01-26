ANSYS Mechanical is a multidisciplinary numerical simulation software suite based on the Finite Element Method (FEM), designed for static, dynamic, and thermal analysis of structures and components. It stands as a reference for evaluating strength, durability, kinematics, and thermal behavior in engineering systems.

The software is widely used in industries such as aerospace, automotive, energy, and electronics to validate prototypes virtually and reduce the need for costly physical tests, thereby accelerating the design and development cycle. It also offers advanced integration with other tools in the ANSYS suite, enabling complex coupled simulations (fluid-mechanical, thermal-structural, etc.).

## Licensing

To launch an Ansys Mechanical simulation on Qarnot, you must grant us access to your license. For more details, please contact our team via <a href="mailto:support-compute@qarnot-computing.com" target="_blank">support-compute@qarnot-computing.com</a>.

From this point forward, we will assume that your license configuration with us is already complete.

## Versions

The versions of Ansys Mechanical available on Qarnot are listed in our <a href="https://qarnot.com/en/software/ansys-mechanical-qanot" target="_blank">catalogue</a>.

If you are interested in another version, please send us an email at <a href="mailto:support-compute@qarnot-computing.com" target="_blank">support-compute@qarnot-computing.com</a>.

## Launching a task on Qarnot

There are two ways to launch a task on Qarnot:
- Via our web interface <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC</a>
- Using a script with a SDK

The rest of this blog post focuses on launching via Python scripts for increased automation and speed.

## Prerequisites

Before launching a calculation with the Python SDK, a few steps are required:
- <a href="https://app.qarnot.com/register" target="_blank">Create an account</a>
- Retrieve your <a href="https://app.qarnot.com/settings/access-token" target="_blank">API authentication token</a>
- <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/installation.html" target="_blank">Install the Qarnot Python SDK</a>
- Know your Qarnot profile, for example `ansys-mechanical-e-corp` and `ansys-mechanical-e-corp-vnc`

**Note**: In addition to the Python SDK, Qarnot also provides SDKs for <a href="https://doc.tasq.qarnot.com/documentation/sdk-csharp/" target="_blank">C#</a> and <a href="https://doc.tasq.qarnot.com/documentation/sdk-nodejs/" target="_blank">Node.js</a>, as well as a Command Line Interface (<a href="https://doc.tasq.qarnot.com/documentation/cli/man/ManIndex.html" target="_blank">CLI</a>).

## Test Case

This test case will show you how to launch the official v8 benchmark model. You will need the files <a href="https://27028395.fs1.hubspotusercontent-eu1.net/hubfs/27028395/%5BMARCOM%5D%20Blog%20site%20HPC/ansys-mecha/V24direct-1.dat" target="_blank">V24direct-1.dat</a> and <a href="https://27028395.fs1.hubspotusercontent-eu1.net/hubfs/27028395/%5BMARCOM%5D%20Blog%20site%20HPC/ansys-mecha/V24direct-1geom.db" target="_blank">V24direct-1geom.db</a> from the <a href="https://ansyshelp.ansys.com/public/account/secured?returnurl=/Views/Secured/corp/v242/en/wb_vm/wbvt-vm-mech-wb.html" target="_blank">Ansys website</a>.

Once the files are downloaded, place them in a directory named `v8-in`.

## Running the test case

Once everything is configured, use the `run-ansys-mechanical.py` script below to launch the calculation on Qarnot.

To launch the calculation, save the code above as a Python script in your working directory. Before running it, make sure to update the following constants at the beginning of the script:
- Replace `MY_SECRET_TOKEN` with your actual authentication token, which can be <a href="http://app.qarnot.com/settings/access-token" target="_blank">retrieved here</a>.

<pre>
.
├── v8-in/
│   ├── V24direct-1.dat
│   ├── V24direct-1geom.db
└── run-ansys-mechanical.py
</pre>

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/ansys-mechanical/run-ansys-mechanical.py"
     data-filename="run-ansys-mechanical.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

To run this script, simply execute `python3 run-ansys-mechanical.py` in your terminal.

You now know how to launch an Ansys Mechanical task on Qarnot!

## Advanced batch launch script

The script presented below allows you to explore more advanced platform features for batch launching.

<div class="wf-code-card"
     data-url="https://cdn.jsdelivr.net/gh/qarnot/blog-samples@main/ansys-mechanical/run-ansys-mechanical_batch.py"
     data-filename="run-ansys-mechanical_batch.py"
     data-language="python"
     data-linenumbers="true"
     data-maxheight="65vh"
     data-fontsize="13px"
     data-download="true"
     data-copy="true"></div>

## Results

You should now have a `v8-out` folder in your local working directory and the same `v8-out` on the <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC app</a> containing all output files.

You can directly view certain images and log files generated by the simulation in your output bucket via the <a href="https://app.qarnot.com/my-simulations" target="_blank">HPC app</a>.

Your results will be stored in the `v8-out` bucket and can be retrieved in three ways:
- Via the web platform: download directly from the Bucket section.
- As shown in the Python script: using the <a href="https://doc.tasq.qarnot.com/documentation/sdk-python/api/compute/task.html#qarnot.task.Task.download_results" target="_blank">download_results</a> function.
- Or via one of the <a href="https://qarnot.com/documentation/manage-your-data-with-a-dedicated-ui" target="_blank">open-source S3 bucket management applications</a>.

For large quantities of files or data exceeding 5GB, we recommend using rclone (Linux) or Cyberduck (Windows). Both are <a href="https://qarnot.com/documentation/manage-your-data-with-a-dedicated-ui" target="_blank">open-source S3 management tools</a>.