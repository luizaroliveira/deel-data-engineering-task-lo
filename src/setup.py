import os
import sys
import subprocess
import sqlalchemy

from src.database.database_connectors import PostgresConnector
from src.database.session import get_connection_arguments

def create_venv():
    """Creates a virtual environment for the project."""

    venv_name = ".venv"  # Standard virtual environment name

    if sys.platform.startswith("win"):
        python_executable = sys.executable
        venv_command = [python_executable, "-m", "venv", venv_name]
        activate_script = os.path.join(venv_name, "Scripts", "activate")
    else:  # Linux/macOS
        python_executable = sys.executable
        venv_command = [python_executable, "-m", "venv", venv_name]
        activate_script = os.path.join(venv_name, "bin", "activate")

    try:
        subprocess.check_call(venv_command)
        print(f"Virtual environment '{venv_name}' created successfully.")

        # Install requirements
        if sys.platform.startswith("win"):
            pip_executable = os.path.join(venv_name, "Scripts", "pip")
        else:
            pip_executable = os.path.join(venv_name, "bin", "pip")

        install_command = [pip_executable, "install", "-r", "requirements.txt"]  # Assumes requirements.txt exists
        subprocess.check_call(install_command)
        print("Requirements installed successfully.")

        print(f"To activate the virtual environment, run:\n{activate_script_instruction(activate_script)}")


    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
    except FileNotFoundError:
        print("requirements.txt not found. Install dependencies manually after activating the environment.")


def activate_script_instruction(activate_script):
    """Provides platform-specific instructions for activating the virtual environment."""

    if sys.platform.startswith("win"):
        return f"{activate_script}"
    else:  # Linux/macOS
        return f"source {activate_script}"


def init_database():

    connector = None
    session = None
    operations_manager = None

    connection_arguments = get_connection_arguments()
    connector = PostgresConnector(
        user=connection_arguments['DATABASE_USER'],
        password=connection_arguments['DATABASE_PASSWORD'],
        host=connection_arguments['DATABASE_HOST'],
        port=connection_arguments['DATABASE_PORT'],
        database=connection_arguments['DATABASE_DB']
    )

    session = connector.create_session()
    with open('database/init_script.sql', 'r') as file:
        sql_statements = file.read()
    
    for statement in sql_statements.strip().split(';'):
        if statement.strip():
            session.execute(sqlalchemy.text(statement))
            session.commit()

if __name__ == "__main__":
    create_venv()
    init_database()

