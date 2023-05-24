from flask import Flask, render_template, request
from file_cleaner import clean_csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('gui.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['csvFile']
    format = file.filename.split('.')[-1].lower()  # Get the file format or extension

    # Process the file based on the format
    if format == 'csv':
        # Process CSV file
        # ...
        return 'CSV file processed successfully'
    elif format == 'xlsx':
        # Process Excel file
        # ...
        return 'Excel file processed successfully'
    else:
        return 'Unsupported file format'
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
