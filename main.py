import os
from datetime import datetime

from flask import Flask
from flask import render_template, request, redirect

import boto3

app = Flask(__name__)
app.config.from_pyfile(os.path.join(".", "app.conf"), silent=False)

# serve index page
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/case-studies")
def casestudies():
    return render_template('case-studies.html')

@app.route("/book")
def book():
    return render_template('book.html')

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    email_sent = 0
    if request.method == 'POST':
        default_value = 0
        firstName = request.form.get('firstName', default_value)
        lastName = request.form.get('lastName', default_value)
        email = request.form.get('email', default_value)
        message = request.form.get('message', default_value)

        recipients = ['webmaster@fireconsultancy.co.uk']
        replyto = [email]
        subject = 'Website Enquiry from ' + str(firstName) + ' ' + str(lastName)

        # You can render the message using Jinja2
        html = render_template('email.html', firstName=firstName, lastName=lastName, email=email, message=message)

        send_email(app,
           recipients=recipients,
           replyto=replyto,
           subject=subject,
           html=html
           )

        email_sent = 1

    return render_template('contact.html', email_sent=email_sent)

def send_email(app, recipients, replyto, sender=None, subject='', text='', html=''):
    ses = boto3.client(
        'ses',
        region_name=app.config['SES_REGION_NAME'],
        aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
    )
    if not sender:
        sender = app.config['SES_EMAIL_SOURCE']

    ses.send_email(
        Source=sender,
        Destination={'ToAddresses': recipients},
        Message={
            'Subject': {'Data': subject},
            'Body': {
                'Text': {'Data': text},
                'Html': {'Data': html}
            }
        },
        ReplyToAddresses=replyto
    )

@app.route("/privacy")
def privacy():
    return render_template('privacy.html')

@app.route("/ask")
def ask():
    return render_template('ask.html')

@app.route("/aerial-surveys")
def aerial_surveys():
    return render_template('services/aerial-surveys.html')

@app.route("/expert-witness")
def expert_witness():
    return render_template('services/expert-witness.html')

@app.route("/external-wall")
def external_wall():
    return render_template('services/external-wall.html')

@app.route("/fire-engineering")
def fire_engineering():
    return render_template('services/fire-engineering.html')

@app.route("/fire-safety-assessments")
def fire_safety_assessments():
    return render_template('services/fire-safety-assessments.html')

@app.route("/favicon.ico")
def favicon():
    return "200"
    
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8082, debug=True)