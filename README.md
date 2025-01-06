# openCollector
Open Source RPI Data Collection Platform

# Environment Setup

The development environment consists of a docker-compose setup with one container for the collector and storage node and other containers for related services. The current workflow for setting up development environments is standardized to use [Development Containers](https://containers.dev/). This makes reproduction of the environment very easy. The cost is that while the devcontainer tool is an open standard, IDE support on IDEs other than VSCode or Neovim is minimal. If you wish to use different IDE, manual installation instructions will need to be created.

## Devcontainer

[Development Containers](https://containers.dev/) allows the use of Docker containers as full-featured development environments.

### Windows, VSCode

1. Install the [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install). This may require changing Windows or Bios settings for virtualization.
2. Install Docker Engine through [Docker Desktop](https://www.docker.com/products/docker-desktop/). Start Docker Engine.
3. Install [VSCode](https://code.visualstudio.com/) and the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension.
4. Run the VSCode command `Clone repository into container volume.` and enter the name of the repository: `compsust/openCollector`. Cloning the repository into the container brings optimal performance, but if that doesn't work, clone the repository into a Windows folder and run the command in VSCode `Run folder in container.`

The container should display a terminal with no errors. Detailed 

### Troubleshooting

- Is Docker Engine running?

## Linux

Instructions for the use of Devcontainers on Linux should be simpler than on Windows, but the instructions have not been created yet. If you follow this path, please update this document.

## Non-devcontainer

Instructions for manual setup of the environment have not yet been created. If you follow this path, please update this document.