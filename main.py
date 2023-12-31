import math

from flask import Flask, render_template, request, flash, redirect, url_for, session

from lib.authenticate import login_with_email
from lib import post_service, setting_service
from lib.config import PAGE_SIZE
from lib.utils import format_timestamp, parse_markdown, init_database

app = Flask(__name__)
app.secret_key = 'JOU*(EUWE:JLJijdla'
init_database()


@app.template_filter()
def format_time(timestamp):
    return format_timestamp(timestamp)


@app.context_processor
def inject_global_variables():
    site_name = setting_service.get("site_name")
    return {"site_name": site_name}


@app.route('/')
def home():
    page = int(request.args.get('page', 1))
    posts, total = post_service.get_enabled_posts(page, PAGE_SIZE)
    total_page = math.ceil(total / PAGE_SIZE)

    return render_template("home.html",
                           page=page,
                           total_page=total_page,
                           posts=posts,
                           total=total)


@app.route('/post/<id>')
def post(id: int):
    post = post_service.get_post(id)
    post["content_html"] = parse_markdown(post["content"])
    return render_template("post.html", post=post)


@app.route('/about')
def about_me():
    about = {
        "title": "About",
        "content_html": parse_markdown(setting_service.get("about"))
    }
    return render_template("post.html", post=about)


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
    posts, total = post_service.get_posts(page, PAGE_SIZE)
    total_page = math.ceil(total / PAGE_SIZE)

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
    enabled = 1 if ("enabled" in request.form and request.form["enabled"] is not None) else 0

    if id:
        post_service.update_post(id, title, content, enabled)
    else:
        id = post_service.add_post(title, content, enabled)

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
