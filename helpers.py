from flask import Flask, render_template, redirect, request, url_for, session, flash
from natsort import natsorted
from operator import itemgetter
import re


# Sort numbers, add to list
def sort_numbers(data, data_list):
    for entry in natsorted(data, key=itemgetter(1), reverse=False):
        data_list.append(entry)

# Set username
def username_set_or_none():
    if 'username' in session:
        username = session['username']
    else:
        username = None
    return username

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