import datetime
from psx import stocks, tickers
from database import Database
from data_mangement import DataManagement

tickers = tickers()
db_name = 'db/primary.db'
db_instance = Database(db_name)
data_mgmt = DataManagement(db_instance)


def insert_meta_data(df, table_name):
    db_instance.connect()
    ddl_for_data = db_instance.df_to_sqlite_dict(df)
    db_instance.create_table(table_name=table_name, columns_dict=ddl_for_data)
    db_instance.insert_dataframe(table_name=table_name, dataframe=df, if_exists_m='replace')

def insert_stk_data(data_table, table_name, insert_type):

    db_instance.connect()
    ddl_for_data = db_instance.df_to_sqlite_dict(data_table)
    db_instance.create_table(table_name=table_name, columns_dict=ddl_for_data)
    if insert_type == 'Full':
        db_instance.insert_dataframe(table_name=table_name, dataframe=data_table, if_exists_m='replace')
        db_instance.close_connection()
    elif insert_type == 'Partial':
        db_instance.insert_dataframe(table_name=table_name, dataframe=data_table, if_exists_m='append')
        db_instance.close_connection()


def get_data(company, start_date, end_date):
    data = stocks([company], start=start_date, end=end_date).reset_index(inplace=False)
    return data


def main():
    start_date = datetime.date(2015, 1, 1)
    end_date = datetime.date(datetime.date.today().year, datetime.date.today().month, datetime.date.today().day)
    table = "psx_data"

    insert_meta_data(tickers, 'meta_data')

    sector_company_name_dict = tickers.groupby('sectorName')['name'].agg(list).to_dict()
    company_name_symbol_dict = tickers.groupby('name')['symbol'].agg(list).to_dict()

    print(tickers.head(5))

    for sector, companies in sector_company_name_dict.items():
        if sector == 'FERTILIZER':
            for company in companies:

                sym = company_name_symbol_dict[company][0]
                if sym == 'EFERT':

                    chk = data_mgmt.check_if_data_exists_in_db(table_name=table, symbol=sym, end_date=end_date)
                    if chk == 'Full':
                        data = get_data(company=sym, start_date=start_date, end_date=end_date)
                        insert_stk_data(data_table=data, table_name=table, insert_type='Full')

                    elif chk is None:
                        print(f'Data present for {sym} in database.')

                    else:
                        data = get_data(company=sym, start_date=chk['start'], end_date=chk['end'])
                        insert_stk_data(data_table=data, table_name=table, insert_type='Partial')


if __name__ == '__main__':
    """
    Program begins from here. main()
    """
    main()
