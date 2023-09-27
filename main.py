from flask import Flask, render_template, request, jsonify, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Set your Google Sheets credentials file and spreadsheet ID
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('D:\zabuza\pythonProject\data\secreatekey.json', scope)
gc = gspread.authorize(credentials)

# Open the Google Sheet by title
spreadsheet = gc.open('student')
worksheet = spreadsheet.get_worksheet(0)  # Adjust the index as needed

# Function to fetch data from Google Sheets
@app.route('/', methods=['GET', 'POST'])
def index():
    unique_list = []
    for cell in worksheet.range('C2:C140'):
         if cell.value not in unique_list and cell.value != '-' and cell.value != '':
             unique_list.append(cell.value)

    unique_set =set()
    for cell in worksheet.range('C2:C140'):
        unique_set.add(cell.value)

    unique_dict ={index: element for index, element in enumerate(unique_set)}
    print(unique_dict)

    if request.method == 'POST':
        project_name = request.form.get('project_name')
        return redirect(url_for('project_details', project_name=project_name))
    length= len(unique_set)

    data = worksheet.get_all_records()
    return render_template('index.html',length=length, unique_dict=unique_dict,project_details=data)


@app.route('/project_details/<project_name>')
def project_details(project_name):
    data = worksheet.get_all_records()
    project_details = [project for project in data if project['Project Name'] == project_name]
    i=0
    j=0
    k=0
    if not project_details:
        return "Project not found"
    for project in project_details:
        if project['Status']== 'Completed':
            k=k+1
        elif project['Status']== 'Ongoing':
            j=j+1
        else:
            i=i+1
    score=[i,j,k]
    return render_template('project_details.html',score=score, project_name=project_name, project_details=project_details)


if __name__ == '__main__':
    app.run(debug=True)
