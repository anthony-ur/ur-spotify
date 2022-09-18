# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.194.3/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Python version: 3, 3.9, 3.8, 3.7, 3.6
ARG VARIANT="3.9"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# inspiration from https://github.com/ml-tooling/ml-workspace/blob/master/Dockerfile
ENV PYTHONUNBUFFERED 1

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive 

# Configure apt and install packages
RUN apt-get update && \
    apt-get -y install --no-install-recommends apt-utils dialog 2>&1 && \
    #
    # Verify git, process tools, lsb-release (common in install instructions for CLIs) installed
    apt-get -y install git iproute2 procps lsb-release cron curl && \
    #
    # odbc
    apt-get -y install unixodbc unixodbc-dev && \
    # upgrade to latest pip
    python -m pip install --upgrade pip && \
    #
    # Install pylint
    pip --disable-pip-version-check --no-cache-dir install pylint && \
    #
    # ===== Install MSSQL Client =====
    # must install unixodbc before mssql
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    # find appropriate package for OS version
    # curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/msprod.list && \
    sudo apt-get update && \
    # mssql tools will install sqlcmd, bcp, odbc driver and kerberos
    ACCEPT_EULA=Y apt-get install -y mssql-tools && \
    echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc && \
    bash -c "source ~/.bashrc" && \
    #
    # Install mongo tools
    wget https://fastdl.mongodb.org/tools/db/mongodb-database-tools-debian11-x86_64-100.5.3.deb && \
    apt install ./mongodb-database-tools-*.deb && \
    rm -f mongodb-database-tools-*.deb && \
    #
    # Clean up
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/* 


# Install Python dependencies if requirements file found
COPY requirements-dev.txt /tmp/pip-tmp/requirements.txt
RUN if [ -f "/tmp/pip-tmp/requirements.txt" ]; then pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp; fi

# set work directory
WORKDIR /workspace
ENV WORK_DIR=/workspace
ENV PYTHONPATH=${WORK_DIR}
ENV DBT_PROFILES_DIR=/workspace/.dbt

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog

# set shell
ENV SHELL /bin/bash 

EXPOSE 8080