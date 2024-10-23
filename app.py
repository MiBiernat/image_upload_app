from flask import Flask, request, redirect, url_for, render_template, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'some_secret_key'  # Potrzebne do wyświetlania komunikatów flash

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Sprawdź czy w żądaniu są pliki
        if 'files[]' not in request.files:
            message = 'Nie wybrano plików.'
            return render_template('upload.html', message=message)
        files = request.files.getlist('files[]')
        if not files or files[0].filename == '':
            message = 'Nie wybrano plików.'
            return render_template('upload.html', message=message)
        
        saved_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                saved_files.append(filename)
        
        if saved_files:
            return render_template('upload_success.html', filenames=saved_files)
        else:
            message = 'Żadne pliki nie zostały przesłane. Sprawdź, czy wybrane pliki są w odpowiednim formacie.'
            return render_template('upload.html', message=message)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
