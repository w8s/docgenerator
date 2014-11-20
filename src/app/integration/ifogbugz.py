from fogbugz import FogBugz
from pprint import pprint

FB_URL = "https://dauxer.fogbugz.com"
# FB_URL = "blah"
# FB_TOKEN = "seven"
FB_TOKEN = "6ivr5eehv55nfcucj85aol633q3d08"

def get_project_data(project_name):
    
    try:
        fb = FogBugz(FB_URL, FB_TOKEN)
    except:
        return "Cannot connect"

    project_xml = fb.viewProject(sProject=project_name)

    person_xml = fb.viewPerson(ixPerson=project_xml.ixpersonowner.text)

    project_dict = {'project': project_xml.sproject.text.encode('UTF-8'),
                        'id': project_xml.ixproject.text,
                        'owner': person_xml.sfullname.text,
                        'email': person_xml.semail.text,
                        'wiki_id': None,
                        'wiki_root': None}

    wiki_list = fb.listWikis()

    for wiki in wiki_list.wikis.childGenerator():
            if project_dict['project'] == wiki.swiki.text.encode('UTF-8'):
                wiki_id = wiki.ixwiki.text
                wiki_root = wiki.ixwikipageroot.text

    project_dict['wiki_id'] = wiki_id
    project_dict['wiki_root'] = wiki_root


    return project_dict

def get_list_of_projects():
    fb = FogBugz(FB_URL, FB_TOKEN)

    project_xml = fb.listProjects()
    wiki_list = fb.listWikis()

    projects = []

    for project in project_xml.projects.childGenerator():

        project_dict = {'project': project.sproject.text.encode('UTF-8'),
                        'id': project.ixproject.text,
                        'owner': project.spersonowner.text,
                        'email': project.semail.text}

        wiki_id = None
        wiki_root = None

        for wiki in wiki_list.wikis.childGenerator():
            if project_dict['project'] == wiki.swiki.text.encode('UTF-8'):
                wiki_id = wiki.ixwiki.text
                wiki_root = wiki.ixwikipageroot.text

        project_dict['wiki_id'] = wiki_id
        project_dict['wiki_root'] = wiki_root

        projects.append(project_dict)

    return projects


def get_requirements_cases(project_name):
    """
    Looks for all cases of category:"Requirement" in Fogbugz

    Returns the following parts of a case:

    * id
    * title
    * status
    * event
    * area
    """

    fb = FogBugz(FB_URL, FB_TOKEN)

    print "Requesting Data"

    resp = fb.search(q='category:"Requirement" orderby:"ixBug" project:"' + project_name + '"', cols="sTitle,sArea,ixBug,sLatestTextSummary,sFixFor,sStatus")

    # cases = get_cases_from_XML(resp)

    return get_cases_from_XML(resp)

def get_cases_from_XML(xmlresp):
    
    cases = []

    for case in xmlresp.cases.childGenerator():
        
        # event_text = ""
        ## Get Text from Event
        # if (not case.events) or (len(case.events) != 0) :
        #     for event in case.events.childGenerator():
        #         if (not event.s) or (len(event.s) != 0) :
        #             event_text = event.s.string.encode('UTF-8')

        case_url = "%s/default.asp?%s" % (FB_URL, case.ixbug.string.encode('UTF-8'))

        case_dict = {"id"    : case.ixbug.string.encode('UTF-8'),
                     "title" : case.stitle.string.encode('UTF-8'),
                     "status": case.sstatus.string.encode('UTF-8'),
                     "event" : case.slatesttextsummary.string.encode('UTF-8'),
                     "area"  : case.sarea.string.encode('UTF-8'),
                     "url"   : case_url }

        cases.append(case_dict)

    return cases


def get_wiki_content(wiki_root):
    fb = FogBugz(FB_URL, FB_TOKEN)

    wiki = fb.viewArticle(ixWikiPage=wiki_root)

    return wiki.wikipage.sbody.text.encode('UTF-8')