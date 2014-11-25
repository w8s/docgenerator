from flask import Flask, request, send_file, render_template, send_from_directory, Markup
from flask.ext.pymongo import PyMongo
import os
from integration import ifogbugz as fb

app = Flask(__name__, static_url_path='')

app.config['MONGO_HOST'] = os.environ['MONGO_PORT_27017_TCP_ADDR']
app.config['MONGO_DBNAME'] = 'dauxer'
mongo = PyMongo(app)

@app.route("/")
def index():

    # online_users = mongo.db.users.find({'online': True})

    projects = None
    error = None

    tmp = fb.get_list_of_projects()

    if type(tmp) == list:
        projects = tmp
    elif type(tmp) == str:
        error = str

    app.logger.info('Received the following projects: %r', [project['project'] for project in projects])

    if error:
        app.logger.error('Ran into the following error: ', error)

    return render_template('home.html', projects=projects,
                                        error=error)

@app.route("/project/<projectname>/")
def project(projectname):
    
    sections = ["Overview", "Points of Contact", "Definitions", 
                "Scope", "User Characteristics", "Assumptions", 
                "Dependencies", "Constraints", "Appendix"]

    project = fb.get_project_data(projectname)

    app.logger.info('Working with: %r', projectname)

    cases = fb.get_requirements_cases(projectname)

    app.logger.info('Number of requirement cases: %r', len(cases))

    wikis = fb.get_wiki_content(project['wiki_id'], sections) 

    app.logger.info('Wiki Sections: %r', sections)

    return render_template('document.html', project=project,
                                            cases=cases,
                                            wikis=wikis)

if __name__ == "__main__":
    app.run(debug=True)