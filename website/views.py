from flask import render_template, request
from flask import redirect
from flask import url_for
from flask_login import login_user, login_required, logout_user, current_user
import random 
from . import db
from functools import wraps
from .models import RegularUser, Hospital, Vaccine, UserVaccineInfo, VaccineRequest, NationalSystem,HospitalVaccineStock
from flask_mail import Mail, Message





def hospital_required(func):
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.email.split('@')[1] == 'hospital.com':
                return func(*args, **kwargs)
            else:
                return redirect(url_for('views.dashboard'))
        else:
            return redirect(url_for('auth.login'))
    return wrapper


@views.route('/')
# @login_required
def index():
    return render_template('index.html')
    # return redirect(url_for('views.submit'))

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@views.route('/home', methods=['GET', 'POST'])  
@login_required
def home():
    return render_template('home.html')

@views.route('/demo')
def demo():
    return render_template("demo.html")

@views.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        data = request.form
        string = data['textarea']
        formatted_string_list = string.split('\r\n')
        list_with_index = list(enumerate(formatted_string_list))
        winner = random.choice(list_with_index)
        return render_template("demo.html", list_with_index=list_with_index, winner=winner)
 
    return render_template("submitname.html")

@views.route('/winner', methods=['POST', 'GET'])
def winner():

    return render_template("winner.html")

@views.route('/vaccineregistration', methods=['POST', 'GET'])
def vaccineregistration():
    if request.method == 'POST':
        data = request.form
        name = data['first_name'] 
        nid = data['nid_number']
        nid = RegularUser.query.filter_by(nid=nid).first()
        vaccine_name = data['vaccine_for']
        hospital_id = data['hospital_id']
        new_vaccine = UserVaccineInfo(
                                    user_id  = nid, 
                                    vaccine_id = Vaccine.query.filter_by(vaccine_name=vaccine_name).first().vaccine_serial,
                                    hospital_id = hospital_id,
                                    user_name = name
                                    )
        
        db.session.add(new_vaccine)
        db.session.commit()
        return redirect(url_for('views.vaccineregistration'))
    
    hospitals = Hospital.query.all()
    vaccines = Vaccine.query.all()
    context = {'hospitals': hospitals,
                'vaccines': vaccines}
            
    return render_template("vaccine-registration.html", context=context) 


@views.route('/download-vaccine-card', methods=['POST', 'GET'])
def download_vaccine_card():
    nid = current_user.nid
    user_vaccine_info = UserVaccineInfo.query.filter_by(user_id=nid).first()
    name = user_vaccine_info.user_name
    vaccine_name = user_vaccine_info.vaccine_name
    hospital_id = user_vaccine_info.hospital_id
    hospital_name = Hospital.query.filter_by(hospital_id=hospital_id).first().name
    status = user_vaccine_info.vaccine_status
    date = user_vaccine_info.vaccine_date
    context = {'name': name,
                'vaccine_name': vaccine_name,
                'hospital_name': hospital_name,
                'status': status, 
                'nid': nid, 
                'date': date}

    return render_template("download-vaccine-card.html", context=context)

@views.route('/make-payment', methods=['POST', 'GET'])
def make_payment():
    if request.method == 'POST':
        data = request.form 
        amount = data['payamt']
        current_user.balance = current_user.balance + int(amount)
        db.session.commit()
        return redirect(url_for('views.make_payment'))
    return render_template("make-payment.html")