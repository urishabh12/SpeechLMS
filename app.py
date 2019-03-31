import os
import sys
from flask import Flask, send_from_directory, render_template, request, redirect, url_for
import sqlite3
from werkzeug.utils import secure_filename
import PyPDF2

UPLOAD_FOLDER = '/home/xtro/speechlms/pdf'
ALLOWED_EXTENSIONS = set(['pdf'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/student/<string:branch>/<string:semester>')
def student(branch, semester):
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    subjects = []
    news = []
    for row in c.execute('select sem%s from %s' %(semester, branch)):
        if row[0] is not None:
            subjects.append(row[0])
    for row in c.execute('select topic from news'):
        if row[0] is not None:
            news.append(row[0])
    return render_template('student.html', subjects = subjects, news = news)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    if request.method == 'POST':
        username = request.form['username']
        c.execute('delete from people where username=?',(username,))
        conn.commit()
        return redirect(url_for('admin'))
    student = []
    teacher = []
    for row in c.execute('select * from people'):
        if row[2] == 'student':
            student.append(row)
        elif row[2] == 'teacher':
            teacher.append(row)
    return render_template('admin.html', student=student, teacher=teacher)

@app.route('/teacher/<string:branch>')
def teacher(branch):
    return render_template('teacher.html', branch=branch)

@app.route('/course/<string:branch>')
def course(branch):
    return render_template('branch.html', branch=branch)

@app.route('/tsubjects/<string:branch>/<string:semester>')
def tsubjects(branch, semester):
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    sub = []
    for row in c.execute('select %s from %s' %(semester, branch)):
        if row[0] is not None:
            sub.append(row[0])
    return render_template('tsubjects.html', subject=sub, branch=branch)

@app.route('/delpdf/<string:name>/<string:subject>')
def delpdf(name, subject):
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    c.execute("delete from %s where name = ?" %subject, (name,))
    conn.commit()
    return redirect(url_for('addres', subject=subject))

@app.route('/addres/<string:subject>', methods=['GET', 'POST'])
def addres(subject):
    print('Head', file=sys.stdout)
    conn = sqlite3.connect("Database.db")
    c = conn.cursor()
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        name = request.form.get('name')
        chapter = request.form.get('chapter')
        addr = file.filename
        data = (name, addr, chapter)
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            c.execute(' insert into %s values(?,?,?)' %subject, data)
            conn.commit()
            return redirect(url_for('addres',
                                    message="Uploaded", subject=subject))
    data = []
    for row in c.execute('select name, addr from %s' %subject):
        data.append(row)
    return render_template('addres.html', data=data, subject=subject)

@app.route('/news', methods=['GET', 'POST'])
def news():
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    if request.method == 'POST':
        news = request.form.get('news')
        c.execute('insert into news values (?)', (news, ))
        conn.commit()
        cnews = []
        for row in c.execute('select * from news'):
            cnews.append(row[0])
        return render_template('news.html', addmessage = "News Submitted", news=cnews)
    cnews = []
    for row in c.execute('select * from news'):
        cnews.append(row[0])
    return render_template('news.html', news=cnews)

@app.route('/rmacc', methods=['GET', 'POST'])
def rmacc(username):
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    c.execute('delete from people where username=?',(username,))
    conn.commit()
    return redirect(url_for('admin'))

@app.route('/delnews/<string:news>')
def delnews(news, branch):
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    c.execute("delete from news where topic = ?" , (news,))
    conn.commit()
    return redirect(url_for('news', branch=branch))

@app.route("/subjects/<string:subject>/<int:chapter>")
def subjects(subject, chapter):
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    data = []
    say = []
    for row in c.execute('select name, addr from %s where chapter = ?' %subject, (chapter,)):
        data.append(row)
        say.append(row[0])
    return render_template('subject.html', data=data, say=say)

@app.route('/feedback')
def feedback():
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    f = []
    for row in c.execute('select * from feedbacknew'):
        f.append(row[0])
    return render_template('feedback.html', f = f)

@app.route('/chapter/<string:subject>')
def chapter(subject):
    conn = sqlite3.connect('Database.db')
    c = conn.cursor()
    chapters = []
    for row in c.execute('select chapter from %s' %subject):
        chapters.append(row[0])
    return render_template('chapter.html', subject=subject, chapters = chapters)

@app.route("/pdf/<path:path>", methods=['GET', 'POST'])
def pdf(path):
    if request.method == "POST":
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        f = request.form.get('feedback')
        c.execute('insert into feedbacknew values(?)',(f,))
        conn.commit()
        return redirect(url_for(pdf, path=path))
    pdfFileObj = open('./pdf/%s' %path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    n = pdfReader.numPages
    text = ""
    for i in range(n):
        text = text + (pdfReader.getPage(i).extractText())
    pdfFileObj.close()
    return render_template('pdf.html', text=text)

@app.route("/js/<path:path>")
def js(path):
    return send_from_directory('js', path)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        username = request.form.get("username")
        password = request.form.get("password")
        u = 0
        for row in c.execute('select username from PEOPLE'):
            if row[0] == username:
                u = 1
                break
        if u == 1:
            ur = (username,)
            c.execute('select password from PEOPLE where username = ?', ur)
            pa = c.fetchone()
            if password == pa[0]:
                c.execute('select type from PEOPLE where username =?', ur)
                ty = c.fetchone()
                if ty[0] == 'student':
                    c.execute('select branch from people where username = ?', ur)
                    bra = c.fetchone()
                    c.execute('select semester from people where username = ?', ur)
                    sem = c.fetchone()
                    return redirect(url_for('student',branch=bra[0], semester=sem[0]))
                elif ty[0] == 'admin':
                    return redirect(url_for('admin'))
                else:
                    c.execute('select branch from people where username = ?', ur)
                    bra = c.fetchone()
                    return redirect(url_for('teacher', branch=bra[0]))
            else:
                return render_template('login.html', message="Wrong username or password")
        else:
            return render_template('login.html', message="Wrong username or password")
    return render_template('login.html', message="")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        u = request.form.get('username')
        p = request.form.get('password')
        t = request.form.get('type')
        b = request.form.get('branch')
        s = request.form.get('semester')
        s = str(s)
        data = (u,p,t,b,s)
        c.execute('INSERT INTO PEOPLE VALUES (?,?,?,?,?)', data)
        conn.commit()
        return render_template('register.html', message = "Successfully Registered")
    return render_template('register.html')

@app.route('/change', methods=['GET', 'POST'])
def change():
    if request.method == 'POST':
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        username = request.form['username']
        password = request.form['password']
        l = []
        for row in c.execute('select * from people where username=?',(username,)):
            l.append(row)
        if l == []:
            return redirect(url_for('change', message=['No such username']))
        c.execute('update people set password=? where username=?',(password,),(username,))
        conn.commit()
        return redirect(url_for('change', message=['Password Changed']))
    return render_template('change.html', message=[])

@app.route('/css/<path:path>')
def css(path):
    return send_from_directory('css', path)

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

app.run()