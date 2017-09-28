from flask import Flask, jsonify
from flask_graphql import GraphQLView
from flask_cors import CORS

from models import db_session, Base, engine, Department, Employee
from schema import schema

app = Flask(__name__)

CORS(app, supports_credentials=True)

app.config['DEBUG'] = True
app.url_map.strict_slashes = False


@app.route('/')
def index():
    return jsonify({'name': 'works'})


@app.route('/create-data')
def create_data():
    Base.metadata.create_all(bind=engine)

    engineering = Department(name='Engineering')
    db_session.add(engineering)
    hr = Department(name='Human Resources')
    db_session.add(hr)

    peter = Employee(name='Peter', department=engineering, hobbies="['pool', 'sitting down']",
                     results="{'code': 'A+', 'team work': 'C'}")
    db_session.add(peter)
    roy = Employee(name='Roy', department=engineering, hobbies="['football', 'mechanics']",
                     results="{'code': 'B', 'team work': 'A'}")
    db_session.add(roy)
    tracy = Employee(name='Tracy', department=hr, hobbies="['smoking', 'guns']",
                     results="{'code': 'A+', 'team work': 'B'}")
    db_session.add(tracy)

    db_session.commit()

    return jsonify({'status': 'ok'})


app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run(host='localhost', port=5001)
