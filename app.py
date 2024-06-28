from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import os
import secrets 

sec_key = secrets.token_hex(16)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = f'{sec_key}'
os.makedirs(app.config['UPLOAD_FOLDER'],exist_ok=True)

@app.route('/', methods = ['GET','POST'])
def index():
    
    if request.method == 'POST':
        ''' To handle all kind of errors '''
        if 'file' not in request.files:
            flash('Oops no file', 'error')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file and pdf_files(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            file_details = {
                'filename' : file.filename,
                'size' : os.path.getsize(filepath),
                'type' : file.content_type
            }
            return render_template('index.html', file_details = file_details)
        else:
            flash('Uh Oh! Only PDF Files can be uplaoded mate!!', 'error')
            return redirect(request.url)
    return render_template('index.html')


def pdf_files(filename):
    ''' To extract the pdf file name '''
    return '.' in filename and filename.rsplit('.',1)[1].lower() == 'pdf'

@app.route('/toggle-mode', methods=['POST'])
def toggle_mode():
    if 'dark_mode' not in session:
        session['dark_mode'] = False
    session['dark_mode'] = not session['dark_mode']
    return jsonify({'success': True, 'dark_mode': session['dark_mode']})


@app.context_processor
def inject_dark_mode():
    return dict(dark_mode=session.get('dark_mode', False))

if __name__ == '__main__':
    app.run(debug=True, port = 0)