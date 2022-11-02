import pandas as pd
from app import parse_table, fix_string

url = "https://www.commerce.wa.gov.au/labour-relations/public-holidays-western-australia"

table_unfixed = parse_table(my_url=url, df_idx=2)
table = table_unfixed.applymap(fix_string)


def test_fixing():
    assert table_unfixed["2022"][0] == "Saturday 1 January &  Monday 3 January"
    assert table_unfixed["2023"][0] == "Sunday 1 January &  Monday 2 January"


def test_header_row():
    assert table.columns[0] == "Unnamed: 0"
    assert table.columns[1] == '2022'
    assert table.columns[2] == '2023'
    assert table.columns[3] == '2024'


def test_header_column():
    assert table["Unnamed: 0"][0] == "New Year's Day"
    assert table["Unnamed: 0"][1] == "Australia Day"
    assert table["Unnamed: 0"][2] == "Labour Day"
    assert table["Unnamed: 0"][3] == "Good Friday"
    assert table["Unnamed: 0"][4] == "Easter Sunday"
    assert table["Unnamed: 0"][5] == "Easter Monday"
    assert table["Unnamed: 0"][6] == "Anzac Day"
    assert table["Unnamed: 0"][7] == "Western Australia Day"
    assert table["Unnamed: 0"][8] == "National Day of Mourning**"
    assert table["Unnamed: 0"][9] == "King's Birthday #"
    assert table["Unnamed: 0"][10] == "Christmas Day"
    assert table["Unnamed: 0"][11] == "Boxing Day"


def test_column_2022():
    assert table["2022"][0] == "Saturday 1 January & Monday 3 January"
    assert table["2022"][1] == "Wednesday 26 January"
    assert table["2022"][2] == "Monday 7 March"
    assert table["2022"][3] == "Friday 15 April"
    assert table["2022"][4] == "Sunday 17 April *"
    assert table["2022"][5] == "Monday 18 April"
    assert table["2022"][6] == "Monday 25 April"
    assert table["2022"][7] == "Monday 6 June"
    assert table["2022"][8] == "Thursday 22 September"
    assert table["2022"][9] == "Monday 26 September"
    assert table["2022"][10] == "Sunday 25 December & Monday 26 December***"
    assert table["2022"][11] == "Monday 26 December & Tuesday 27 December"


def test_column_2023():
    assert table["2023"][0] == "Sunday 1 January & Monday 2 January"
    assert table["2023"][1] == "Thursday 26 January"
    assert table["2023"][2] == "Monday 6 March"
    assert table["2023"][3] == "Friday 7 April"
    assert table["2023"][4] == "Sunday 9 April *"
    assert table["2023"][5] == "Monday 10 April"
    assert table["2023"][6] == "Tuesday 25 April"
    assert table["2023"][7] == "Monday 5 June"
    assert pd.isna(table["2023"][8]) == True
    assert table["2023"][9] == "Monday 25 September"
    assert table["2023"][10] == "Monday 25 December"
    assert table["2023"][11] == "Tuesday 26 December"


def test_column_2024():
    assert table["2024"][0] == "Monday 1 January"
    assert table["2024"][1] == "Friday 26 January"
    assert table["2024"][2] == "Monday 4 March"
    assert table["2024"][3] == "Friday 29 March"
    assert table["2024"][4] == "Sunday 31 March *"
    assert table["2024"][5] == "Monday 1 April"
    assert table["2024"][6] == "Thursday 25 April"
    assert table["2024"][7] == "Monday 3 June"
    assert pd.isna(table["2024"][8]) == True
    assert table["2024"][9] == "Monday 23 September"
    assert table["2024"][10] == "Wednesday 25 December"
    assert table["2024"][11] == "Thursday 26 December"

