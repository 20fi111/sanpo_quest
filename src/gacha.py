import sqlite3
import random



def get_all_item():
    conn = sqlite3.connect("gacha.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursur()
    cur.execute("select * from gachas")
    result = [dict(row) for row in cur.fetchall()]

    print(result)
    conn.close()
    return result

def random_choice(result):
    todays_choice = random.sample(result,k=3)
    choiceA = todays_choice["0"]
    choiceB = todays_choice["1"]
    choiceC = todays_choice["2"]

    return choiceA,choiceB,choiceC

get_all_item()

