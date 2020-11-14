"""
In this script, I will define the login_required decorator
its validate is there a user logged in or not
"""
import functools
from flask import render_template, session, redirect, url_for

def login_required(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('id') is None:
            return redirect(url_for('login'))
        return func(*args, **kwargs)

    return wrapper