FROM <qarnot-provided-roce-base-image>:<tag-provided-by-qarnot>

COPY mpi_test/run_mpi_demo.sh /opt/roce-demo/run_mpi_demo.sh
COPY wrapper.sh /opt/qarnot/wrapper

RUN chmod +x /opt/roce-demo/run_mpi_demo.sh \
 && chmod +x /opt/qarnot/wrapper

# Set to 1.0.0 to ignore
ENV DOCKER_BUILD_SOFT_VERSION=5.0.9
