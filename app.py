import pandas as pd
from tabulate import tabulate
from dateutil.parser import parse
from models import Holiday
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dictionaries import int_to_month, int_to_weekday
import unicodedata


def fix_string(my_str):
    """ Function that removes extra empty spaces and normalizes string
    :param my_str: string provided to process
    :type my_str: str
    :return: returns a fixed string
    :return type: str
    """
    if type(my_str) is str:
        my_lst = my_str.split(" ")
        my_lst = [unicodedata.normalize("NFKD", i) for i in my_lst if i]
        my_str = ' '.join(my_lst)

    return my_str


def parse_table(my_url, df_idx):
    """Function that fetches and parses a table from a provided url
    :param my_url: provided url
    :type my_url: str
    :param df_idx: idx of a table in a dataframe
    :type df_idx: int
    :return: returns parsed table
    :return type: pandas.DataFrame
    """
    # read all tables from html into pandas dataframe
    df = pd.read_html(my_url, flavor='bs4')
    # table of interest is the table with index 2
    sub_df = df[df_idx]
    return sub_df


if __name__ == "__main__":
    url = "https://www.commerce.wa.gov.au/labour-relations/public-holidays-western-australia"
    table = parse_table(url, 2)

    table = table.applymap(fix_string)

    # print(tabulate(table, headers='keys', tablefmt='psql'))

    # rename the unnamed column
    table.rename(columns={"Unnamed: 0": "Holiday Name"}, inplace=True)

    # slice only necessary columns
    table_years = table[['Holiday Name', '2022', '2023']]

    # replace asterix character in entire dataframe
    table_years = table_years.replace('\*','', regex=True)

    # split column with dates into several columns if there is more than one date
    # in the given table. These dates are concatenated with & character
    # column for each year is in this case split into two columns
    new_table_2022 = table_years['2022'].str.split('&', 1, expand=True)
    new_table_2023 = table_years['2023'].str.split('&', 1, expand=True)

    # add column with holiday name to
    new_table_2022['Holiday Name'] = table_years['Holiday Name']
    new_table_2023['Holiday Name'] = table_years['Holiday Name']

    df1, df2 = new_table_2022[['Holiday Name', 0]], new_table_2022[['Holiday Name', 1]]
    df3, df4 = new_table_2023[['Holiday Name', 0]], new_table_2023[['Holiday Name', 1]]

    df1['Year'], df2['Year'] = 2022, 2022
    df3['Year'], df4['Year'] = 2023, 2023

    # rename columns, so they could be stacked on top of each other
    df2.rename(columns={1: 0}, inplace=True)
    df4.rename(columns={1: 0}, inplace=True)

    # stack all records on top of each other
    final = pd.concat([df1, df2, df3, df4])

    # drop records where there is no date
    final.dropna(subset=[0], how='all', inplace=True)

    # reset index
    final.reset_index(drop=True, inplace=True)

    final[0] = final[0] + " " + final['Year'].astype(str)

    # convert date string in datetime object
    final['Holiday Date'] = final[0].apply(lambda x: parse(x))

    # create several columns of interest
    final['Day'] = final['Holiday Date'].apply(lambda x: int_to_weekday[x.isoweekday()])
    final['Month'] = final['Holiday Date'].apply(lambda x: int_to_month[x.month])

    result = final[['Holiday Name', 'Day', 'Month', 'Year', 'Holiday Date']]

    # print pandas dataframe
    print("\n--------------------------------------   TASK 2   --------------------------------------\n")
    print(tabulate(result, headers='keys', tablefmt="grid"))

    # in memory sqlite database
    connection_argument = "sqlite://"

    # create connection
    Base = declarative_base()
    engine = create_engine(connection_argument)
    session = Session(engine)

    # drop sql table into pandas dataframe
    result.to_sql('holiday', engine, index=True, index_label='id',  if_exists='replace')

    # check if the results are stored in the database
    query_results = session.query(Holiday).all()
    # print(f"Number of records in the database: {len(query_results)}")

    # read sql table from pandas dataframe
    results_from_db = pd.read_sql_table('holiday', engine, index_col='id')

    # print results from pandas dataframe
    print("\n---------------------------------------   TASK 4   ---------------------------------------\n")
    print(tabulate(results_from_db, headers='keys', tablefmt="grid"))