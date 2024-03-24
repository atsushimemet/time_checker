import sys
from datetime import datetime, timedelta

import pandas as pd
from logzero import logger


def validate_calendar_null_date(tmp: list):
    start_date = tmp[0][1]
    end_date = tmp[0][-1]

    date_range = pd.date_range(start=start_date, end=end_date)
    date_str_list = [date.strftime("%Y/%m/%d") for date in date_range]

    actual = tmp[0][1:]
    expected = date_str_list
    try:
        assert actual == expected, AssertionError(
            ("Not all calendar information for the dates is available.")
        )
    except AssertionError as e:
        logger.warning(e)
        sys.exit(2)


class ValidatorCalendarValue:
    def __init__(self, sheet):
        self.sheet = sheet
        self.date_list = sheet[0]
        self.weekday_list = sheet[1]
        self.calendar_list = sheet[2:]

    def head_oflist_oflists(self):
        l_head = [a_list[0] for a_list in self.sheet]
        expected = [
            "date",
            "weekday",
            "Sleep",
            "MorningRoutine",
            "Personal",
            "RegularRevenue",
            "House",
            "Vook&NewBusiness",
            "Friends",
            "Training",
            "Move",
            "Study",
            "sum",
        ]
        assert l_head == expected, AssertionError(
            f"Check head of list of lists.\n\tl_head:{l_head}\n\texpected:{expected}"
        )

    def date_format(self):
        for date_str in self.date_list[1:]:
            try:
                # yyyy/mm/dd 形式で日付が正しいか確認
                datetime.strptime(date_str, "%Y/%m/%d")
            except ValueError:
                # 日付が指定された形式でない場合はFalseを返す
                return False
        # すべての日付が指定された形式である場合はTrueを返す
        return True

    def weekday_format(self):
        valid_weekdays = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        expected = set(valid_weekdays)
        assert set(self.weekday_list[1:]) == expected

    def calendar_format(self):
        for calendar_list in self.calendar_list:
            for item in calendar_list[1:]:
                # 特定の文字列のチェック
                if item == "#NUM!":
                    continue
                # 整数の文字列のチェック
                elif "." not in item:
                    raise ValueError(f"items is integer:{item}")
                # 浮動小数点数の文字列のチェック
                try:
                    str(float(item)) == item
                    continue
                except ValueError:
                    raise ValueError(f"Invalid element found: {item}")


def validates_24hours(sum_list: list):
    assert set(sum_list) == {"24.00"}, AssertionError(
        f"Not 24 hours date exists.\nsum_list set is {set(sum_list)}"
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
    start_date_s = start_date_p.strftime("%Y-%m-%d")
    df_tmp_20240101_raw = df_long.loc[start_date_s:check_date]  # type: ignore
    # NOTE: Ignoring type check due to Mypy's inability to handle dynamic typing used by pandas for date range slicing.
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
