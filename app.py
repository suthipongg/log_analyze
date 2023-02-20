from flask import Flask, flash, request, redirect, render_template
import os
from werkzeug.utils import secure_filename
from pathlib import Path
from main import main_log

# set download path to "static" directory
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # root directory
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))
app = Flask(__name__)
UPLOAD_FOLDER = ROOT / 'static'
if UPLOAD_FOLDER.name not in os.listdir(ROOT):
    os.makedirs(UPLOAD_FOLDER)

# config mak file size
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024

# define file extension
ALLOWED_EXTENSIONS = set(['bin'])
# select model
model_path = Path(__file__).resolve().parent / "models"
model_ls = os.listdir(model_path)
data = []
for model in model_ls:
    model_name = os.path.splitext(model)[0]
    if model_name == "STD":
        data.insert(0, {'name':model_name})
    else:
        data.append({'name':model_name})
        

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template(
        'index.html',
        data=data)


@app.route('/', methods=['POST'])
def upload():
    # get file and model
    file = request.files.getlist("file")
    model_select = request.form.get('comp_select')
    for n, model in enumerate(data):
        if model['name'] == model_select:
            data.pop(n)
            data.insert(0, {'name':model_select})
            break
    # check if there is a file
    if file == []:
        flash('No image selected for uploading')
        return redirect(request.url)
    
    have_file = 0
    for f in file:
        # check file type
        if f and allowed_file(f.filename):
            have_file = 1
            filename = secure_filename(f.filename)
            f.save(app.config['UPLOAD_FOLDER'] / filename)
        # print file type not is "bin"
        else:
            flash(f.filename + 'types not is - bin')
    # call function log analyze
    result = main_log(app.config['UPLOAD_FOLDER'], model=model_select)
    list_dir = os.listdir(app.config['UPLOAD_FOLDER'])
    for file in list_dir:
        os.remove(app.config['UPLOAD_FOLDER'] / file) 
    # check if their is bin file
    if have_file:
        return render_template('index.html', tables=[result.to_html(classes='data', header="true")], data=data)
    else:
        return redirect(request.url)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=False)