from flask import Flask, flash, redirect, render_template, request, session, redirect
from functools import wraps
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

#データベースを使用できるようにする
conn = sqlite3.connect("db/gacha.db")
cur = conn.cursor()

@app.route("/")
@login_required
def index():
    #ホームページ


@app.route("/quest")
@login_required
def quest():
    #クエスト詳細画面


@app.route("/gacha")
@login_required
def gacha():
    #ガチャ画面


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

        #パスワードが入力されていない
        elif not password:
            flash("パスワードを入力してください")
        
        #データベースからIDを検索し、パスワードが正しいか確認する
        rows = cur.execute("SELECT * FROM users WHERE username = ?", (user_id,))
        count = rows.fetchall()

        if  len(count) != 1 or not check_password_hash(count[0][2], password):
            flash("IDもしくはパスワードが違います")
        
        #ログイン
        session["user_id"] = count[0][0]

        #メインページへリダイレクト
        return redirect("/")
    
    else:
        return render_template("login.html")    #login.html


@app.route("/logout")
def logout():
    #ログアウト
    session.clear()
    return redirect("/")


@app.route("/register")
def register():
    #新規登録画面
    if request.method == "POST":

        user_id = request.form.get("userid")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not user_id:
            flash("IDを入力してください")

        elif not password:
            flash("パスワードを入力してください")

        elif not confirmation:
            flash("パスワードは2回入力してください")

        elif password != confirmation:
            flash("2つのパスワードが異なっています")
        
        rows = cur.execute("SELECT * FROM users WHERE username = ?", (user_id,))
        count = rows.fetchall()

        if count == 1:
            flash("この名前はすでに使われています")

        #新規登録
        password_hash = generate_password_hash(password)
        cur.execute("INSERT INTO users (username, hash) VALUES(?, ?)", (user_id, password_hash))

        #データベース上のid取得
        id = cur.execute("SELECT * FROM users WHERE username = ?", (user_id,))

        #ログイン
        session["user_id"] = user_id[0][0]

        #メインページへリダイレクト
        return redirect("/")
    
    else:
        return render_template("register.html")


def login_required(f):
    #ログインされているか確認する関数
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function