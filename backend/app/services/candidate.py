from models.user import User
from models.candidate import Candidate
from models.job_application import JobApplication
from models.job_post import JobPost
from models.employer import Employer
from extensions import db
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask import request

class CandidateService:
	@staticmethod
	@jwt_required()
	def update_profile():
		try:
			# Verify jwt token

			if not get_jwt_identity():
				return {'error': 'Unauthorized'}, 401

			# Get user email from jwt token
			user_email = get_jwt_identity()

			user = User.query.filter_by(email=user_email).first()
			candidate = Candidate.query.filter_by(id=user.id).first()

			# Check if user type is candidate
			if user.type != 'candidate':
				return {'error': 'Unauthorized'}, 401
			
			user.first_name = request.json['first_name']
			user.last_name = request.json['last_name']
			candidate.work_experience = request.json['work_experience']
			candidate.education = request.json['education']
			candidate.certifications = request.json['certifications']
			candidate.resume_url = request.json['resume_url']
			candidate.linkedin_url = request.json['linkedin_url']
			candidate.github_url = request.json['github_url']
			# Add skills
			skills = request.json['skills']
			for skill in skills:
				candidate.skills.append(skill)

			db.session.commit()
			return {'message': 'Profile updated successfully'}, 200
		except Exception as e:
			return {'error': str(e)}, 500
		
	@staticmethod
	@jwt_required()
	def get_profile(id):
		try:
			# Verify jwt token
			if not get_jwt_identity():
				return {'error': 'Unauthorized'}, 401

			user = User.query.filter_by(id=id).first()
			# Check if user type is candidate
			if user.type != 'candidate':
				return {'error': 'Unauthorized'}, 401
			candidate = Candidate.query.filter_by(id=id).first()
			if not candidate:
				return {'error': 'Candidate not found'}, 404
			return candidate.serialize(), 200
		except Exception as e:
			return {'error': str(e)}, 500


	@staticmethod
	@jwt_required()
	def get_potential_employer(id):
		try:
			# Verify jwt token
			if not get_jwt_identity():
				return {'error': 'Unauthorized'}, 401
			user = User.query.filter_by(id=id).first()
			# Check if user type is candidate
			if user.type != 'candidate':
				return {'error': 'Unauthorized'}, 401
			candidate = Candidate.query.filter_by(id=id).first()
			if not candidate:
				return {'error': 'Candidate not found'}, 404
			job_applications = JobApplication.query.filter_by(candidate_id=candidate.id)
			employer_list=[]
			for job_application in job_applications:
				job_posts = JobPost.query.filter_by(id = job_application.job_post_id)
				for job_post in job_posts:
					employer = Employer.query.filter_by(id = job_post.employer_id).first()
					employer_list.append(employer.serialize())
			return employer_list,200
		except Exception as e:
			return {'error': str(e)}, 500
