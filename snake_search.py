import bottle
from bottle import *
from collections import OrderedDict
from operator import itemgetter
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from beaker.middleware import SessionMiddleware

mainword = ""
maintblstr = ""
maindict = OrderedDict()  # creating ordered dictionary "maindict"

@route('/')  # getting user query IN ANONYMOUS MODE
def home_page():
    return static_file('snake_search.html', root='./')
@route('<filename:path>')
def static(filename):
    return static_file(filename, root='./')

@route('/redirect')
def redirect_page():  # query entered in SIGN IN MODE
    # Step2: App server generates auth URL base on client ID
    flow = flow_from_clientsecrets("client_secrets.json", scope='https://www.googleapis.com/auth/plus.me '
                                                                'https://www.googleapis.com/auth/userinfo.email',
                                   redirect_uri="http://localhost:8080")
    print "Flow from client secrets"
    uri = flow.step1_get_authorize_url()
    print "Get Auth"
    bottle.redirect(str(uri))
    print "Bottle redirect"

    code = request.query.get('code', '')
    flow = OAuth2WebServerFlow(client_id='1011735639727i12ach2k55gogrfl603e9fl1ub2u5rm0.apps.googleusercontent.com',
                               client_secret='GDrQHnGCjVoDLJLgP5p7IyAr',
                               scope='https://accounts.google.com/o/oauth2/token,auth_provider_x509_cert_url'
                                     'https://www.googleapis.com/oauth2/v1/certs',
                               redirect_uri='http://localhost:8080')
    credentials = flow.step2_exchange(code)
    token = credentials.id_token['sub']
    print "Line 27"
    http = httplib2.Http()
    http = credentials.authorize(http)
    #   Get user email
    users_service = build('oauth2', 'v2', http=http)
    user_document = users_service.userinfo().get().execute()
    user_email = user_document['email']


@route('/firstpage', method="GET")
def main():
    global mainword  # declaring global word string
    global maintblstr
    global maindict  # declaring global ordered dictionary datastructure
    mainqueryresult = request.query['keywords'].lower()  # requesting 'keywords' from HTML and making it lowercase
    mainquerylist = mainqueryresult.split(" ")  # splitting queryresult by the spaces and reversing it

    for mainword in mainquerylist:  # for each word in user query
        if mainword not in maindict:  # check if the word does not exist in the main dictionary
            maindict[mainword] = 1  # if nonexistent, add it in and count value = 1
        else:  # else word does exist in main dictionary
            maindict[mainword] += 1  # increase count value by 1

    for k, v in maindict.iteritems():  # for each key and value in maindictionary, go through each item
        maintblstr = maintblstr + "<tr> <td> {queryword} </td> <td> {querycount} </td>".format(queryword=k,
                                                                                               querycount=v)  # add each item as a row in the table HTML format
    resultstringreturn = results()
    # historystringreturn = history() ####you do not return history in anonymous mode

    return resultstringreturn, "<br><br><br>"  # , historystringreturn


def history():  # returns top 20 queried words
    global maindict
    word = ""
    tblstr = ""
    dict = OrderedDict()
    newdict = OrderedDict()
    queryresult = request.query['keywords'].lower()
    querylist = queryresult.split(" ")
    newdict = sorted(maindict, key=maindict.get,
                     reverse=True)  # returns new dict list of values sorted by decreasing # of counts...not a dictionary
    newdict = newdict[:20]  # cut the sorted new dict list to only 20 elements (highest count decreasing)
    for newdictword in newdict:  # for each word in the 20 element list
        tblstr = tblstr + "<tr> <td> {queryword} </td> <td> {querycount} </td>".format(queryword=newdictword,
                                                                                       querycount=maindict[
                                                                                           newdictword])  # add the word in 20 element list and it's value in tblstr
    mainsearchstring = "Top 20 queried words:"  # SHOWS ON RESULT PAGE: history table header
    maintableheader = "<tr> <td> <b> Word </b> </td> <td> <b> Count </b> </td></tr>"  # SHOWS ON RESULT PAGE: header of table
    maintablebeginning = "<table id = \"history\">"  # SHOWS ON RESULT PAGE: table id beginning
    maintableend = "</table>"  # SHOWS ON RESULT PAGE: table id ender
    historystring = mainsearchstring + maintablebeginning + maintableheader + tblstr + maintableend
    return historystring;


def results():  # returns the count of words that user has queried (cumulating word count but only to show words of those which user has last queried)
    i = 0
    global maindict  # declaring global main dictionary used in main()
    word = ""  # declaring word string
    tblstr = ""
    dict = OrderedDict()  # declaring ordered dictionary datastructure
    newdict = OrderedDict()
    queryresult = request.query['keywords'].lower()  # requesting 'keywords' from HTML and making it lowercase
    querylist = queryresult.split(" ")  # splitting queryresult by the spaces and reversing it
    for word in querylist:  # for each word in user query
        # if word in maindict: #if the word exists in main dictionary (saved as server runs)
        # dict[word]=maindict[word] #make the count of current results dictionary = count of main dictionary
        if word not in dict:  # if word is not in the results dictionary, add it and assign it a count of 1
            dict[word] = 1
        else:  # if word is in results dictionary, increase the count by 1
            dict[word] += 1
    searchstring = "Search for <i>\"{querystring}\" </i> ".format(querystring=request.query['keywords'])
    tableheader = "<tr> <td> <b> Word </b> </td> <td> <b> Count </b> </td></tr>"
    for k, v in dict.iteritems():  # for each key and value in maindictionary, go through each item
        tblstr = tblstr + "<tr> <td> {queryword} </td> <td> {querycount} </td>".format(queryword=k,
                                                                                       querycount=v)  # add each item as a row in the table HTML format
    tablebeginning = "<table id = \"results\">"
    tableend = "</table>"

    resultstring = searchstring + tablebeginning + tableheader + tblstr + tableend
    # for k, v in dict.iteritems():
    # tblstr = tblstr + "<tr> <td> {queryword} </td> <td> {querycount} </td>".format(queryword=k, querycount=v)
    # resultstring = searchstring + tablebeginning + tableheader + tblstr + tableend
    return resultstring;


run(hosts='localhost', port=8080, debug=True)
