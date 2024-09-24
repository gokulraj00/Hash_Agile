from flask import Flask, request, render_template, send_from_directory
import PyPDF2
import docx2txt
import os
from pymongo import MongoClient
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# MongoDB setup
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['resume_database']
resumes_collection = db['resumes']

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def extract_text_from_pdf(pdf_path):
    text = ''
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    return text

def extract_text_from_docx(docx_path):
    return docx2txt.process(docx_path)

def extract_resume_data(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    return ''

def extract_info_from_text(text):
    # Enhanced regex for email extraction
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    name = "Not found"
    college = "Not found"
    skills = "Not found"
    email = "Not found"

    # Extract email
    email_match = re.search(email_regex, text)
    if email_match:
        email = email_match.group(0)

    # Example extraction for name, college, and skills (You can improve this using regex or NLP)
    lines = text.split('\n')
    for line in lines:
        if 'name' in line.lower():
            name = line.split(":")[1].strip() if ':' in line else line.strip()
        elif 'college' in line.lower():
            college = line.split(":")[1].strip() if ':' in line else line.strip()
        elif 'skills' in line.lower():
            skills = line.split(":")[1].strip() if ':' in line else line.strip()

    return {
        'Name': name,
        'College': college,
        'Skills': skills,
        'Email': email
    }

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    extracted_resumes = list(resumes_collection.find({}, {'_id': 0}))  # Fetch existing resumes from MongoDB
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        
        files = request.files.getlist('file')
        for file in files:
            if file.filename == '':
                return 'No selected file'

            if file and (file.filename.endswith('.pdf') or file.filename.endswith('.docx')):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)

                # Extract text and data from the file
                text = extract_resume_data(file_path)
                info = extract_info_from_text(text)

                # Extract the filename without the extension
                filename_without_extension = file.filename.rsplit('.', 1)[0]

                # Save to MongoDB
                resumes_collection.insert_one({
                    'Filename': filename_without_extension,  # Store without extension
                    'Name': info['Name'],
                    'College': info['College'],
                    'Skills': info['Skills'],
                    'Email': info['Email']
                })

                info['Filename'] = filename_without_extension
                extracted_resumes.append(info)

        return render_template('upload.html', resumes=extracted_resumes)

    return render_template('upload.html', resumes=extracted_resumes)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename + '.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
