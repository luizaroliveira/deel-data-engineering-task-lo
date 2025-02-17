from operations.utils import has_sql_code

from database.models import ReportOperations


class ReportOperationsQueryBuilder():
    """
    Builds SQL queries for report operations.
    This class interfaces the operations saved in the database with client input arguments to generate the final version of the queris that will be needed to generate the reports.
    """

    def validate_operation_params(self, operation: ReportOperations, cli_arguments: object) -> object:
        min_expected_argument_count = len([p for p in operation.arguments if not p.optional])

        # Not expecting any arguments.
        if (not operation.arguments
                or (min_expected_argument_count == 0 and len(cli_arguments) == 0)):
            return True

        for argument in operation.arguments:
            try:
                argument_text = str(list(cli_arguments)[argument.argument_position]).strip('"').strip("'")
                if has_sql_code(argument_text):
                    raise ValueError(f"Please don't try injecting SQL into the parameters! These operations can be tracked.")
            except IndexError as e:
                raise ValueError(f"Invalid parameters. Usage example: {operation.argument_usage}")
        return True

    def proccess_query(self, operation, cli_arguments):        
        """
        Processes the query string replacing placeholders with the given arguments.
        """

        where_block_string = " "
        where_block_arguments = {arg.associated_field: cli_arguments[arg.argument_position]
                        for arg in operation.arguments
                       if not arg.embedded and arg.block == 'where'}

        other_block_arguments = {arg.block: cli_arguments[arg.argument_position]
                                 for arg in operation.arguments
                                 if not arg.embedded and arg.block != 'where'}

        embedded_arguments = {arg.argument_name: cli_arguments[arg.argument_position]
                                 for arg in operation.arguments
                                 if arg.embedded}

        # Generating the where block if necessary
        for position, (key, value) in enumerate(where_block_arguments.items()):
            if position ==0 :
                where_block_string += f'WHERE {key} = {value}'
            else:
                where_block_string += f' AND {key} = {value}'
        if where_block_string != " ":
            operation.query = operation.query.replace('{where}', where_block_string)

        # Replacing query polaceholders for other blocks and embedded arguments
        for argument, value in {**other_block_arguments, **embedded_arguments}.items():
            operation.query = operation.query.replace(f"{{{argument}}}", value)

    def prepare_query(self, operation: ReportOperations, cli_arguments):
        """"
        Validates the arguments, check for sql injections and fills the base query with the user inputs.
        """
        self.validate_operation_params(operation, cli_arguments)
        self.proccess_query(operation, cli_arguments)
