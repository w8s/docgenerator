from flask import Flask, request, send_file, render_template, send_from_directory, Markup
import os
from integration import ifogbugz as fb

app = Flask(__name__, static_url_path='')


@app.route("/")
def index():
    projects = fb.get_list_of_projects()
    return render_template('home.html', projects=projects)

@app.route("/project/<projectname>/")
def project(projectname):

    project = fb.get_project_data(projectname)

    cases = fb.get_requirements_cases(projectname)

    wiki = fb.get_wiki_content(project['wiki_root']) 

    return render_template('document.html', project=project,
                                            cases=cases,
                                            wiki=Markup(wiki))

if __name__ == "__main__":
    app.run(debug=True)