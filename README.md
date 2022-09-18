# UR Spotify

Welcome to the UR (Untitled Research): Spotify Project.

This repository contains all code and neccessary assets for creating a highly functional Spotify data store.

## Overview

### Purpose
The goal of this project is to ingest, process and analyze Spotify data. Insights/feedback found in the analysis will drive future project direction.


### Build with

 - Docker - container runtime
 - VSCode - IDE (preferred)
 - Git - version control system
 - Python
 - Snowflake - database
 - dbt - data build tool for data transformations [dbt](https://www.getdbt.com/)

### Repository structure

```
├── [.dbt]                   <- DBT working directory which drives profile/target currently used when running
├── [.devcontainer]          <- Development container - bootstrapped environment with Docker - use VSCode Remote Development extension
│   ├── profiles.yml         <- Models for final dw organized by business unit (marts)
├── [.vscode]                <- VSCode IDE settings and tasks (customizable)
├── [docs]                   <- Project documentation, including contribution and style guides
├── [misc]                   <- Miscellaneous sql scripts
├── [privileges]             <- Database privileges and security rules
├── [target]                 <- Working directory for dbt, when running final compiled SQL et al. will be here (local directory only)
├── [transform]              <- Transformation logic (dbt project root)
│   ├── [analysis]           <- Analysis files
│   ├── [docs]               <- dbt generated docs home
│   ├── [macros]             <- dbt macros
│   ├── [models]             <- Models home folder, organized by data workflow stage and purpose
│   │   ├── [base]           <- Base models, reflection of sources that comforms naming and data types
│   │   ├── [prep]           <- Data preparation models, generally preparing from base and for UDW
│   │   ├── [source]         <- Models for source data landed, as is from source systems
│   │   ├── [udw]            <- Models for final master data warehouse, central "source of truth"
│   │   └── [workspace]      <- Workspace models
│   ├── [profiles]           <- dbt profile templates which can be used to swich processing target
│   ├── [seeds]              <- Seed data
│   ├── [snapshots]          <- dbt snapshots
│   └── [tests]              <- dbt tests
├── [utils]                  <- Utility scripts
├── .env                     <- environment variables (this file is must be created locally, it will contain your personal security credentials and settings and always stays local)
├── .gitignore               <- git repository configuration file which governs which elements are NOT commited to the common repository
├── dbt_project.yml          <- dbt project config file
├── packages.yml             <- dbt packages
├── README.md                <- The top-level README for developers using this project.
├── requirements-dev.txt     <- The requirements file for dev packages                               
└── template.env             <- Template file for your local env setup, needs to be copied, renamed to ".env" and filled in with developer credentials upon initial setup
```

## Getting Started 

### Setting up dev environment

For best experience we recommend running this project within VSCode with Docker based Dev container
This section reflects setup with VSCode. You can however bring your own IDE and configure your repo workspace as you wish.

#### Install Requirements
To set up the local development environment for this project, the following must be installed:

 - [Docker Desktop](https://www.docker.com/products/docker-desktop) 
 - VSCode with [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension
 - [git](https://git-scm.com/downloads)  


#### Set up local environment

1. Clone this git repo
2. Make sure Docker Desktop is running (we recommend running docker in Hyper-V mode, and increasing the default RAM allocation)
3. Start VS Code and open this project folder ("judge-udw", the repo just cloned)
4. Create new **.env** file with your specific environmental variables (use [template.env](./template.env), fill in your credentials and settings)
5. (re)Start VS Code with [Development Session inside Container](https://code.visualstudio.com/docs/remote/containers#_quick-start-open-an-existing-folder-in-a-container). On first run the development containers will take a few minutes to build.
6. Create **.dbt/profiles.yml** with appropriate dbt profiles (use [dev-profiles.yml](./profiles/dev-profiles.yml) as template, should be good to use as is just copy and rename)
7. Create any necessary databases on target DB engine (sync with .env, e.g. "USERNAME_PREP", "USERNAME_UDW",etc.)
8. Test dbt configuration with `dbt debug`
9. Run `dbt deps` to install dependencies

### Running dbt commands

Try running the following commands:
```bash
# test connection setup
dbt debug
# generate & serve docs (see project doc/dag)
dbt docs generate && dbt docs serve
# build dbt models (run all code, without actually executing in the DB)
dbt build
# run dbt models
dbt run
# run select dbt model(s), in this example job_order
dbt run --select +udw.job_order+ # run udw.job_order model, including all upstream and downstream models
dbt run --select +udw.job_order # run udw.job_order model including all upstream models that udw.job_order depends on
dbt run --select udw.job_order+ # run udw.job_order model including all downstream models that depend on udw.job_order
dbt run --select udw.job_order # run udw.job_order model only
# run dbt tests
dbt test
```

You can find more project setup information here [project-setup.md](./docs/project-setup.md)  
You can find project notes here [project-notes.md](./docs/project-notes.md)
