#!/bin/bash

set -euo pipefail

# Loaded automatically by /qarnot/utils/roce_wrapper before the simulation steps.
function setup_environment(){
    export ROCE_DEMO_IMAGE_READY=true
    export ROCE_DEMO_IMAGE_SCRIPT=/opt/roce-demo/run_mpi_demo.sh
    export ROCE_DEMO_CLUSTER_SCRIPT=/share/run_mpi_demo.sh
    export ROCE_DEMO_QHOST=/share/qhost

    cat <<'EXTRA_ENV' > /etc/profile.d/qarnot_90_roce_demo_env.sh
#!/bin/bash
export ROCE_DEMO_IMAGE_READY=true
export ROCE_DEMO_IMAGE_SCRIPT=/opt/roce-demo/run_mpi_demo.sh
export ROCE_DEMO_CLUSTER_SCRIPT=/share/run_mpi_demo.sh
export ROCE_DEMO_QHOST=/share/qhost
EXTRA_ENV

    if [ ! -f "$ROCE_DEMO_CLUSTER_SCRIPT" ]; then
        cp "$ROCE_DEMO_IMAGE_SCRIPT" "$ROCE_DEMO_CLUSTER_SCRIPT"
    fi

    chmod +x "$ROCE_DEMO_CLUSTER_SCRIPT"
}

function main(){
    setup_environment

    # This runtime version check must match DOCKER_BUILD_SOFT_VERSION from the Dockerfile.
    export QARNOT_GET_SOFT_VERSION="mpirun --version 2>/dev/null | sed -n '1s/^mpirun (Open MPI) //p' | xargs"
}

main "$@"
