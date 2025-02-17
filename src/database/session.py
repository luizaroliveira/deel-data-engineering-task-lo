import os
import yaml
def get_connection_arguments():
    """"
    Creates a database connection using a given cdatabase connector and default environment variables.
    """

    try:
        # Read a YAML file
        with open('connection_config.yaml', 'r') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError("connection config file is missing.")

    required_variables = {
        "DATABASE_USER": config["DATABASE_USER"],
        "DATABASE_PASSWORD": config["DATABASE_PASSWORD"],
        "DATABASE_HOST": config["DATABASE_HOST"],
        "DATABASE_PORT": config["DATABASE_PORT"],
        "DATABASE_DB": config["DATABASE_DB"]
    }


    if not all(required_variables.values()):
        missing_variables = [k for k,v in required_variables.items() if not v]
        raise KeyError(f"Missing environment variable(s) for database connection: {', '.join(missing_variables)}")
    return required_variables

