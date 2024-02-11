#!/usr/bin/env python
# coding: utf-8

from datetime import datetime

import pandas as pd
from config import designated_date, window
from constants import JSON_PATH, SHEET_NAME, SS_ID
from dateutil.relativedelta import relativedelta
from logzero import logger
from utils import (
    LogSettingRunner,
    correct_bad_records,
    create_df_long,
    get_worksheet_values,
    output_graph,
)
from validates import (
    ValidatorCalendarValue,
    validate_bad_records,
    validate_calendar_null_date,
    validate_data_types,
    validates_calculate_moving_average,
)


def main(window, designated_date):
    # ログの設定
    LogSettingRunner.run()

    # ローデータを取得する
    sheet = get_worksheet_values(JSON_PATH, SS_ID, SHEET_NAME)
    validate_calendar_null_date(sheet)
    vcv = ValidatorCalendarValue(sheet)
    vcv.head_oflist_oflists()
    vcv.date_format()
    vcv.weekday_format()
    vcv.calendar_format()
    print("Here")
    # 縦持ちのデータを作る
    df_long = create_df_long(sheet)
    logger.info(
        f"Bad records num:{df_long[df_long['time'] == '#NUM!'].shape[0]}",
    )

    # 不正なレコードを修正する
    bad_rec_index = df_long[df_long["time"] == "#NUM!"].index.tolist()
    logger.info(f"Bad records index:{bad_rec_index}")
    df_long = correct_bad_records(df_long, bad_rec_index)
    validate_bad_records(df_long)

    # データ型の定義:型の前提をここでFIXする
    df_long["date"] = pd.to_datetime(df_long["date"])
    df_long["time"] = df_long["time"].astype(float)
    validate_data_types(df_long)

    # 移動平均の計算準備のため
    df_long.set_index("date", inplace=True)
    df_long.sort_index(inplace=True)

    # 移動平均の計算
    df_calc_ma = (
        df_long.groupby("calendar")["time"]
        .rolling(window=window, min_periods=1)
        .mean()
        .reset_index()
    )
    validates_calculate_moving_average(
        df_long, df_calc_ma, "2024-01-01", window
    )  # noqa

    # 指定日からwindow分の移動平均を描画するため
    designated_date = datetime.strptime(designated_date, "%Y-%m-%d")
    min_date = designated_date - relativedelta(days=window - 1)
    df_calc_maspecified_period = df_calc_ma[
        (df_calc_ma["date"] >= min_date)
        & (df_calc_ma["date"] <= designated_date)  # noqa
    ].sort_values(by="date")

    # データフレームをピボットして日付ごとにカレンダーカテゴリの時間を積み上げる
    df_pivot = df_calc_maspecified_period.pivot_table(
        index="date", columns="calendar", values="time", aggfunc="sum"
    )
    # 重要な順番で下から積み上がるようにするため
    df_pivot = df_pivot[
        [
            "sleep",
            "regularrevenue",
            "vook_newbusiness",
            "house",
            "friends",
            "morningroutine",
            "study",
            "training",
            "move",
            "personal",
        ]
    ]
    output_graph(df_pivot, window, True)


if __name__ == "__main__":
    main(window, designated_date)
