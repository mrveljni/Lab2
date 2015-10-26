import bottle
import httplib2
import urllib
from bottle import *
from collections import OrderedDict
from operator import itemgetter
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from beaker.middleware import SessionMiddleware

querylist=[]
mainword = ""
maintblstr = ""
emaildict = OrderedDict()
emaildict2 = OrderedDict()
email_of_user_logged_in = ""

# Session information
session_opts = {
    'session.type': 'file',
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)

# Establishing home page and static assets
@route('<filename:path>')
def static(filename):
    return static_file(filename, root='./')

# Sign Out
@route('/signout')
def signout():
    session = bottle.request.environ.get('beaker.session')
    print "You are in sign out"
    global email_of_user_logged_in
    email_of_user_logged_in=""
    flow = flow_from_clientsecrets("client_secrets.json",
                                   scope='https://www.googleapis.com/auth/plus.me '
                                         'https://www.googleapis.com/auth/userinfo.email',
                                   redirect_uri="https://www.google.com/accounts/Logout?continue=https://appengine.google.com/_ah/logout?continue=http://localhost:8080")
    uri = flow.step1_get_authorize_url()
    bottle.redirect(str(uri))

# Sign In
@route('/signin')
def signin():
    print "You are in sign in"
     # Step2: App server generates auth URL base on client ID
    flow = flow_from_clientsecrets("client_secrets.json",
                                   scope='https://www.googleapis.com/auth/plus.me '
                                         'https://www.googleapis.com/auth/userinfo.email',
                                   redirect_uri="http://localhost:8080/redirect")
    uri = flow.step1_get_authorize_url()
    print"You are being redirected to /redirect"
    bottle.redirect(str(uri))

# Redirect to authorize user, extract user email and create session
@route('/redirect')
def redirect_page():  # query entered in SIGN IN MODE
    print "You are in redirect"
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
    session = bottle.request.environ.get('beaker.session') #session is a dictionary
    session[user_email] = token #saving user_email as key, and value is token
    global email_of_user_logged_in
    email_of_user_logged_in = user_email
    print "This is email: ", email_of_user_logged_in
    session.save
    bottle.redirect('/')


# Main search engine method
@route('/', method="GET")
def main():
    global emaildict
    global email_of_user_logged_in
    session = bottle.request.environ.get('beaker.session') #extracting the global variable dictionary beaker.session
    print "In Main: ", email_of_user_logged_in

    welcome_html = ""
    if (email_of_user_logged_in in session):
        welcome_html = '<html>\
        <div><h3 align="middle">Hey there, {user_email}</h3>\
        <form align="middle" name="snake_signout" action="http://localhost:8080/signout" method="GET">\
        <input style="width:150px; height:100px" type="submit" value="Sign Out!"></input>\
        </form><div></html>'.format(user_email=email_of_user_logged_in)
    else:
        print "WE DO NOT HAVE A SESSION"

    try: #check if the user is passing /?keywords in the URL (request)
        request.query['keywords']
    except KeyError:
        page = urllib.urlopen('snake_search.html').read()
        return welcome_html + page

    if email_of_user_logged_in:
        global mainword  # declaring global word string
        global maintblstr
        maindict = OrderedDict()
        print 'This is user logged in: ', email_of_user_logged_in
        print 'This is main dict: ', maindict
        if email_of_user_logged_in not in emaildict:
            emaildict[email_of_user_logged_in]= maindict
        mainqueryresult = request.query['keywords'].lower()  # requesting 'keywords' from HTML and making it lowercase
        mainquerylist = mainqueryresult.split(" ")  # splitting queryresult by the spaces and reversing it
        for mainword in mainquerylist:  # for each word in user query
            if mainword not in emaildict[email_of_user_logged_in]:  # check if the word does not exist in the main dictionary
                emaildict[email_of_user_logged_in][mainword] = 1  # if nonexistent, add it in and count value = 1
            else:  # else word does exist in main dictionary
                emaildict[email_of_user_logged_in][mainword] += 1  # increase count value by 1
        for k, v in emaildict[email_of_user_logged_in].iteritems():  # for each key and value in maindictionary, go through each item
            maintblstr = maintblstr + "<tr> <td> {queryword} </td> <td> {querycount} </td>".format(queryword=k,
                                                                                                   querycount=v)
                                                                                               # add each item as a row
                                                                                               # in the table HTML
                                                                                               # format
    not_logged_in=""
    not_logged_in = '<h3>You are not logged in a session!</h3>'
    resultstringreturn = results()
    if email_of_user_logged_in:
        historystringreturn = history()
        recentlystringreturn = recentlysearched()
        return welcome_html, resultstringreturn, "<br><br><br>", historystringreturn, "<br><br><br>", recentlystringreturn
    else:
        return not_logged_in, resultstringreturn, "<br><br><br>"

# History Table
def history():  # returns top 20 queried words
    word = ""
    tblstr = ""
    dict = OrderedDict()
    newdict = OrderedDict()
    queryresult = request.query['keywords'].lower()
    querylist = queryresult.split(" ")
    newdict = sorted(emaildict[email_of_user_logged_in], key=emaildict[email_of_user_logged_in].get,
                     reverse=True)  # returns new dict list of values sorted by decreasing # of counts
    newdict = newdict[:20]  # cut the sorted new dict list to only 20 elements (highest count decreasing)
    for newdictword in newdict:  # for each word in the 20 element list
        # add the word in 20 element list and it's value in tblstr
        tblstr = tblstr + "<tr> <td> {queryword} </td> <td> {querycount} </td>".format(queryword=newdictword,
                                                                                       querycount=emaildict
                                                                                       [email_of_user_logged_in]
                                                                                       [newdictword])

    mainsearchstring = "Top 20 queried words:"  # SHOWS ON RESULT PAGE: history table header
    maintableheader = "<tr> <td> <b> Word </b> </td> <td> <b> Count </b> </td></tr>"
    maintablebeginning = "<table id = \"history\">"  # SHOWS ON RESULT PAGE: table id beginning
    maintableend = "</table>"  # SHOWS ON RESULT PAGE: table id ender
    historystring = mainsearchstring + maintablebeginning + maintableheader + tblstr + maintableend
    return historystring;

# Return Table
def results():  # returns the count of words that user has queried (cumulating word count but only to show words of
                # those which user has last queried)
    word = ""  # declaring word string
    global querylist
    tblstr = ""
    dict = OrderedDict()  # declaring ordered dictionary datastructure
    queryresult = request.query['keywords'].lower()  # requesting 'keywords' from HTML and making it lowercase
    querylist = queryresult.split(" ")  # splitting queryresult by the spaces and reversing it
    for word in querylist:  # for each word in user query
        if word not in dict:  # if word is not in the results dictionary, add it and assign it a count of 1
            dict[word] = 1
        else:  # if word is in results dictionary, increase the count by 1
            dict[word] += 1
    searchstring = "Search for <i>\"{querystring}\" </i> ".format(querystring=request.query['keywords'])
    tableheader = "<tr> <td> <b> Word </b> </td> <td> <b> Count </b> </td></tr>"
    for k, v in dict.iteritems():  # for each key and value in dict, go through each item
        # add each item as a row in the table HTML format
        tblstr = tblstr + "<tr> <td> {queryword} </td> <td> {querycount} </td>".format(queryword=k,querycount=v)
    tablebeginning = "<table id = \"results\">"
    tableend = "</table>"

    resultstring = searchstring + tablebeginning + tableheader + tblstr + tableend
    return resultstring;

def recentlysearched():
    tblstr=""
    templst=[]
    print 'You are in recently searched'
    if email_of_user_logged_in:
        recentsearchstring = []
        if email_of_user_logged_in not in emaildict2:
            emaildict2[email_of_user_logged_in]= recentsearchstring
    emaildict2[email_of_user_logged_in] = emaildict2[email_of_user_logged_in] + querylist
    len_of_rss_array = len(emaildict2[email_of_user_logged_in])
    print 'This is length of rss array: ', len_of_rss_array
    a = len_of_rss_array - 10
    print 'This is array: ', emaildict2[email_of_user_logged_in]
    templst = emaildict2[email_of_user_logged_in][a:]
    print 'This is a: ', a
    print 'This is array2: ', templst
    templst = templst[::-1]
    print 'This is array3: ', templst
    mainsearchstring = "10 most recently searched:"  # SHOWS ON RESULT PAGE: history table header
    maintablebeginning = "<table id = \"recently_searched\">"  # SHOWS ON RESULT PAGE: table id beginning
    if len(templst) < 10:
        for i in range(len(templst)):
            tblstr = tblstr + "<tr> <td> {recentword}</td>".format(recentword=templst[i])
    else:
        for i in range(10):
            tblstr = tblstr + "<tr> <td> {recentword}</td>".format(recentword=templst[i])
    maintableend = "</table>"  # SHOWS ON RESULT PAGE: table id ender
    recentsearchstring = mainsearchstring + maintablebeginning + tblstr + maintableend
    return recentsearchstring






run(app=app, hosts='localhost', port=8080, debug=True)
