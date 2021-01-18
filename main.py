#from flask import Flask, render_template # これだけだったけど、
from flask import Flask, render_template, request, redirect # 追加で2つimportする
from flask_sqlalchemy import SQLAlchemy

# Faskのインスタンスを作成
app = Flask(__name__)
# SQLAlchemyを使ってDBを作成する
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

#DBのテーブルの設定をする。
#Postはテーブル名。
class Post(db.Model):
    # IDは整数。主キー。
    id = db.Column(db.Integer, primary_key=True)
    # titleはToDoListの内容。文字列。空っぽは禁止。
    title = db.Column(db.String(50), nullable=False)

#todo.dbファイルの作成。DBのテーブルを作る。
#db.create_all()

# ルーティングの指定
#@app.route('/') # 元々はこれだったけど
@app.route('/', methods=['GET', 'POST'])
def index():
    #GETメソッドでアクセスされた場合
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('index.html', posts=posts)
    #GETメソッド以外でアクセスされた場合（POSTメソッドのとき）
    else:
        title = request.form.get('title')
        
        new_post = Post(title=title)
        
        #フォームから届いたデータをデータベースのテーブルに入れる
        db.session.add(new_post)
        #コミットする（上書き保存する）
        db.session.commit()

        #指定したページに飛ばす
        return redirect('/')

# タスクの追加ページ
@app.route('/create')
def create():
    return render_template('create.html')

# タスクの削除
@app.route('/delete/<int:id>')
def delete(id):
    #SQLのSELECT文
    post = Post.query.get(id)

    #指定されたIDのテーブルのレコードを削除する
    db.session.delete(post)
    db.session.commit()
    return redirect('/')

# デバッグモードでサーバを起動させる
app.run(debug=True, host='0.0.0.0')
