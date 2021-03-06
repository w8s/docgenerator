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

    app.logger.info('Received the following projects: %r', [project['project'] for project in projects])

    if error:
        app.logger.error('Ran into the following error: ', error)

    return render_template('home.html', projects=projects,
                                        error=error)


@app.route("/project/<projectname>/")
def project(projectname):

    sections = None

    with open (os.path.join(os.path.dirname(os.path.abspath(__file__)), "wiki_sections.cfg"), "r") as section_cfg:
        sections=section_cfg.read().replace('\n', '')

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
