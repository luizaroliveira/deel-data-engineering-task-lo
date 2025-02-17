import csv
import shutil
import os
from tempfile import NamedTemporaryFile

from sqlalchemy import text
from sqlalchemy.orm import Session
from database.models import ReportOperations
import datetime

class CSVReportGenerator():
    """
    Generates CSV reports from database queries.
    """

    def __init__(self, session: Session, chunk_size: int = 1000):
        self.session = session
        self.chunk_size = chunk_size

    def export_csv(self, report_operation: ReportOperations, csv_filepath=None):
        """
        Exports query results to a CSV file incrementally.
        """

        if not csv_filepath:
            ts_now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            csv_filepath = f"{report_operation.report_description.replace(' ', '_')}_{ts_now}.csv"
        try:
            with NamedTemporaryFile(mode='w', delete=False, newline='', encoding='utf-8', suffix='.csv') as tmp_csvfile:
                writer = csv.writer(tmp_csvfile)

                with self.session.execute(text(report_operation.query)) as result:
                    column_names = result.keys()
                    
                    # Testing if there is data to write before writing the header
                    chunk = result.fetchmany(self.chunk_size)
                    if chunk:
                        writer.writerow(column_names)
                        for row in chunk:
                            writer.writerow(row)
                    else:
                        tmp_csvfile.close()
                        os.unlink(tmp_csvfile.name)
                        return {"status": "success", "message": "The report has completed successfuly, but found no data to be exported."}

                    # Writing the rest of the file.        
                    while True:
                        chunk = result.fetchmany(self.chunk_size)
                        for row in chunk:
                            writer.writerow(row)
                        if not chunk:  # No more rows
                            break
                    temp_file_path = tmp_csvfile.name
                shutil.move(temp_file_path, csv_filepath)
            return {"status": "success", "message": f"Export finished successfully!\nOutput file: {csv_filepath}"}
            
        except Exception as e:
            return {"status": "error", "message": f"Error exporting to CSV: {e}"}

        finally:
            self.session.close()
