from datetime import datetime, timedelta

import pandas as pd


def validate_calendar_null_date(tmp: list):
    start_date = tmp[0][1]
    end_date = tmp[0][-1]

    date_range = pd.date_range(start=start_date, end=end_date)
    date_str_list = [date.strftime("%Y/%m/%d") for date in date_range]

    actual = tmp[0][1:]
    expected = date_str_list
    assert actual == expected, AssertionError(
        "Not all calendar information for the dates is available."
    )


def validates_24hours(sum_list: list):
    assert set(sum_list) == {"24.00"}, AssertionError(
        "Not 24 hours date exists."
    )  # noqa


def validate_bad_records(df: pd.DataFrame):
    assert not df[df["time"] == "#NUM!"].shape[0], AssertionError(
        "Bad records exist."
    )  # noqa
    print("Bad records num:", df[df["time"] == "#NUM!"].shape[0])


def validate_data_types(df):
    expected_data_types = {
        "date": "datetime64[ns]",
        "weekday": object,
        "calendar": object,
        "time": "float64",
    }

    for column, expected_type in expected_data_types.items():
        if df[column].dtype != expected_type:
            raise ValueError(
                f"Column '{column}' should be of type {expected_type}, but it is {df[column].dtype}"  # noqa
            )

    print("Data types validation passed!")


def validates_calculate_moving_average(
    df_long: pd.DataFrame, df_tmp: pd.DataFrame, check_date: str, window: int
):
    check_date_p = datetime.strptime(check_date, "%Y-%m-%d")
    # X日前の日付を計算
    start_date_p = check_date_p - timedelta(days=window - 1)
    # 新しい日付をyyyy-mm-dd形式の文字列型に変換
    start_date_p = start_date_p.strftime("%Y-%m-%d")
    df_tmp_20240101_raw = df_long.loc[start_date_p:check_date]
    actual = df_tmp_20240101_raw[df_tmp_20240101_raw["calendar"] == "friends"][
        "time"
    ].mean()
    df_tmp_20240101 = df_tmp[df_tmp["date"] == "2024/01/01"]
    expected = df_tmp_20240101[df_tmp_20240101["calendar"] == "friends"][
        "time"
    ].values[  # noqa
        0
    ]
    assert actual == expected, AssertionError(
        f"""
        Not calculate correct moving average.
        actual: {actual}
        expected: {expected}
        """
    )
