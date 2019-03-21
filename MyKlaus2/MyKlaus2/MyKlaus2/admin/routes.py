from flask import Blueprint, render_template, flash, redirect, url_for
from myklaus2.admin.forms import LoginForm

admin = Blueprint("admin", __name__)

@admin.route("/admin", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.user.data == "admin" and form.pwd.data == "password":
            flash("Login Erfolgreich! (TODO: Login Check)", "success")
            return redirect(url_for('main.home'))
        else:
            flash("Nope! (TODO: Login Check)", "danger")
    return render_template("admin/login.html", form=form, title="Admin Login")