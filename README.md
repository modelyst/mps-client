# MPS client
A CLI Tool for Querying data within an instance of the Materials Provenance Store database.

## Installation
To install the latest version of mps-client use the following command
``` Python
pip install git+https://github.com/modelyst/mps-client.git
```
To further specify a version you can add a ref tag to the url like that shown below:
``` Python
pip install git+https://github.com/modelyst/mps-client.git
```

## Configuration
All configuration is done through a `.env` type file which loads environmental variables set on the CLI as well as in a local file. To see all the possible configuration variables you can run the command
```
mps-client config
```
The option `--simple` can show the commonly changed parameters (mainly those related to the database connections). The output of this command can be used to generate a starting `.env` file like so:

```
mps-client config --simple > .env
```

This new `.env` file can be filled in with credential details for interacting with the database. Make sure to add the `.env` file to any `.gitignore` file if you are working in a git repo so that you don't commit sensitive credentials to version control.

By default, mps-client tries to read the `.env` file in the current working directory. If you need to change this behavior you can set the environmental variable `MPS_ENV_FILE` to the path you would like to use for your current environment.

Additionally, any of the configuration variables set in the `.env` file can be set with an environmental variable like so:

```
export MPS_POSTGRES_PASSWORD=password
```
This can help keep sensitive credentials in working memory only and not in plaintext. Environmental variables will override any variable set in the `.env` file.

## Jupyter
An example Jupyter notebook and sql queries are provided under the jupyter/ directory showing how one can use mps_client in a jupyter environment. Configuration is still handled as above.
