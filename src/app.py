from flask import Flask, flash, redirect, render_template, request, session, redirect
from functools import wraps
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from gacha import random_choice,get_all_item

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#データベースを使用できるようにする
conn = sqlite3.connect("../db/gacha.db")
cur = conn.cursor()

def login_required(f):
    #ログインされているか確認する関数
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
@login_required
def index():
    #ホームページ
    return render_template("index.html")


@app.route("/quest", methods=["GET", "POST"])
@login_required
def quest():
    #クエスト詳細画面
    conn = sqlite3.connect("../db/gacha.db")
    cur = conn.cursor()
    #デイリークエスト
    db = cur.execute("SELECT * FROM dailys")
    dailys = db.fetchall()

    #メインクエスト
    db2 = cur.execute("SELECT * FROM spots WHERE boolean_clear = 0")
    spots = db2.fetchall()

    return render_template("quest.html", dailys=dailys)


@app.route("/achieve_quest", methods=["GET", "POST"])
@login_required
def achieve_quest():
    if request.method == "POST":
        id = request.form.get("id")
        conn = sqlite3.connect("../db/gacha.db")
        cur = conn.cursor()
        cur.execute("UPDATE dailys SET boolean_clear = 1 WHERE id = ?", (id, ))

        return redirect("/quest")


@app.route("/gacha",methods=["GET","POST"])
@login_required
def gacha():
    #ガチャ画面
    #ボタンと表示のページ
    return render_template("gacha.html")

@app.route("/run_gacha",methods=["POST"])
@login_required
def run_gacha():
        #ガチャの実行
        daily = random_choice()
        choiceA=daily[0]
        choiceB=daily[1]
        choiceC=daily[2]


        #データベースに結果を入れる
        #gacha.dbの中のchoicesを更新

        conn = sqlite3.connect("../db/gacha.db")
        cur = conn.cursor()
        count1 = cur.execute("SELECT COUNT (*) FROM dailys WHERE id = 1")
        if count1.fetchone()[0] >= 1:
            cur.execute("UPDATE dailys SET choice=? WHERE id = 1", (choiceA, ))
        else:
            cur.execute("INSERT INTO dailys (choice) VALUES (?)", (choiceA, ))

        count2 = cur.execute("SELECT COUNT (*) FROM dailys WHERE id = 2")
        if count2.fetchone()[0] >= 1:
            cur.execute("UPDATE dailys SET choice=? WHERE id = 2", (choiceB, ))
        else:
            cur.execute("INSERT INTO dailys (choice) VALUES (?)", (choiceB, ))

        count3 = cur.execute("SELECT COUNT (*) FROM dailys WHERE id = 3")
        if count3.fetchone()[0] >= 1:
            cur.execute("UPDATE dailys SET choice=? WHERE id = 3", (choiceC, ))
        else:
            cur.execute("INSERT INTO dailys (choice) VALUES (?)", (choiceC, ))

        conn.commit()
        conn.close()



        #ガチャ結果画面に表示
        return render_template("result.html",choiceA=choiceA,choiceB=choiceB,choiceC=choiceC)



@app.route("/login", methods=["GET", "POST"])
def login():
    #ログイン画面
    session.clear()

    if request.method == "POST":
        #IDとパスワードを取得
        user_id = request.form.get("userid")    #userid
        password = request.form.get("password") #password

        #IDが入力されていない
        if not user_id:
            flash("IDを入力してください")   #flash
            return render_template("login.html")

        #パスワードが入力されていない
        elif not password:
            flash("パスワードを入力してください")
            return render_template("login.html")

        else:
            #データベースからIDを検索し、パスワードが正しいか確認する
            conn = sqlite3.connect("../db/gacha.db")
            cur = conn.cursor()
            rows = cur.execute("SELECT * FROM users WHERE username = ?", (user_id,))
            count = rows.fetchall()

            if  len(count) != 1 or not check_password_hash(count[0][2], password):
                flash("IDもしくはパスワードが違います")
                return render_template("login.html")

            #ログイン
            session["user_id"] = count[0][0]

            conn.close()
        #メインページへリダイレクト
        return redirect("/")

    else:
        return render_template("login.html")    #login.html


@app.route("/logout")
def logout():
    #ログアウト
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    #新規登録画面
    if request.method == "POST":

        user_id = request.form.get("userid")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not user_id:
            flash("IDを入力してください")
            return render_template("register.html")

        elif not password:
            flash("パスワードを入力してください")
            return render_template("register.html")

        elif not confirmation:
            flash("パスワードは2回入力してください")
            return render_template("register.html")

        elif password != confirmation:
            flash("2つのパスワードが異なっています")
            return render_template("register.html")

        else:
            #データベースに接続
            conn = sqlite3.connect("../db/gacha.db")
            cur = conn.cursor()
            rows = cur.execute("SELECT * FROM users WHERE username = ?", (user_id,))
            count = rows.fetchall()

            if len(count) == 1:
                flash("この名前はすでに使われています")
                return render_template("register.html")

            else:
                #新規登録
                password_hash = generate_password_hash(password)
                cur.execute("INSERT INTO users (username, hash) VALUES(?, ?)", (user_id, password_hash))
                conn.commit()

                #データベース上のid取得
                id = cur.execute("SELECT * FROM users WHERE username = ?", (user_id,))

                #ログイン
                session["user_id"] = user_id[0][0]

                conn.close()
                #メインページへリダイレクト
                return redirect("/")

    else:
        return render_template("register.html")


