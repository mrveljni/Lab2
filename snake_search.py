import re
import httplib2
import urllib
from bottle import *
# easy-install bottle_sqlite/bottle-sqlite
import bottle.ext.sqlite as sqlite
from collections import OrderedDict
from collections import Counter
from operator import itemgetter
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from beaker.middleware import SessionMiddleware

mainword = ""
maintblstr = ""
emaildict = OrderedDict()
emaildict2 = OrderedDict()

# Session information
session_opts = {
    'session.type': 'file',
    'session.data_dir': './data',
    'session.auto': True
}

plugin = sqlite.Plugin(dbfile='./snake_search.db')
_bottleApp = app()
_bottleApp.install(plugin)
app = SessionMiddleware(_bottleApp, session_opts)


# hook before a request is processed
@hook('before_request')
def update_auth_state():
    # only authenticated users can hit these urls
    restricted_urls = ['/signout']
    # state vars
    s = request.environ.get('beaker.session')
    # views load in either authenticated or unauth content depending on the state of logged_in...
    logged_in = True if (s) and ('user_email' in s) and (s['user_email']) else False
    # save path url here
    BaseTemplate.defaults['path'] = request.path

    if (logged_in == False) and (request.path in restricted_urls):
        return redirect('/')
    else:
        BaseTemplate.defaults['user_email'] = s['user_email'] if (s) and ('user_email' in s) and (s['user_email']) else False
        BaseTemplate.defaults['logged_in'] = logged_in
        return

# Establishing home page and static assets
@route('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='./static/')

# Sign Out
@route('/signout')
def signout():
    session = request.environ.get('beaker.session')
    session['user_email'] = False
    redirect('/')

# Sign In
@route('/signin')
def signin():
     # Step2: App server generates auth URL base on client ID
    flow = flow_from_clientsecrets("client_secrets.json",
                                   scope='https://www.googleapis.com/auth/plus.me '
                                         'https://www.googleapis.com/auth/userinfo.email',
                                   redirect_uri="http://localhost:8080/redirect")
    uri = flow.step1_get_authorize_url()
    redirect(str(uri))

# Redirect to authorize user, extract user email and create session
@route('/redirect')
def redirect_page():  # query entered in SIGN IN MODE
    code = request.query.get('code', '')
    flow = OAuth2WebServerFlow(client_id='1011735639727-i12ach2k55gogrfl603e9fl1ub2u5rm0.apps.googleusercontent.com',
                               client_secret='GDrQHnGCjVoDLJLgP5p7IyAr',
                               scope="https://www.googleapis.com/auth/calendar",
                               redirect_uri='http://localhost:8080/redirect')
    credentials = flow.step2_exchange(code)
    token = credentials.id_token['sub']
    http = httplib2.Http()
    http = credentials.authorize(http)

    # Get user email
    users_service = build('oauth2', 'v2', http=http)
    user_document = users_service.userinfo().get().execute()
    user_email = user_document['email']

    # At this point we create a session for the signed-in user.
    session = request.environ.get('beaker.session') #session is a dictionary
    #saving user_email as key, and value is token
    session[user_email] = token 
    # saving user_email as a value here, using as an identifier for authenticated state.
    session['user_email'] = user_email
    session.save
    redirect('/')

# Main search engine method
@route('/', method="GET")
def main(db):
    global emaildict
    session = request.environ.get('beaker.session') #extracting the global variable dictionary beaker.session
    # print "In Main: ", session['user_email']

    try: #check if the user is passing /?keywords in the URL (request)
        raw_query_string = request.query['keywords']
    except KeyError:
        return template('views/home.tpl')

    if ('user_email' in session) and session['user_email']:
        maindict = OrderedDict()
        # print 'This is user logged in: ', session['user_email']
        # print 'This is main dict: ', maindict
        if session['user_email'] not in emaildict:
            emaildict[session['user_email']]= maindict
        
        mainqueryresult = raw_query_string.lower()  # requesting 'keywords' from HTML and making it lowercase
        mainquerylist = re.findall ('\w+', mainqueryresult)
        
        for mainword in mainquerylist:  # for each word in user query
            if mainword not in emaildict[session['user_email']]:  # check if the word does not exist in the main dictionary
                emaildict[session['user_email']][mainword] = 1  # if nonexistent, add it in and count value = 1
            else:  # else word does exist in main dictionary
                emaildict[session['user_email']][mainword] += 1  # increase count value by 1

    # Add the history and recent data structures only if user is logged in
    if ('user_email' in session) and session['user_email']:
        return template('views/results.tpl', query_str=raw_query_string.lower(), pagerankedList=pageranked_url_fetcher(db), resDict=results(), historyDict = history(), recentList = recentlysearched())
    else:
        return template('views/results.tpl', query_str=raw_query_string.lower(), pagerankedList=pageranked_url_fetcher(db), resDict=results(), historyDict = False, recentList = False)

# Returns user's top 20 queried words as an OrderedDict
def history():
    session = request.environ.get('beaker.session')
    historyDict = emaildict[session['user_email']]
    return OrderedDict(Counter(historyDict).most_common(20));

# Return Query Word & Count as an OrderedDict
def results():  
    # returns the count of words that user has queried (cumulating word count but only to show words of
    # those which user has last queried)
    resDict = OrderedDict()  # declaring ordered dictionary datastructure
    queryresult = request.query['keywords'].lower()  # requesting 'keywords' from HTML and making it lowercase
    querylist = re.findall ('\w+', queryresult) # splitting queryresult by the spaces and reversing it
    for word in querylist:  # for each word in user query
        if word not in resDict:  # if word is not in the results dictionary, add it and assign it a count of 1
            resDict[word] = 1
        else:  # if word is in results dictionary, increase the count by 1
            resDict[word] += 1
    return resDict

# Returns user's 10 most recently searched word as a List
def recentlysearched():
    tblstr=""
    templst=[]

    s = request.environ.get('beaker.session')

    queryresult = request.query['keywords'].lower()  # requesting 'keywords' from HTML and making it lowercase
    querylist = re.findall ('\w+', queryresult)

    recentsearchstring = []
    if s['user_email'] not in emaildict2:
        emaildict2[s['user_email']] = recentsearchstring

    emaildict2[s['user_email']] = emaildict2[s['user_email']] + querylist
    len_of_rss_array = len(emaildict2[s['user_email']])

    templst = emaildict2[s['user_email']][::-1]
    templst = templst[:10]

    return templst

# fetches links and their pagerank scores
# associated with the first word of the user's query
def pageranked_url_fetcher(db):
    firstword = re.findall ('\w+', request.query['keywords'].lower())[0]
    # Need to pass arguments in as a tuple or an array.
    args = [ firstword ]
    cursor = db.execute("select doc_url, doc_url_title, doc_rank from (select doc_index.doc_id, doc_index.doc_url, doc_index.doc_url_title from lexicon,inverted_index,doc_index where lexicon.word_id=inverted_index.word_id and inverted_index.doc_id=doc_index.doc_id  and lexicon.word=?) unranked left join page_rank on unranked.doc_id=page_rank.doc_id order by page_rank.doc_rank desc;", args)
    results = cursor.fetchall();
    # print results
    return results

run(app=app, hosts='localhost', port=8080, debug=True)
