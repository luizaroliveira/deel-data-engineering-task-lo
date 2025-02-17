import click
from sqlalchemy.exc import SQLAlchemyError
from database.database_connectors import PostgresConnector
from database.session import get_connection_arguments
from operations.operations_manager import OperationsManager

connector = None
session = None
operations_manager = None

try:
    connection_arguments = get_connection_arguments()
    connector = PostgresConnector(
        user=connection_arguments['DATABASE_USER'],
        password=connection_arguments['DATABASE_PASSWORD'],
        host=connection_arguments['DATABASE_HOST'],
        port=connection_arguments['DATABASE_PORT'],
        database=connection_arguments['DATABASE_DB']
    )

    session = connector.create_session()
    operations_manager = OperationsManager(session)
except KeyError as e:
    print(f"Missing environment variable necessary for Database connection: {e}")
    exit(1)
except SQLAlchemyError as e:
    print(f"Database error: {e}")
    exit(1)
except Exception as e:
    print(f"An unexpected error occurred when trying to connect to the database: {e}")
    exit(1)


@click.group()
def cli():
    """Report generator CLI."""
    pass

@cli.command()
def list():
    """
    Lists all export operations currently available.
    """

    if operations_manager.available_operations:
        for op in operations_manager.available_operations.values():
            click.echo(f'{op.report_id} - {op.report_description}')
        click.echo(f'Please use the command export.')
    else:
        click.echo('No operations available.')


@cli.command()
@click.argument('operation')
@click.argument('params', nargs=-1)
def export(operation: str, params):
    """
    Runs an export operation from the list
    """
    if operation not in operations_manager.available_operations.keys():
        click.echo("Invalid operation!")
        click.echo("Please select an operation number from the list below:")
        for op in operations_manager.available_operations.values():
            click.echo(f'{op.report_id} - {op.report_description}')
        return

    try:
        result = operations_manager.run_operation(operation, params)
        if result["status"] == "success":
            click.echo(result["message"])
        else:
            click.echo(f"Error: {result['message']}")
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    cli()
