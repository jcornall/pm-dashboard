# pm-dashboard
A Grafana dashboard implementation offering unified observability over a suite of patch management tools. 

## Setup

### API Key - Environment Variables

Tenable API keys (an access key and a secret key) are required to properly execute this program. It is recommended that you set environment variables to keep the credentials on your system. A guide on how to do this can be found [here](ENV.md) - this guidance follows recommendations from OpenAI on the best practices for API Key Safety, available [here](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety).

### Virtual Environment

#### Windows

Set up the virtual environment and dependencies by typing the following commands:

```
python3.12 -m pip install virtualenv
python3.12 -m virtualenv .venv
source .\.venv\Scripts\activate
pip install -r requirements.txt
```

#### Linux

Linux users can set up the virtual environment and dependencies by navigating to the project directory and executing the install.sh shell script with the following command:

```
source ./install.sh
```

## Execution

### Windows

Activate the virtual environment with the following command:

```
source .venv/bin/activate
```

Execute the program with the following command:

```
python3.12 __main__.py
```

To deactivate the virtual environment after program execution is complete, use the following command:

```
deactivate
```

### Running database migrations

Before the first run, the database must first be migrated. [golang-migrate](https://github.com/golang-migrate/migrate) is used to handle database migration. To run all the migrations for each database, make sure the `golang-migrate` binary is downloaded first by running `install.sh`. Then, run:

```shell
./golang-migrate/migrate -path ./src/<insert pmt name>/migrations -database "mysql://user:pass@tcp(domain:port)/<db-name>" up
```

where:

- `<insert pmt name>` is the name of the patch management tool for which this migration is run, e.g. tenable
- `user` is the username of the database
- `pass` is the password used to identify the user
- `domain` is the domain at which the MySQL/MariaDB instance is running
- `port` is the port on which the DB is listening
- `<db-name>` is the name of the database that holds data for a specific patch management tool, e.g. tenable

Go to `docs/database.md` for further documentation on database.

