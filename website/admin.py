from flask import render_template, request
from flask import redirect
from flask import url_for
from flask_login import login_user, login_required, logout_user, current_user
import random 
from . import db
from functools import wraps
from .models import RegularUser, Hospital, Vaccine, UserVaccineInfo, VaccineRequest, NationalSystem,HospitalVaccineStock


@admin.route('/national-vaccine-stock', methods=['POST', 'GET'])
@require_admin
def national_vaccine_stock():
    if request.method == 'POST':
        data = request.form
        vaccine_name = data['add_vaccine_name']
        add_amount = 0 
        remove_amount = 0
        add_amount = int(data['add_vaccine_amount'])
        remove_amount = int(data['remove_vaccine_amount'])
        vaccine = Vaccine.query.filter_by(vaccine_name=vaccine_name)
        vaccine.vaccine_amount = vaccine.vaccine_amount + add_amount - remove_amount
        db.session.commit()
        return redirect(url_for('admin.national_vaccine_stock'))
    
    
    vaccines = Vaccine.query.all()
    return render_template("national-vaccine-stock.html", vaccines=vaccines)

@admin.route('/add-new-vaccine', methods=['POST', 'GET'])
@require_admin
def add_new_vaccine():
    if request.method == 'POST':
        data = request.form
        new_vaccine = Vaccine(
            vaccine_name = data['new_vaccine_name'],
            vaccine_amount = data['new_vaccine_amount'],
        )
        db.session.add(new_vaccine)
        db.session.commit()
        return redirect(url_for('admin.national_vaccine_stock'))
    return render_template("add-new-vaccine.html")


@admin.route('/permit-hospitals', methods=['POST', 'GET'])
@require_admin
def permit_hospitals():
    if request.method == 'POST':
        data = request.form
        hospital_id = data['hospital_name']
        hospital = Hospital.query.filter_by(hospital_id=hospital_id)
        hospital.status = "Approved"
        db.session.commit()
        return redirect(url_for('admin.permit_hospitals'))
    hospitals = Hospital.query.filter_by(status="Requested").all()
    return render_template("permit-hospitals.html", hospitals=hospitals)

@admin.route('/hospital-requests', methods=['POST', 'GET'])
@require_admin
def hospital_requests():
    if request.method == "POST":
        data = request.form
        hospital_id = data['hospital_name']
        vaccine_amount = data['vaccine_amount']
        vaccine_serial = data['vaccine_name']
        request_id = data['request_id']
        hospital = Hospital.query.filter_by(hospital_id=hospital_id)
        vaccine = Vaccine.query.filter_by(vaccine_serial=vaccine_serial)

        new_hospital_stock = HospitalVaccineStock(
            hospital_id = hospital.hospital_id,
            vaccine_id = vaccine.vaccine_serial,
            vaccine_amount = vaccine_amount)
        db.session.add(new_hospital_stock)
        db.session.commit()
        
        vaccine_request = VaccineRequest.query.filter_by(id=request_id)
        vaccine_request.request_status = "Approved"
        db.session.commit()

        
    hospital_requests = VaccineRequest.query.all()
    return render_template("hospital-requests.html", hospital_requests=hospital_requests)