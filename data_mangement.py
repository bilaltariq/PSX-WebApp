import pandas as pd
from datetime import timedelta

class DataManagement:
    def __init__(self, db):
        self.dbInstance = db

    def check_if_data_exists_in_db(self, table_name, symbol, end_date):
        self.dbInstance.connect()
        df = self.dbInstance.select_table(table_name=table_name)
        self.dbInstance.close_connection()

        df = df[df['Ticker'] == symbol]
        if len(df) > 0:
            max_date_db = df['Date'].max()
            max_date_db = pd.to_datetime(max_date_db).date()
            if max_date_db < end_date:
                return {'start': max_date_db + timedelta(days=1), 'end': end_date}
            else:
                return None

        return 'Full'
