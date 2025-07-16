


from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required
from app.extensions import db
from app.models.upwork_job import UpworkJob
from app.schemas.upwork_jobs_schema import UpworkJobSchema
from app.enums import UserRoleEnum
from app.utils.role_required import role_required
from app.utils.gemini import assess_job_feasibility,generate_dummy_upwork_jobs
from datetime import datetime
import json

upwork_job_bp = Blueprint('upwork_job', __name__, url_prefix='/upwork-jobs')

upwork_jobs_schema = UpworkJobSchema(session=db.session)
upwork_jobs_list_schema = UpworkJobSchema(many=True)

@upwork_job_bp.route('/create', methods=['GET', 'POST'])
@login_required
@role_required(UserRoleEnum.admin, UserRoleEnum.team_lead, UserRoleEnum.salesman)
def create_upwork_job():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        # Convert comma-separated strings to list/JSON
        data['skills'] = json.dumps([s.strip() for s in data.get('skills', '').split(',') if s.strip()])
        data['tags'] = json.dumps([t.strip() for t in data.get('tags', '').split(',') if t.strip()])

        if data.get('posted_at'):
            try:
                data['posted_at'] = datetime.fromisoformat(data['posted_at'])
            except ValueError:
                flash("Invalid date format for posted_at. Use ISO format.", "danger")
                return render_template("dashboard/upwork_job_create.html", form=data)

        errors = upwork_jobs_schema.validate(data)
        if errors:
            flash("Validation failed. Please check your input.", "danger")
            return render_template("dashboard/upwork_job_create.html", errors=errors, form=data)

        if UpworkJob.query.filter_by(job_id=data.get("job_id")).first():
            flash(f"Job ID '{data['job_id']}' already exists.", "warning")
            return render_template("dashboard/upwork_job_create.html", form=data)

        try:
            data['feasibility_status'] = assess_job_feasibility(data)
            upwork_job = upwork_jobs_schema.load(data)
            db.session.add(upwork_job)
            db.session.commit()
            flash("Upwork job created successfully.", "success")
            return redirect(url_for('upwork_job.list_upwork_jobs'))

        except Exception as e:
            db.session.rollback()
            flash(f"Internal error: {str(e)}", "danger")
            return render_template("dashboard/upwork_job_create.html", form=data)

    return render_template("dashboard/upwork_job_create.html")



@upwork_job_bp.route('/list', methods=['GET'])
@login_required
@role_required(UserRoleEnum.admin, UserRoleEnum.team_lead, UserRoleEnum.salesman)
def list_upwork_jobs():
    jobs = UpworkJob.query.order_by(UpworkJob.created_at.desc()).all()
    return render_template("dashboard/upwork_jobs.html", jobs=jobs)



@upwork_job_bp.route('/generate-dummy-jobs', methods=['POST'])
def generate_dummy_jobs():
    try:
        # Call Gemini utility to generate 10 dummy jobs
        jobs = generate_dummy_upwork_jobs()

        return jsonify({
            "message": "10 dummy jobs generated successfully.",
            "jobs": jobs
        }), 200

    except Exception as e:
        return jsonify({
            "error": f"Failed to generate dummy jobs: {str(e)}"
        }), 500
    




@upwork_job_bp.route('/bulk-create', methods=['POST'])
@login_required
@role_required(UserRoleEnum.admin, UserRoleEnum.team_lead, UserRoleEnum.salesman)
def bulk_create_upwork_jobs():
    jobs_data = generate_dummy_upwork_jobs()

    if not isinstance(jobs_data, list):
        return jsonify({"error": "Expected a list of jobs"}), 400

    created_jobs = []
    skipped_jobs = []
    errors = []

    for idx, job_data in enumerate(jobs_data):
        try:
            # Step 1: Basic validation
            validation_errors = upwork_jobs_schema.validate(job_data)
            if validation_errors:
                errors.append({
                    "job_index": idx,
                    "job_id": job_data.get("job_id"),
                    "error": validation_errors
                })
                continue

            # Step 2: Check for duplicates
            if UpworkJob.query.filter_by(job_id=job_data.get("job_id")).first():
                skipped_jobs.append(job_data.get("job_id"))
                continue

            # Step 3: AI feasibility assessment
            job_data['feasibility_status'] = assess_job_feasibility(job_data)

            # Step 4: Deserialize and add to session
            upwork_job = upwork_jobs_schema.load(job_data)
            db.session.add(upwork_job)
            created_jobs.append(upwork_job)

        except Exception as e:
            errors.append({
                "job_index": idx,
                "job_id": job_data.get("job_id"),
                "error": str(e)
            })

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to commit jobs: {str(e)}"}), 500

    return jsonify({
        "message": "Bulk job insert complete.",
        "created": [upwork_jobs_schema.dump(job) for job in created_jobs],
        "skipped_existing_job_ids": skipped_jobs,
        "errors": errors
    }), 207  # 207 Multi-Status: Some succeeded, some failed


@upwork_job_bp.route('/<int:job_id>', methods=['GET'])
@login_required
def get_upwork_job(job_id):
    job = UpworkJob.query.get(job_id)
    if not job:
        return jsonify({"error": f"No job found with ID {job_id}"}), 404

    return jsonify({
        "job": upwork_jobs_schema.dump(job)
    }), 200