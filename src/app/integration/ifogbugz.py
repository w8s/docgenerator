from fogbugz import FogBugz
from flask import Markup
from pprint import pprint

FB_URL = "https://dauxer.fogbugz.com"
FB_TOKEN = "6ivr5eehv55nfcucj85aol633q3d08"

def get_project_data(project_name):
    """
    Gets data regarding specific project from FogBugz.

    Returns a project dictionary object:
    {
        "project": project name,
        "id"     : FogBugz ID of project,
        "owner"  : project contact name,
        "email"  : owner's email,
        "wiki_id": FogBugz ID of the wiki with the same name as project
    }
    """
    try:
        fb = FogBugz(FB_URL, FB_TOKEN)
    except:
        return "Cannot connect"

    project_xml = fb.viewProject(sProject=project_name)

    person_xml = fb.viewPerson(ixPerson=project_xml.ixpersonowner.text)

    project_dict = {
                        'project': project_xml.sproject.text.encode('UTF-8'),
                        'id': project_xml.ixproject.text,
                        'owner': person_xml.sfullname.text,
                        'email': person_xml.semail.text,
                        'wiki_id': None
                    }

    wiki_list = fb.listWikis()

    for wiki in wiki_list.wikis.childGenerator():
            if project_dict['project'] == wiki.swiki.text.encode('UTF-8'):
                wiki_id = wiki.ixwiki.text

    project_dict['wiki_id'] = wiki_id

    return project_dict


def get_list_of_projects():
    """
    Gets a list of projects from FogBugz.

    Returns a list of project dictionary objects:
    [
        {
            "project": project name,
            "owner"  : project contact name,
            "email"  : owner's email
        }
    ]
    """
    try:
        fb = FogBugz(FB_URL, FB_TOKEN)
    except:
        return "Cannot connect"

    project_xml = fb.listProjects()

    projects = []

    for project in project_xml.projects.childGenerator():

        project_dict = {'project': project.sproject.text.encode('UTF-8'),
                        # 'id': project.ixproject.text,
                        'owner': project.spersonowner.text,
                        'email': project.semail.text}

        projects.append(project_dict)

    return projects


def get_requirements_cases(project_name):
    """
    Looks for all cases of category:"Requirement" in Fogbugz

    Returns a list of case dictionary objects with the following of a case:
    [
        {
            "id"      : FogBugz ID of case,
            "title"   : Title of case,
            "status"  : FogBugz status (i.e. 'proposed', 'approved', etc),
            "event"   : Description of requirement,
            "area"    : FogBugz area of case (Front End, Support, etc),
            "url"     : URL to actual case in FogBugz,
            "children": Subcases attached to current case
        }
    ]
    """

    fb = FogBugz(FB_URL, FB_TOKEN)

    print "Requesting Data"

    resp = fb.search(q='category:"Requirement" orderby:"ixBug" project:"' + project_name + '"',
                     cols="sTitle,sArea,ixBug,sLatestTextSummary,sFixFor,sStatus,ixBugChildren")

    return get_cases_from_XML(resp)


def get_cases_from_XML(xmlresp):

    cases = []

    for case in xmlresp.cases.childGenerator():

        children = case.ixbugchildren.text
        if not children:
            child_list = []
        else:
            child_list = children.split(',')

        case_url = "%s/default.asp?%s" % (FB_URL, case.ixbug.string.encode('UTF-8'))

        case_dict = {"id"      : case.ixbug.string.encode('UTF-8'),
                     "title"   : case.stitle.string.encode('UTF-8'),
                     "status"  : case.sstatus.string.encode('UTF-8'),
                     "event"   : case.slatesttextsummary.string.encode('UTF-8'),
                     "area"    : case.sarea.string.encode('UTF-8'),
                     "url"     : case_url ,
                     "children": child_list}

        cases.append(case_dict)

    return cases


def get_wiki_content(wiki_id, sections):
    """
    Grabs wiki pages from FogBugz that match a section listed in 'sections'.

    Returns a list of wiki dictionary objects:

    [
        {
            "page_id"   : FogBugz ID of wiki page,
            "name"      : Title of page,
            "url"       : URL to actual wiki page in FogBugz,
            "content"   : Raw HTML of Wiki Content
        }
    ]

    """
    fb = FogBugz(FB_URL, FB_TOKEN)

    wiki_articles = fb.listArticles(ixWiki=wiki_id)

    article_list = []

    for page in wiki_articles.articles.childGenerator():
        if page.sheadline.text.encode('UTF-8') in sections:
            wiki_url = "%s/default.asp?W%s" % (FB_URL, page.ixwikipage.text)
            article_dict = {"page_id": page.ixwikipage.text,
                            "name"   : page.sheadline.text.encode('UTF-8'),
                            "url"    : wiki_url}
            content = fb.viewArticle(ixWikiPage=article_dict["page_id"])
            article_dict['content'] = Markup(content.wikipage.sbody.text.encode('UTF-8'))
            article_list.append(article_dict)

    return article_list
