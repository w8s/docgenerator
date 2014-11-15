from flask import Flask, request, send_file, render_template, send_from_directory
import os
from integration import ifogbugz as fb

app = Flask(__name__, static_url_path='')


@app.route("/")
def index():
    # Specify project
    # create link for project.
    projects = ["PROJECT NAME"]
    return render_template('home.html', projects=projects)

@app.route("/project/<projectname>/")
def project(projectname):

    ## get wiki text
    cases = fb.get_requirements_cases(projectname) 

    return render_template('document.html', projectname=projectname,
                                            cases=cases)

if __name__ == "__main__":
    app.run(debug=True)