from flask import render_template, request
from flask import redirect
from flask import url_for
from flask_login import login_user, login_required, logout_user, current_user
import random 
from . import db
from functools import wraps
from .models import RegularUser, Hospital, Vaccine, UserVaccineInfo, VaccineRequest, NationalSystem,HospitalVaccineStock


@hospitals.route('/request-approval', methods=['POST', 'GET'])  
def request_approval():
    if request.method == 'POST':
        data = request.form
        hospital = Hospital.query.filter_by(hospital_id=current_user.hospital_id)
        hospital.status = "Requested"
        db.session.commit()
        return render_template('request-approval.html')
    return render_template('request-approval.html')

@hospitals.route('/update-users', methods=['POST', 'GET'])  
def update_users():
    if request.method == 'POST':
        data = request.form
        vaccine_serial = data['vaccine_serial']
        if data['updated_status'] == 'Vaccinated':
            #* Hospital request status update
            user = UserVaccineInfo.query.filter_by(vaccine_serial=vaccine_serial)
            user.vaccine_status = "Vaccinated"
            db.session.commit()
        
    hospital_vaccine_users = UserVaccineInfo.query.filter_by(hospital_id=current_user.hospital_id)
    users = hospital_vaccine_users
    
    return render_template('update-users-vaccine.html', users=users)


@hospitals.route('/request-vaccine', methods=['POST', 'GET'])
def request_vaccine():
    if request.method == 'POST':
        data = request.form 
        vaccine_name = data['vaccine_name']
        vaccine_amount = data['vaccine_amount']
        hospital_id = current_user.hospital_id
        hospital = Hospital.query.filter_by(hospital_id=hospital_id)
        vaccine = Vaccine.query.filter_by(vaccine_name=vaccine_name)

        new_vaccine_request = VaccineRequest(vaccine_name = vaccine_name,
                                             vaccine_id=vaccine.vaccine_serial, 
                                             request_amount=vaccine_amount)
                                             
        db.session.add(new_vaccine_request)
        db.session.commit()
        return redirect(url_for('hospitals.request_vaccine'))
    vaccine_names = Vaccine.query
    own_requests = VaccineRequest.query.filter_by(hospital_id=current_user.hospital_id)
    
    return render_template('request-vaccine.html', vaccine_names=vaccine_names, own_requests=own_requests)

@hospitals.route('/hospital-vaccine-stock', methods=['POST', 'GET'])
def hospital_vaccine_stock():
    hospital_id = current_user.hospital_id
    hospital_stock = HospitalVaccineStock.query.filter_by(hospital_id=hospital_id)
    return render_template('hospital-vaccine-stock.html', hospital_stock=hospital_stock)