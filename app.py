from flask import Flask, flash, request, redirect, url_for, render_template
import os
from werkzeug.utils import secure_filename
from pathlib import Path
from main import main_log


FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # root directory
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))

app = Flask(__name__)
UPLOAD_FOLDER = ROOT / 'static'

if UPLOAD_FOLDER.name not in os.listdir(ROOT):
    os.makedirs(UPLOAD_FOLDER)

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['bin'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload():
    file = request.files.getlist("file")
    if file == []:
        flash('No image selected for uploading')
        return redirect(request.url)
    have_file = 0
    for f in file:
        if f and allowed_file(f.filename):
            have_file = 1
            filename = secure_filename(f.filename)
            f.save(app.config['UPLOAD_FOLDER'] / filename)

        else:
            flash(f.filename + 'types not is - bin')
    result = main_log(app.config['UPLOAD_FOLDER'], model="STD")
    list_dir = os.listdir(app.config['UPLOAD_FOLDER'])
    for file in list_dir:
        os.remove(app.config['UPLOAD_FOLDER'] / file) 
        
    if have_file:
        return render_template('index.html', tables=[result.to_html(classes='data', header="true")])
    else:
        return redirect(request.url)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=False)