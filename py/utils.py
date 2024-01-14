import os
from datetime import datetime

import gspread
import logzero
import matplotlib.pyplot as plt
import pandas as pd
from config import designated_date
from logzero import logger
from oauth2client.service_account import ServiceAccountCredentials
from validates import validates_24hours


class ColorCodes:
    SLEEP = "#AD1357"
    REGULARREVENUE = "#D71A60"
    VOOK_NEWBUSINESS = "#7CB342"
    HOUSE = "#795548"
    FRIENDS = "#009688"
    MORNINGROUTINE = "#F4511E"
    STUDY = "#AD1357"
    TRAINING = "#3F50B5"
    MOVE = "#616161"
    PERSONAL = "#7886CB"


class LogSettingRunner:
    def run():
        # ログディレクトリのパス
        log_directory = "log"

        # 現在の日時を取得
        current_time = datetime.now()
        # フォーマットされた日時文字列を生成 (yyyy-mm-dd-HH:MM:SS)
        timestamp = current_time.strftime("%Y-%m-%d-%H:%M:%S")
        # ファイル名を生成
        log_file_name = f"{timestamp}.txt"

        # ログの設定
        logzero.logfile(os.path.join(log_directory, log_file_name))


def get_worksheet_values(json_path: str, ss_id: str, sheet_name: str):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    # Credentials 情報を取得
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        json_path, scopes
    )  # noqa
    # OAuth2のクレデンシャルを使用してGoogleAPIにログイン
    gc = gspread.authorize(credentials)
    # IDを指定して、Googleスプレッドシートのワークブックを選択する
    workbook = gc.open_by_key(ss_id)
    # シート名を指定して、ワークシートを選択
    worksheet = workbook.worksheet(sheet_name)
    # スプレッドシートをDataFrameに取り込む
    return worksheet.get_values()


def create_df_long(sheet: list) -> pd.DataFrame:
    # データフレームに使用するリスト
    date_list = sheet[0][1:]
    weekday_list = sheet[1][1:]
    sleep_list = sheet[2][1:]
    morningroutine_list = sheet[3][1:]
    personal_list = sheet[4][1:]
    regularrevenue_list = sheet[5][1:]
    house_list = sheet[6][1:]
    vook_newbusiness_list = sheet[7][1:]
    friends_list = sheet[8][1:]
    training_list = sheet[9][1:]
    move_list = sheet[10][1:]
    study_list = sheet[11][1:]
    sum_list = sheet[12][1:]
    validates_24hours(sum_list)

    tmp = pd.DataFrame(
        {
            "date": date_list,
            "weekday": weekday_list,
            "sleep": sleep_list,
            "morningroutine": morningroutine_list,
            "personal": personal_list,
            "regularrevenue": regularrevenue_list,
            "house": house_list,
            "vook_newbusiness": vook_newbusiness_list,
            "friends": friends_list,
            "training": training_list,
            "move": move_list,
            "study": study_list,
        }
    )

    tmp = tmp.melt(
        id_vars=["date", "weekday"], var_name="calendar", value_name="time"
    )  # noqa
    return tmp.sort_values(["date", "weekday", "calendar"])


def correct_bad_records(df: pd.DataFrame, bad_rec_index: list) -> pd.DataFrame:
    for idx in bad_rec_index:
        d = df.loc[idx].date
        w = df.loc[idx].weekday
        c = df.loc[idx].calendar
        t = df[df["date"] == d]["time"].tolist()
        if t.count("#NUM!") == 0:
            continue
        elif t.count("#NUM!") == 1:
            complement = str(24.00 - sum([float(v) for v in t if v != "#NUM!"]))  # noqa
            df.loc[idx] = [d, w, c, complement]
        else:
            c = t.count("#NUM!")
            complement = str(
                (24.00 - sum([float(v) for v in t if v != "#NUM!"])) / c
            )  # noqa
            df_tmp = df[df["date"] == d].replace("#NUM!", complement)
            df = pd.concat([df[df["date"] != d], df_tmp])
    return df


def output_graph(df: pd.DataFrame, window: int, save: bool = False):
    plt.rcParams["font.family"] = "Times New Roman"  # font familyの設定

    color = [
        ColorCodes.SLEEP,
        ColorCodes.REGULARREVENUE,
        ColorCodes.VOOK_NEWBUSINESS,
        ColorCodes.HOUSE,
        ColorCodes.FRIENDS,
        ColorCodes.MORNINGROUTINE,
        ColorCodes.STUDY,
        ColorCodes.TRAINING,
        ColorCodes.MOVE,
        ColorCodes.PERSONAL,
    ]

    # 積み上げ棒グラフを描画
    ax = df.plot(
        kind="bar",
        stacked=True,
        figsize=(10, 7),
        color=color,
        edgecolor="#00081A",
        alpha=0.75,
    )

    # グラフにタイトルと軸ラベルを追加
    plt.title("Stacked Bar Chart of Time by Google Calendar")
    plt.xlabel("Date")
    plt.ylabel("Total Time")

    # 凡例をグラフの右外側に表示
    plt.legend(title="Calendar", loc="center left", bbox_to_anchor=(1, 0.5))

    # x軸の日付表記をカスタマイズ（冗長な部分を省略）
    date_labels = df.index.strftime("%Y-%m-%d")
    ax.set_xticklabels(date_labels)

    # グラフの表示範囲の調整
    plt.tight_layout()

    # y軸の範囲を0から24までに設定
    plt.ylim(0, 24)
    plt.yticks(range(0, 25, 3))

    # グラフを保存
    if save:
        # 現在の日時を取得
        current_time = datetime.now()
        # フォーマットされた日時文字列を生成 (yyyy-mm-dd-HH:MM:SS)
        timestamp = current_time.strftime("%Y-%m-%d-%H:%M:%S")
        # ファイル名を生成
        graph_file_name = f"{timestamp}_{designated_date}.png"
        if window == 7:
            plt.savefig(f"./graph/weekly/{graph_file_name}")
        elif window == 30:
            plt.savefig(f"./graph/monthly/{graph_file_name}")
        else:
            logger.warning("bad window config is set.")

    # グラフを表示
    plt.show()
