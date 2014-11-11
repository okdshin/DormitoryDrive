import os
import hashlib
import subprocess
import flask
import werkzeug
from flask.ext.sqlalchemy import SQLAlchemy
import sqlalchemy
FOOTER = 'DomitoryDrive is presented by Netkai (WirelessiaLiberation)'
FILE_LIST_MAX_NUM = 10
app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    filename = db.Column(db.String(80), unique=False)
    filetype = db.Column(db.String(20), unique=False)

    def __init__(self, filename, id):
        self.filename = filename
        self.id = id
        if filename.split('.')[-1] in ['ogv', 'flv', 'mp4', 'avi', 'mpeg']:
            command = [ 'ffmpeg', '-y',
                        '-i', 
                        os.path.join(
                            app.static_folder,
                            app.config['UPLOAD_FOLDER'], 
                            id
                        ),
                        '-codec:v', 'libtheora',
                        '-qscale:v', '5',
                        '-codec:a', 'libvorbis',
                        '-qscale:a', '5', 
                        os.path.join(
                            app.static_folder,
                            app.config['UPLOAD_FOLDER'], 
                            id+'.ogv'
                        )
                    ]
            child = subprocess.Popen(command)#, stdout = subprocess.PIPE)
            #child.wait()
            self.filetype = 'video'
        elif filename.split('.')[-1] in ['jpg', 'png', 'bmp']:
            self.filetype = 'image'
        else:
            self.filetype = 'unknown'

    def __repr__(self):
        return '<File {fn}, {i}, {ft}'.format(
                fn=self.filename, i=self.id, ft=self.filetype)

@app.route('/', methods=['GET', 'POST'])
def index():
    page = int(flask.request.args.get('page','0'))
    if flask.request.method == 'POST':
        keyword = flask.request.form['keyword']
        files = File.query.filter(
                    File.filename.like('%{k}%'.format(k=keyword))
                ).order_by(
                    File.filename
                ).slice(page*FILE_LIST_MAX_NUM, (page+1)*FILE_LIST_MAX_NUM)
    else:
        files = File.query.order_by(File.filename).slice(
                page*FILE_LIST_MAX_NUM, (page+1)*FILE_LIST_MAX_NUM)
    return flask.render_template('file_list.html', files=files, footer=FOOTER)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if flask.request.method == 'POST':
        file = flask.request.files['file']
        if file:
            secured_filename = werkzeug.secure_filename(file.filename)
            id = hashlib.sha256(file.stream.read()).hexdigest()
            file.stream.seek(0)
            file.save(os.path.join(app.static_folder, 
                app.config['UPLOAD_FOLDER'], id))
            if db.session.query(sqlalchemy.sql.exists().where(File.id==id)).scalar():
                return 'same file has already existed'
            db.session.add(File(secured_filename, id))
            db.session.commit()
            return flask.redirect(flask.url_for('uploaded_file', id=id))
    return flask.render_template('upload.html')

@app.route('/uploads/<id>')
def uploaded_file(id):
    fileurl = flask.url_for('static', 
        filename=os.path.join(app.config['UPLOAD_FOLDER'], id))
    file = File.query.filter(File.id==id).first()
    return flask.render_template('view.html', 
        id=id, furl=fileurl, filename=file.filename, 
        filetype=file.filetype, footer=FOOTER)

if __name__ == '__main__':
    app.run(debug=True)
