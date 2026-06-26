#!/bin/bash

set -euo pipefail

SHARE_DIR="/share"
QHOST_FILE="$SHARE_DIR/qhost"
QHOST_COPY="$SHARE_DIR/qhost.txt"
MPIHOSTS_FILE="${SETUP_CLUSTER_MPIHOST_FILENAME:-${QARNOT_RESOURCES_DIRECTORY:-/job}/mpihosts}"
MPIHOSTS_COPY="$SHARE_DIR/mpihosts.txt"
MPI_LOG="$SHARE_DIR/mpi-demo.log"
MPI_RANKS_FILE="$SHARE_DIR/mpi-ranks.txt"
SUMMARY_FILE="$SHARE_DIR/summary.txt"
INSTANCE_COUNT_VALUE="${INSTANCE_COUNT:-${QARNOT_INSTANCE_COUNT:-2}}"
SLOTS_PER_NODE="${SETUP_CLUSTER_NB_SLOTS:-1}"
TOTAL_MPI_SLOTS="$((SLOTS_PER_NODE * INSTANCE_COUNT_VALUE))"
MPI_RANKS="${MPI_RANKS:-$TOTAL_MPI_SLOTS}"

cp "$QHOST_FILE" "$QHOST_COPY"
if [ -f "$MPIHOSTS_FILE" ]; then
    cp "$MPIHOSTS_FILE" "$MPIHOSTS_COPY"
fi
: > "$MPI_RANKS_FILE"

{
    echo "MPI demo started at $(date -Iseconds)"
    echo "Using hostfile: $QHOST_FILE"
    echo "Using mpihosts file: $MPIHOSTS_FILE"
    echo "SETUP_CLUSTER_NB_SLOTS (slots per node): $SLOTS_PER_NODE"
    echo "INSTANCE_COUNT (number of nodes): $INSTANCE_COUNT_VALUE"
    echo "Total MPI slots available: $TOTAL_MPI_SLOTS"
    echo "Requested ranks: $MPI_RANKS"
    echo "Contents of /share/qhost:"
    cat "$QHOST_FILE"
    if [ -f "$MPIHOSTS_FILE" ]; then
        echo "Contents of mpihosts:"
        cat "$MPIHOSTS_FILE"
    fi
} | tee "$MPI_LOG"

mpirun ${QARNOT_MPI_ARGS:-} --hostfile "$QHOST_FILE" -np "$MPI_RANKS" /bin/bash -lc '
set -euo pipefail
rank="${OMPI_COMM_WORLD_RANK:-${PMI_RANK:-0}}"
host="$(hostname)"
printf "rank=%s host=%s\n" "$rank" "$host" | tee -a /share/mpi-ranks.txt
'

{
    echo
    echo "MPI ranks recorded in /share/mpi-ranks.txt"
    echo "Slots per node from SETUP_CLUSTER_NB_SLOTS: $SLOTS_PER_NODE"
    echo "Node count from INSTANCE_COUNT: $INSTANCE_COUNT_VALUE"
    echo "Total MPI slots available: $TOTAL_MPI_SLOTS"
    echo "Unique hosts detected:"
    awk '{print $2}' "$MPI_RANKS_FILE" | cut -d'=' -f2 | sort -u
    echo
    echo "Core output files:"
    printf '%s\n' "$MPI_LOG" "$MPI_RANKS_FILE" "$QHOST_COPY" "$SUMMARY_FILE"
    if [ -f "$MPIHOSTS_COPY" ]; then
        printf '%s\n' "$MPIHOSTS_COPY"
    fi
} | tee "$SUMMARY_FILE"
