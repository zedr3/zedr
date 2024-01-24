from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.zedr'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.id

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        post = Post(title=title, text=text)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи произошел трабл"

    else:
        return render_template('create.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/posts')
def posts():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts)


@app.route('/posts/<int:id>')
def detail(id):
    details = Post.query.get(id)
    return render_template('detail.html', details=details)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    details = Post.query.get_or_404(id)

    try:
        db.session.delete(details)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении произошла ошибка"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    details = Post.query.get(id)
    if request.method == 'POST':
        details.title = request.form['title']
        details.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании статьи произошел трабл"

    else:
        return render_template('post_update.html', details=details)




if __name__ == "__main__":
    app.run(debug=True)