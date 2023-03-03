import sqlite3
import random
import pandas as pd


def get_all_item():
    conn = sqlite3.connect("gacha.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("select * from gachas")
    result = [dict(row) for row in cur.fetchall()]

    print(result)
    conn.close()
    return result

def random_choice():
    choices = get_all_item()
    todays_choice = [d.get('choice') for d in choices]
    three_choices = random.sample(todays_choice,3)


    print(three_choices)
    choiceA = three_choices[0]
    choiceB = three_choices[1]
    choiceC = three_choices[2]

    print(choiceA,choiceB,choiceC)

    return choiceA,choiceB,choiceC

random_choice()