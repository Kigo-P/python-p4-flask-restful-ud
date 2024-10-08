#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):

    def get(self):
        
        response_dict = {
            "message": "Welcome to the Newsletter RESTful API",
        }
        
        response = make_response(
            response_dict,
            200,
        )

        return response

api.add_resource(Home, '/')

class Newsletters(Resource):

    def get(self):
        
        response_dict_list = [n.to_dict() for n in Newsletter.query.all()]

        response = make_response(
            response_dict_list,
            200,
        )

        return response

    def post(self):
        
        new_record = Newsletter(
            title=request.form['title'],
            body=request.form['body'],
        )

        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()

        response = make_response(
            response_dict,
            201,
        )

        return response

api.add_resource(Newsletters, '/newsletters')

class NewsletterByID(Resource):

    def get(self, id):

        response_dict = Newsletter.query.filter_by(id=id).first().to_dict()

        response = make_response(
            response_dict,
            200,
        )

        return response
    
    #  creating a patch method
    def patch(self, id):
        #  querying the database by the id
        newsletter = Newsletter.query.filter_by(id = id).first()
        #  creating a for loop to set the attributes for the requests
        for attr in request.form:
            setattr(newsletter, attr, request.form[attr])
        #  adding and commiting the changes to the database
        db.session.add(newsletter)
        db.session.commit()

        # making the new record to a dictionary using to_dict()
        newsletter_dict = newsletter.to_dict()

        #  creating and returning a response
        response = make_response(newsletter_dict, 200)
        return response
    
    # creating a delete method
    def delete(self, id):
        #  querying the database by the id
        newsletter = Newsletter.query.filter_by(id = id).first()
        #  deleting and commiting the changes to the database
        db.session.delete(newsletter)
        db.session.commit()

        #  creating a response message to show that the item is deleted
        delete_message = {
            "message": "record successfully deleted"
        }

        #  creating and returning a response
        response = make_response(delete_message, 200)
        return response





api.add_resource(NewsletterByID, '/newsletters/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)