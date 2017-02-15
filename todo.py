import sqlite3
from bottle import route, run, debug, template, request, static_file, error
import os.path

if not os.path.exists("todo.db"):
    con = sqlite3.connect('todo.db')
    con.execute("CREATE TABLE todo (id INTEGER PRIMARY KEY, task char(100) NOT NULL, status bool NOT NULL)")
    con.commit()

@route('/hello')
def hello():
    hello = 'Hello World!!!!'
    return hello

@route('/todo')
@route('/')
def todo_list():
    # データベースに接続
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()

    # データベースにSQLのクエリを投げて問い合わせ todo テーブル
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")

    # 結果をresultに入れる c.fetchall() は Tupleを返す
    result = c.fetchall()

    # データベースの接続を終了する
    c.close()

    print(result)
    # resultをmake_table.tplを使って表示する
    output = template('make_table', rows=result)
    print(output)

    # response としてoutputを返す
    return output

@route('/new', method='GET')
def new_item():
    return template('new_task.tpl')

@route('/new', method='POST')
def create_item():
    # 前後の空白を除去 str.strip()
    new = request.POST.task.strip()

    # データベースに接続
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()

    # SQLをDBに発行
    c.execute("INSERT INTO todo (task,status) VALUES (?,?)", (new, 1))

    # テーブルの最後のIDを取得
    new_id = c.lastrowid

    # データベースの変更を確定　commit
    conn.commit()

    # データベースの接続を終了
    c.close()

    return '<p>The new task was inserted into the database, the ID is %s</p><a href="/">Back</a>' % new_id

@route('/edit/<no:int>', method='GET')
def edit_item(no):
    # 編集画面を表示
    # データベース接続
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()

    # DBにSQL発行 id が no なレコード
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (str(no),) )

    # 1件だけ取得 c.fetchone()
    cur_data = c.fetchone()

    return template('edit_task', old=cur_data, no=no)

@route('/edit/<no:int>', method='POST')
def update_item(no):
    # 変更処理
    edit = request.POST.task.strip()
    status = request.POST.status.strip()

    if status == 'open':
        status = 1
    else:
        status = 0

    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("UPDATE todo SET task = ?, status = ? WHERE id LIKE ?", (edit, status, no))
    conn.commit()

    return '<p>The item number %s was successfully updated</p><a href="/show/%s">Back</a>' % (no, no)

@route('/delete/<no:int>')
def delete_item(no):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("DELETE FROM todo WHERE id LIKE ?", (str(no),))
    conn.commit()

    return '<p>The item number %s was successfully deleted</p><a href="/">Back</a>' % no

@route('/show/<item:re:[0-9]+>')
def show_item(item):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (item,))
    result = c.fetchall()
    c.close()
    if not result:
        return 'This item number does not exist!'
    else:
        return template('show_task', item=result[0], no=item)
        # return 'Task: %s' % result[0]

@route('/help')
def help():
    return static_file('help.html', root='.')

@route('/json<json:re:[0-9]+>')
def show_json(json):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (json,))
    result = c.fetchall()
    c.close()

    if not result:
        return {'task': 'This item number does not exist!'}
    else:
        return {'task': result[0]}

@error(403)
def mistake403(code):
    return 'The parameter you passed has the wrong format!'

@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

# Webサーバーを立ち上げて待機する
run()
