from flask import session, flash, redirect, request

from lib.config import EMAIL, PASSWORD


def login_with_email(request):
    email = request.form['email']
    password = request.form['password']
    return email == EMAIL and password == PASSWORD
