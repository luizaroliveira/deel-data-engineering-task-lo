import os
from sqlalchemy.orm import Session
from database.models import ReportOperations, ReportOperationsArguments # Correct import
from database.query_builder import ReportOperationsQueryBuilder as QueryBuilder
from operations.csv_report_generator import CSVReportGenerator
from sqlalchemy.exc import SQLAlchemyError


class OperationsManager():
    """
    Manages database operations and report generation.
    """

    _available_operations = None

    def __init__(self, session: Session) -> None:
        self.session = session

        # For filling the base queries with the user inputs
        self.query_builder = QueryBuilder()
        
        # The amount of data, in rows, that will be transfered at once to avoid OOM errors.
        chunk_size = int(os.environ.get("CHUNK_SIZE", 10000))
        
        # For exporting the output as CSV
        self.report_exporter = CSVReportGenerator(session, chunk_size)
        

    @property
    def available_operations(self):

        if self._available_operations:
            return self._available_operations


        try:
            self._available_operations = {str(op.report_id): op for op in self.session.query(ReportOperations).all()}
            if not self.available_operations:
                raise ValueError("No operations found in the database.")
            return self._available_operations
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error while fetching operations: {e}") from e
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred while fetching operations: {e}") from e

    def run_operation(self, operation_id: str, params: tuple, file_path: str = None):
        """"
        Runs an export operation, by operation_id.        
        """
        try:
            operation = self.available_operations.get(operation_id)
            if not operation:
                raise ValueError(f"Operation with ID '{operation_id}' not found.")
            self.query_builder.prepare_query(operation, params)
            result = self.report_exporter.export_csv(operation, file_path)
            return result
        except ValueError as e:
            return {"status": "error", "message": str(e)}
        except SQLAlchemyError as e:
            return {"status": "error", "message": f"Database error during operation execution: {e}"}
        except Exception as e:
            return {"status": "error", "message": f"An unexpected error occurred during operation execution: {e}"}


