"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, request, render_template, jsonify

from FlaskWebProject import app
from FlaskWebProject.email_service import EmailService
from FlaskWebProject.email_senders import MailgunSender, MandrillSender

def send_email(message_data):
    # Use dependency injection to set senders for the service to call
    service = EmailService([MandrillSender(), MailgunSender()])
    # send email
    return service.send(message_data)

"""
Basic service exposed on website
"""

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/', methods=['POST'])
@app.route('/home', methods=['POST'])
def send():
    ret = send_email(request.form)
    return render_template('index.html', message = ret.message)


"""
RESTful APIs
"""

sample_json_input = {
    'from_email':'test_from@testmail.com',
    'to_email':['test_to1@testmail.com,test_to2@testmail.com'],
    'cc_email':'test_cc@testmail.com',
    'bcc_email':['test_bcc1@testmail.com', 'test_bcc2@testmail.com'],
    'subject':'test subject',
    'content':'test content'
}

sample_json_output = {
    'status_code': 200,
    'status': 'OK',
    'mesage': 'Email sent successfully'
}

@app.route('/api/sendmail', methods=['GET'])
def help():
    """
    Return a help message as a welcome to the service
    """
    return jsonify(
        {'status_code': 200,
         'status': 'OK',
         'Mesage': 'Welcome to our basic mail service. Please use POST method to send email with json input. Output is also in json format which contains HTTP status codes to indicate result status of the request.',
         'sample_json_input':sample_json_input,
         'sample_json_output': sample_json_output})

@app.route('/api/sendmail', methods=['POST'])
def send_mail_rest():
    """
    Serve a request to our API: take a json in and return back a json out    
    """
    ret = send_email(request.json)
    return jsonify({'status_code': ret.status_code, 'status': ret.status, 'message': ret.message})

if __name__ == '__main__':
    app.run()