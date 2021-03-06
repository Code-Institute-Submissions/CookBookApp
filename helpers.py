from flask import Flask, render_template, redirect, request, url_for, session, flash
from natsort import natsorted
from operator import itemgetter
import re
import db_users

# Set username
def username_set_or_none():
    if 'username' in session:
        username = session['username']
    else:
        username = None
    return username

# Get user_id to store in sessions
def user_id_for_session(username):
    id_data = db_users.get_user_id(username)
    for entry in id_data:
        return entry.user_id
    return

# Sort numbers, add to list
def sort_numbers(data, data_list):
    for entry in natsorted(data, key=itemgetter(1), reverse=False):
        data_list.append(entry)
    return
# Remove too many spaces
def remove_whitespaces(s):
    new_s = re.sub(r"\s\s+", " ", s)
    return new_s

# Check if string contains only numbers
def isFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

 # Remove duplicates from list
def remove_duplicates(mylist):
    seen = set()
    seen_add = seen.add
    return [r_id for r_id in mylist if not (r_id in seen or seen_add(r_id))]

    