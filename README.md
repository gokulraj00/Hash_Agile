# Resume Uploader & Details Viewer

This project is a web application that allows users to upload their resumes (in PDF format), extract details from the PDF, and view the extracted information. Additionally, it includes a feature to display all previously uploaded resumes and download them as PDF or CSV files.

## Features

- *Resume Upload*: Upload resumes in PDF format, extract key information like name, email, phone, college name, and skills.
- *Details Display*: View all uploaded resumes along with their extracted details.
- *File Download*: Download individual resume details as PDF or CSV.
- *Tab Navigation*: Switch between "Upload Resume" and "Display Details" views using a simple tab navigation.

## Project Structure

bash
├── templates
│   └── index.html          # HTML file for the web interface
├── static
│   └── styles.css          # CSS styling for the web app
├── app.py                  # Flask application to handle routes and logic
└── README.md


## Installation

### Prerequisites

- Python 3.x
- pip

### Steps to Run

#### Clone the Repository

bash
git clone https://github.com/your-username/resume-uploader.git
cd resume-uploader


#### Install Dependencies

Create a virtual environment and install necessary dependencies:

bash
python3 -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt


#### Run the Application

Start the Flask server:

bash
flask run


The app will be available at [http://localhost:5000](http://localhost:5000).

## Backend Setup

You need a backend server running to handle PDF extraction and storing of details with MongoDB as the database. The app assumes you have the following routes:

- POST /generate_details: To process the extracted text from a PDF and return details.
- POST /post_details: To save the extracted details to a MongoDB collection.
- GET /get_details: To fetch a list of previously submitted resumes.

Make sure to modify the MongoDB URI and Flask route handlers in app.py.

## Usage

### Upload a Resume:

1. Navigate to the *Upload Resume* tab.
2. Choose a PDF file containing the resume, and the system will extract details like name, email, phone, etc.
3. The extracted details will be sent to the server for further processing.

### View Uploaded Resumes:

1. Switch to the *Display Details* tab.
2. The system fetches all uploaded resumes and their details from the database.
3. You can download the details as either a PDF or CSV.

## Technologies Used

### Frontend:

- HTML
- CSS

### Backend:

- Flask
- PyPDF2 or PDFMiner (for PDF extraction)
- MongoDB (for data storage)
