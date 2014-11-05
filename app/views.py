from flask import render_template, flash, redirect, request, Flask, url_for, send_from_directory
from app import app 
import urllib2
import json
import csv
import os
import smtplib


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Home')

@app.route('/upload')
def upload():
	return render_template('upload.html', title="Bulk CSV Upload")

@app.route('/validate')
def validate():
	return render_template('validate.html', title="Email Validator")

@app.route('/validatereturn', methods=['POST'])
def validatereturn():
	
	email = request.form['email']

	try:
		url = ("https://api.fullcontact.com/v2/person.json?email={}&apiKey=7081b94d8a62c12e".format(email))
		raw_response = urllib2.urlopen(url).read()
		response = json.loads(raw_response)
		result == "Valid"
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

		for photo in response.get('photos'): 
			if photo.get('isPrimary') == 'True': 
				photourl = photo.get('url')
	except:
		result == "Invalid"

	return render_template('validatereturn.html', photourl=photourl)


@app.route('/message/', methods=['POST'])
def message(): 
	first = request.form['firstname']
	last = request.form['lastname']
	domain = request.form['domain']
	bestemail = 0 
	counter = 0
	profiles=0
	email1 = first+(".")+last+("@")+domain #first.last@domain.com
	email2 = first[0]+last+("@")+domain #f.last@domain.com 
	email3 = first+last+("@")+domain #firstlast@domain.com 
	email4 = first+last[0]+("@")+domain #firstl@domain.com 
	email5 = first+("@")+domain #first@domain.com 
	emails = [email1, email2, email3, email4, email5]

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

						for photo in response.get('photos'): 
							if photo.get('isPrimary') == 'True': 
								photourl = photo.get('url')
					counter = 0 

				except:
					None
	
	return render_template('message.html', firstname=first,lastname=last, bestemail=bestemail, linkedinbio=linkedinbio, linkedinurl=linkedinurl)
