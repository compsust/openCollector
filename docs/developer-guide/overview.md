# Overview

Overall, the OpenCollector system is made up of two components:

1. A Python / Micropython program which reads sensor data and uploads it to a database on a loop.
2.  A Python webserver which reads data from the database and exposes it to a REST API and browser interface.

This developer guide provides technical details on how these components are set up and instructions on how to work on the codebase.

See the documentation sections for each sub-project:

- [Collector](./collector/overview.md)
- [Storage](./storage/overview.md)

## Project Structure

The project is split up into sections, each with one folder in the root of the repository:

- `collector` for the collector node code.
- `storage` for the storage node code.
- `common` for code common to the two nodes, such as metadata for the supported sensors.
- `docs` for this documentation site.

The [UV package manager](https://docs.astral.sh/uv/) is used to manage dependencies. A file called `pyproject.toml` is used to store metadata about the project such as its dependencies. There is a `pyproject.toml` file in the root of the repository, which specifies the dependencies used throughout the entire repository, as well as one `pyproject.toml` in each of the `common`, `storage`, and `collector` directories which specifies the dependencies required for each sub-project.

The `collector` and `storage` sub-projects both specify a local path dependency to the `common` directory.

The following commands are available using `uv`:

- `uv sync` - this installs the dependencies into the environment, and is run automatically after container creation.
- `uv sync --active` - because of the way `uv` handles depdendencies in sub-projects, to install the dependencies of a sub-project it may be required to navigate to the sub-project directory and run this so that `uv` installs the dependencies specified in the sub-project's `pyproject.toml` and not the one at the root of the repository.
- `uv add` - this is used to add a dependency to the `pyproject.toml`. Note that it will add the dependency to the sub-project the command is run in.
- `uv add --dev` - for development-only dependencies.
- `uv run <command>` - used to run commands made available by the dependencies installed by `uv` 
- `uv run ruff format` this runs the code formatter.
- `uv run ruff check --fix` this runs the code linter.

See the individual sub-project folders of this documentation for commands specific to each project.

## Environment Setup

The development environment may be set up manually or it may be produced using [Development Containers](https://containers.dev/). The benefit to using devcontainers is that reproduction of the environment, including a QuestDB instance, is easy and configurable. The downside is that docker is required to be running on your development machine, and support for IDEs other than VSCode is lacking.

Note that if you are only editing the documentation, no steps other than cloning the repository is needed as the documentation is build using a Github Action, however previewing the documentation does require installing the development dependencies. If you are just working on the collector code and don't need to test a database connection, you may skip using Docker and Devcontainers as the main advantage of that is easy installation of QuestDB.

### Devcontainer

[Development Containers](https://containers.dev/) allows the use of Docker containers as full-featured development environments.

#### Operating System

##### Windows

Using devcontainers on Windows requires Linux virtualization as Docker cannot run natively on Windows.

1. Install the [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install). This may require changing Windows or Bios settings for virtualization.
2. Install Docker Engine through [Docker Desktop](https://www.docker.com/products/docker-desktop/). Start Docker Engine.

##### Linux

1. Install Docker Engine through [Docker Desktop](https://www.docker.com/products/docker-desktop/) or on its own. Start Docker Engine.

#### Editor

##### VSCode

1. Install [VSCode](https://code.visualstudio.com/) and the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension.
2. Run the VSCode command `Clone repository into container volume.` and enter the name of the repository: `compsust/openCollector`. Cloning the repository into the container brings optimal performance, but if that doesn't work, clone the repository into a Windows folder and run the command in VSCode `Run folder in container.`

The container should display a terminal with no errors.

##### Other Editors

Devcontainers should work with other IDEs such as Neovim, but setup instructions aren't included here at this time.

#### Troubleshooting

- Is Docker Engine running?

### Manual

Use a manual environment when Docker is unavailable or when you only need one sub-project.

1. Install Git, Python 3.13 or later, and [uv](https://docs.astral.sh/uv/getting-started/installation/).
2. Clone the repository and install the root development dependencies:

    ```bash
    git clone https://github.com/compsust/openCollector.git
    cd openCollector
    uv sync --dev
    ```

3. When working on a sub-project, change into `collector` or `storage` and run `uv sync --active` so uv installs that sub-project's dependencies and its local dependency on `common`.
4. Install and start [QuestDB](https://questdb.com/docs/quick-start/) if the work requires database integration. Copy `storage/.env.example` to `storage/.env` and make its PostgreSQL connection settings match the QuestDB instance.
5. Run the checks used by the project before submitting a change:

    ```bash
    uv run ruff format --check .
    uv run ruff check .
    uv run mkdocs build --strict
    ```

To preview documentation locally, run `uv run mkdocs serve` from the repository root and open the address printed in the terminal. See the [user setup guide](../user-guide/setup.md) for starting the storage application and database.

## Supporting New Sensors

To add a new sensor to the software, see the instructions located in the [sensors page](./collector/sensors.md)
