import math

from flask import Flask, render_template, request, flash, redirect, url_for, session

from lib.authenticate import login_with_email
from lib import post_service
from lib.config import ADMIN_PAGE_SIZE

app = Flask(__name__)
app.secret_key = 'JOU*(EUWE:JLJijdla'


@app.route('/')
def home():
    return 'Hello World!'


@app.route('/post/<id>')
def post(id: int):
    return 'Hello World!'


@app.route('/login', methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST':
        if not login_with_email(request):
            error = 'Invalid credentials'
        else:
            session["username"] = request.form["email"]
            flash('You were successfully logged in')
            return redirect(url_for('get_posts'))
    return render_template('login.html', error=error)


def check_login():
    if 'username' not in session:
        flash("Not login yet!")
        return redirect("/")


@app.route('/admin')
def get_posts():
    check_login()
    page = int(request.args.get('page', 1))
    posts, total = post_service.get_posts(page, ADMIN_PAGE_SIZE)
    total_page = math.ceil(total / ADMIN_PAGE_SIZE)

    return render_template("admin/home.html",
                           page=page,
                           total_page=total_page,
                           posts=posts,
                           total=total)


@app.route('/admin/posts/add')
def add_post():
    check_login()
    return render_template("admin/post.html")


@app.route('/admin/posts/edit/<id>')
def edit_post(id: int):
    check_login()
    post = post_service.get_post(id)
    return render_template("admin/post.html", post=post)


@app.post('/admin/posts/save')
def save_post():
    check_login()
    id = int(request.form["id"])
    title = request.form["title"]
    content = request.form["content"]

    if id:
        post_service.update_post(id, title, content)
    else:
        id = post_service.add_post(title, content)

    flash('Save successfully')
    return redirect(f"/admin/posts/edit/{id}")


@app.route('/admin/posts/delete/<id>')
def delete_post(id: int):
    flash('Delete successfully')
    post_service.delete_post(id)
    return redirect("/admin")


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
