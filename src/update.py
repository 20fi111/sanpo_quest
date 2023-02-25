#ガチャの中身を更新するためのプログラム

from cs50 import SQL

def main():
    open("src/gacha.db", "w").close()
    db = SQL("sqlite:///src/gacha.db")

    #データベースを作成
    db.execute("CREATE TABLE gachas(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, choice TEXT)")

    #choice.txtを開く
    with open("src/choice.txt", "r") as file:

        #fileを行ごとに分割しリスト化する
        datalist = file.readlines()

        for data in datalist:
            #dataがすでにデータベースに存在しないかを調べる
            rows = db.execute("SELECT * FROM gachas WHERE choice = ?", data)
            if len(rows) == 1:
                continue

            #存在しなければデータベースに追加
            else:
                db.execute("INSERT INTO gachas (choice) VALUES(?)", data)


main()
