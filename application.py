from typing import Text
from flask import Flask,render_template,request

#DBアクセス用ライブラリ
import pyodbc

#日付取得用
import datetime

#DB接続
def connectSQL():
    server = 'mcdev001.database.windows.net'
    database = 'DMRE_Demo_1st'
    username = 'mcroot'
    password = 'mlG0klf$3_6r'   
    driver= '{ODBC Driver 17 for SQL Server}'
    conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()
    print("SQL Connect OK")
    return conn,cursor

#DB切断
def closeSQL(_cursor,_conn):
    _cursor.close()
    _conn.close()
    print("SQL Close OK")
    return

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main_page_GET():
    text = "ここに結果が出力されます"
    return render_template("page.html",text=text)

@app.route("/", methods=["POST"])
def main_page_POST():

    cn,cur = connectSQL()

    cur.execute("select * from Table_D_テストテーブル")
    rows = cur.fetchall()
#    rows = [[1,'2021-05-01','入庫','AAAA'],[2,'2021-05-02','入庫','BBBB'],[3,'2021-05-01','出庫','CCCC'],[4,'2021-05-03','入庫','DDDD'],[5,'2021-05-01','出庫','EEEE'],[6,'2021-05-02','入庫','FFFF'],[7,'2021-05-04','出庫','GGGG']]
    closeSQL(cur,cn)

    rows2 = []

    input_id = request.form["input_id"]
    kind = request.form["kind"]
    reg_date = str(datetime.date.today())
    input_data = request.form["input_data"]
    print("登録ID：" + input_id)
    print("種別：" + kind)
    print("登録日：" + reg_date)
    print("登録内容：" + input_data)

    if input_id != "":
        text = "入力された登録ＩＤは" + input_id + "です。"
        for r in rows:
            if int(input_id) == r[0]:
                text2 ="入力したＩＤが重複しています。"
                return render_template("page.html",text=text,text2=text2)

        print("DBに登録")
        text2 ="登録しました。 種別：" + kind + "　　登録日：" + reg_date + "　　登録内容：" + input_data  

        cn,cur = connectSQL()
#        sql = "INSERT INTO [dbo].[Table_D_テストテーブル] ([ID],[日付],[種別],[内容]) VALUES (%x,%s,%s,%s)"
#        val = (int(input_id), reg_date, kind, input_data)
#        cur.execute(sql, val)
        cur.execute("INSERT INTO Table_D_テストテーブル (ID,日付,種別,内容) VALUES (15,"2021-05-10","入庫","abcdef")")


        closeSQL(cur,cn)

        return render_template("page.html",text=text,text2=text2)

    else:
        text = "登録IDが入力されていません。"     
        return render_template("page.html",text=text)

## 実行
if __name__ == "__main__":
    app.run(debug=True)