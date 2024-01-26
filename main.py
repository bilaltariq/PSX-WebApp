import datetime
from psx import stocks, tickers
from database import Database

tickers = tickers()
db_name = 'db/primary.db'
db_instance = Database(db_name)


def main():
    sector_company_name_dict = tickers.groupby('sectorName')['name'].agg(list).to_dict()
    company_name_symbol_dict = tickers.groupby('name')['symbol'].agg(list).to_dict()

    for sector, companies in sector_company_name_dict.items():
        if sector == 'FERTILIZER':
            for company in companies:
                if company_name_symbol_dict[company][0] == 'EFERT':
                    data = stocks([company_name_symbol_dict[company][0]]
                                  , start=datetime.date(2024, 1, 1), end=datetime.date.today()).reset_index(inplace=False)
                    db_instance.connect()
                    ddl_for_data = db_instance.df_to_sqlite_dict(data)
                    db_instance.create_table(table_name='psx_data', columns_dict=ddl_for_data)
                    db_instance.insert_dataframe(table_name='psx_data', dataframe=data, if_exists_m='replace')
                    db_instance.close_connection()


if __name__ == '__main__':
    """
    Program begins from here. main()
    """
    main()
