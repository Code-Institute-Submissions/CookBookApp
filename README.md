# COOKBOOK APP

A web application that allows users to store and access cooking recipes.

This is a milestone project for Data Centric Development, part of the Full-Stack Web Developer program @ Code Institute.

## Introduction

A web application for storing and accessing cooking recipes.

I created relational database in MS SQL Server. 

Application has a form to allow users to add new recipes to the site and edit them. 

They can search for recipes using title keywords, type ot ingredient. 

There is also basic registration and authentication. 


This Project is deployed [here](https://cookbookappproject.herokuapp.com/)

Source code is availible on [GitHub](https://github.com/tjasajan/CookBookApp)

## Build with

+ [Python](https://www.python.org/)
+ [Flask Framework](http://flask.pocoo.org/)

## Other technologies used

+ Visual Studio Code editor
+ Virtual environment
+ MS SQL
+ Pylint
+ pip
+ pyodbc
+ WTForms
+ HTML5, CSS3
+ Chrome DevTools

## Database diagram
![Diagram](https://github.com/tjasajan/CookBookApp/blob/master/DB/DB-Diagram.png?raw=true)

## Installation

1. Download files
2. Install [Python](https://www.python.org/downloads/)
3. Install Flask and other requirements
~~~~
pip install -r requirements.txt
~~~~
5. Run application
~~~~
python app.py
~~~~


## Testing

Testing was done manually throughout development process and with help of a print() function for each new functionality. 

Testing for responsive layout was done in Chrome and also on different devices.  

## Deployment

Output installed packages for dependency management:
~~~~
pip freeze --local > requirements.txt
~~~~

Create Procfile needed for Heroku deployment:
~~~~
echo web: python app.py
~~~~

Add to Heroku app repository:
~~~~
heroku git:remote -a cookbookappproject
~~~~

On Heroku platform add buildpack for Python.  
Add custom buildpack for pyodbc: 
~~~~
heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-apt
~~~~

Add aptfile with content:
~~~~
unixodbc
unixodbc-dev
python-pyodbc
libsqliteodbc
~~~~

Configure app:
~~~~
heroku ps:scale web=1
~~~~

On Heroku site add settings for IP (0.0.0.0) and PORT (5000) and restart all dynos.



