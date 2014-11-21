from flask import Flask, request, send_file, render_template, send_from_directory, Markup
import os
from integration import ifogbugz as fb

app = Flask(__name__, static_url_path='')


@app.route("/")
def index():

    projects = None
    error = None

    tmp = fb.get_list_of_projects()

    if type(tmp) == list:
        projects = tmp
    elif type(tmp) == str:
        error = str

    return render_template('home.html', projects=projects,
                                        error=error)

@app.route("/project/<projectname>/")
def project(projectname):
    
    sections = ["Overview", "Points of Contact", "Definitions", 
                "Scope", "User Characteristics", "Assumptions", 
                "Dependencies", "Constraints", "Appendix"]



    project = fb.get_project_data(projectname)

    cases = fb.get_requirements_cases(projectname)

    wikis = fb.get_wiki_content(project['wiki_id'], sections) 

    return render_template('document.html', project=project,
                                            cases=cases,
                                            wikis=wikis)

if __name__ == "__main__":
    app.run(debug=True)