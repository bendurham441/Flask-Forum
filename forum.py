from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3

app = Flask(__name__)

# TODO: user context manager

conn = sqlite3.connect('forum.db')
curs = conn.cursor()
app.config['SECRET_KEY'] = '\xe1\x03\xf1p}2\xdd\xd1\xeeP\x03e\xe9\xd0\xfbKD8J\xeeIj\x1fw'

def post(title, text):
    if session.logged_in == True:
        curs.execute('''insert into posts (title, text) values 
                ("{}", "{}")'''.format(title, text))
        conn.commit()
    else:
        print('You must be logged in to post')

def get_posts(*columns):
    cmd = 'select '
    if columns == ():
        cmd += '*'
    for column in columns:
            cmd += '{},'.format(column)
    print(cmd)
    if cmd[-1] == ',':
        cmd = cmd[:-1]
    cmd += ' from posts;'
    print(cmd)
    curs.execute(cmd)
    return curs.fetchall()

def register_db(username, password):
    cmd = 'select * from users;'
    curs.execute(cmd)
    for user in curs.fetchall():
        print(user)
        if user[1] == username:
            return 'username has already been taken'
    else:
        curs.execute('''insert into users (username, password) values 
            ("{}", "{}");'''.format(username, password))
        conn.commit()
        return 'registered successfully!'

def login_db(username, password):
    cmd = 'select * from users;'
    curs.execute(cmd)
    for user in curs.fetchall():
        if user[1] == username:
            if user[2] == password:
                session['username'] = username
                return 'logged in'
    else:
        return 'username or password is incorrect or nonexistent'

@app.route('/')
def index():
    posts = get_posts()
    print(posts)
    return render_template('index.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return login_db(request.form['username'], request.form['password'])
        # return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return register_db(request.form['username'], request.form['password'])
    return render_template('register.html')

def main():
    try:
        with open('forum_schema.sql', 'r') as schema:
            curs.executescript(schema.read())
            print(schema)
    except:
        print('Table has already been created')
    register_db('name', 'pass')
    post('This is a test title', 'This is some test content')
    print(get_posts())
    
if __name__ == '__main__':
    main()
