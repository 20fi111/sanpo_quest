import sqlite3
import random
import pandas as pd


def get_all_item():

    # データベースに接続
    conn = sqlite3.connect("../db/gacha.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("select * from gachas")
    result = [dict(row) for row in cur.fetchall()]



    conn.close()
    return result

def random_choice():

    choices = get_all_item()

    # 辞書から値だけ取り出してリストで保存し、重複なし＆ランダムで３つ（任意の数に変更可能）を抽出
    todays_choice = [d.get('choice') for d in choices]
    three_choices = random.sample(todays_choice,3)


    choiceA = three_choices[0]
    choiceB = three_choices[1]
    choiceC = three_choices[2]



    return choiceA,choiceB,choiceC

# 一連の動作が行われるか確認のため呼び出し

