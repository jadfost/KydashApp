from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file and file.filename.endswith('.xlsx'):
        df = pd.read_excel(file)
        return render_template('tabla.html', tables=[df.to_html(classes='data', header="true")])

    return 'Invalid file format'

if __name__ == '__main__':
    app.run(debug=True)
