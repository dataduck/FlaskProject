import os
import urllib2
import json
import csv
import smtplib
from config import gmailuser, gmailpassword

# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from flask_mail import Mail
from flask.ext.mail import Message, Mail

# Initialize the Flask application
app = Flask(__name__)
mail = Mail(app)
# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['csv','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config.update(
    DEBUG=True,
    #Email Settings
    MAIL_SERVER = 'smtp.gmail.com', 
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = gmailuser,
    MAIL_PASSWORD = gmailpassword
    )
mail = Mail(app)
# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html')

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return redirect(url_for('uploaded_file',
                                filename=filename))

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    currentrow = 0 
    with open('uploads/' + filename, 'rU') as infile: 
        reader = csv.reader(infile)
        for row in reader: 
            currentrow += 1 
            if currentrow == 1: 
                continue 
            first = row[0]
            last = row[1]
            domain = row[2]

            email1 = first+(".")+last+("@")+domain #first.last@domain.com
            email2 = first[0]+last+("@")+domain #f.last@domain.com 
            email3 = first+last+("@")+domain #firstlast@domain.com 
            email4 = first+last[0]+("@")+domain #firstl@domain.com 
            email5 = first+("@")+domain #first@domain.com 
            emails = [email1, email2, email3, email4, email5]

            bestemail = 0
            profiles = 0 
            counter = 0

            with open('output.csv', 'a') as outfile:
                writer = csv.writer(outfile)
                for email in emails:
                    try:
                        url = ("https://api.fullcontact.com/v2/person.json?email={}&apiKey=7081b94d8a62c12e".format(email))
                        raw_response = urllib2.urlopen(url).read()
                        response = json.loads(raw_response)
                        
                        for profile in response.get('socialProfiles'): 
                                counter = counter + 1
                        
                        if counter > profiles: 
                            profiles = counter
                            bestemail = email 
                            givenname = response.get('contactInfo').get('givenName')
                            familyName = response.get('contactInfo').get('familyName')
                            fullname = response.get('contactInfo').get('fullName')

                            for profile in response.get('socialProfiles'): 
                                if profile.get('typeName') == 'LinkedIn': 
                                    linkedinbio = profile.get('bio')
                                    linkedinurl = profile.get('url')
                                if profile.get('typeName') == 'Vimeo': 
                                    vimeourl = profile.get('url')
                                if profile.get('typeName') == 'Twitter': 
                                    twitterurl = profile.get('url')
                                if profile.get('typeName') == 'Facebook': 
                                    facebookurl = profile.get('url')
                        counter = 0 
                    except:
                        None

                newrow = (first, last, domain, bestemail, linkedinbio, linkedinurl, twitterurl)
                            
                writer.writerow(newrow)
              
            msg = Message(subject="Your requested attachment", sender="mcguirea@gmail.com", recipients=["mcguirea@gmail.com"])
            msg.body = 'Check out the attachment in the email and If you have questions, send any questions to mcguirea@gmail.com'
            msg.attach 
            mail.send(msg)
            
    infile.close()
    
    return "File Uploaded & Emailed"  
