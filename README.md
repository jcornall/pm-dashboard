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
