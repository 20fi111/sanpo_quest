#ガチャの中身を更新するためのプログラム

import sqlite3

def main():
    conn = sqlite3.connect("../db/gacha.db")
    cur = conn.cursor()

    #choice.txtを開く
    with open("../db/choice.txt", "r") as file:

        #fileを行ごとに分割しリスト化する
        datalist = file.readlines()

        for data in datalist:
            #dataがすでにデータベースに存在しないかを調べる
            rows = cur.execute("SELECT COUNT (*) AS num FROM gachas WHERE choice = ?", (data,))
            count = rows.fetchone()[0]
            if count >= 1:
                continue

            #存在しなければデータベースに追加
            else:
                cur.execute("INSERT INTO gachas (choice) VALUES (?)", (data,))

    conn.commit()
    conn.close()

main()
