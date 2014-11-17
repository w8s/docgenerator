from fogbugz import FogBugz
from pprint import pprint

FB_URL = "FOGBUGZ URL"
FB_TOKEN = "FOGBUGZ TOKEN"

fb = FogBugz(FB_URL, FB_TOKEN)

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

    print "Requesting Data"

    resp = fb.search(q='category:"Requirement" orderby:"ixBug" project:"' + project_name + '"', cols="sTitle,sArea,ixBug,latestEvent,sFixFor,sStatus")

    # cases = get_cases_from_XML(resp)

    return get_cases_from_XML(resp)

def get_cases_from_XML(xmlresp):
    
    cases = []

    for case in xmlresp.cases.childGenerator():
        
        event_text = ""
        ## Get Text from Event
        if (not case.events) or (len(case.events) != 0) :
            for event in case.events.childGenerator():
                if (not event.s) or (len(event.s) != 0) :
                    event_text = event.s.string.encode('UTF-8')

        case_url = "%s/default.asp?%s" % (FB_URL, case.ixbug.string.encode('UTF-8'))

        case_dict = {"id"    : case.ixbug.string.encode('UTF-8'),
                     "title" : case.stitle.string.encode('UTF-8'),
                     "status": case.sstatus.string.encode('UTF-8'),
                     "event" : event_text,
                     "area"  : case.sarea.string.encode('UTF-8'),
                     "url"   : case_url }

        cases.append(case_dict)

    return cases