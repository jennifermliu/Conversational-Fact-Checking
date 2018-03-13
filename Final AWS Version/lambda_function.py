from __future__ import print_function
import boto3
import requests
import json
import csv
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, EntitiesOptions, KeywordsOptions, CategoriesOptions, ConceptsOptions, RelationsOptions, SemanticRolesOptions
from paralleldots import set_api_key, get_api_key, similarity, ner, taxonomy, sentiment, keywords, intent, emotion, multilang, abuse, sentiment_social
#DO NOT randomly test, limited to 100 calls/day, for testing go to: https://www.paralleldots.com/semantic-analysis
# more API examples here: https://github.com/ParallelDots/ParallelDots-Python-API

# api key for paralleldots
# set_api_key("d8v9gnGdk06CfiB3lxGkAd3fiQafeUTPUdmBniHhIoc")

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)
    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)








# input: a txt file name as string
# output: text as string
def readOneMinuteText(f):
    data=''
    with open(f, "r") as myfile:
        data=myfile.read()
    return data

# input: string
# output: dictionary
def semanticAnalysis(data):
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        username='dcc4c5d9-682d-4eb7-8360-fe8d010b84de',
        password='PobFBTuJ6nEm',
        version='2017-02-27')
    response = natural_language_understanding.analyze(
        text=data,
        features=Features(concepts=ConceptsOptions(limit=8),
        keywords=KeywordsOptions(limit=50),
        entities=EntitiesOptions(model='en-news',limit=50),
        semantic_roles=SemanticRolesOptions (entities=True,keywords=True,limit=50)),
        return_analyzed_text=True)
    #print(json.dumps(response, indent=2))
    return response

# input: dictionary
# output: string array, string array
def extractKeywords(response):
    subjectlist=[]
    peoplelist=[]

    sem=response['semantic_roles']
    for i in range (len(sem)):
        record=sem[i]
        if 'object' in record:
            objdict=record['object']
            for key,value in objdict.iteritems():
                # print(key)
                if(key=='keywords'):
                    for j in range (len(value)):
                        candidate=value[j]['text']
                        subjectlist.append(str(candidate))
        if 'subject' in record:
            subdict=record['subject']
            for key,value in subdict.iteritems():
                # print(key)
                if(key=='keywords'):
                    for j in range (len(value)):
                        candidate=value[j]['text']
                        subjectlist.append(str(candidate))

    ent=response['entities']
    for i in range (len(ent)):
        record=ent[i]
        if 'type' in record:
            if record['type']=='Person':
                if 'disambiguation' in record:
                    candidate=record['disambiguation']['name']
                    peoplelist.append(str(candidate))
                else:
                    candidate=record['text']
                    peoplelist.append(str(candidate))
            else:
                candidate=record['text']
                subjectlist.append(str(candidate))

    concepts=response['concepts']
    for i in range (len(concepts)):
        record=concepts[i]
        if 'text' in record:
            candidate=record['text']
            subjectlist.append(str(candidate))

    # print(peoplelist)
    # print(subjectlist)
    return peoplelist,subjectlist

# input: none
# output: dictionary, dictionary
def constructDict():
    polipeople=[]
    polisubject=[]
    synonymdict={}

    with open('subjectdictionary.csv','rb') as csvfile:
        reader=csv.reader(csvfile)
        for row in reader:
            key=""
            for i in range (len(row)):
                if i==0:
                    key=row[0]
                    polisubject.append(key)
                else:
                    if row[i]!="":
                        synonymdict[row[i]]=key
    with open('peopledictionary.csv','rb') as csvfile:
        reader=csv.reader(csvfile)
        for row in reader:
            for i in range (len(row)):
                if i ==0:
                    key=row[0]
                    polipeople.append(key)
                else:
                    if row[i]!="":
                        synonymdict[row[i]]=key
    peopledict=set(polipeople)
    subjectdict=set(polisubject)

    return peopledict,subjectdict,synonymdict




# input: string array, string array, string dictionary, string dictionary, map
# output: string array, string array
def getAcceptedKeywords(peoplelist,subjectlist,peopledict,subjectdict,synonymdict):
    pl=[]
    sl=[]
    for i in range (len(peoplelist)):
        temp = peoplelist[i].lower()
        temp = temp.replace(' ','-')
        if temp in peopledict:
            if temp not in pl:
                pl.append(temp)
        if peoplelist[i] in synonymdict:
            value=synonymdict[peoplelist[i]]
            if value not in pl:
                pl.append(value)
        if peoplelist[i].lower in synonymdict:
            value=synonymdict[peoplelist[i].lower]
            if value not in pl:
                pl.append(value)
    for i in range (len(subjectlist)):
        temp = subjectlist[i].lower()
        temp = temp.replace(' ','-')
        if temp in subjectdict:
            if temp not in sl:
                sl.append(temp)
        if subjectlist[i] in synonymdict:
            value=synonymdict[subjectlist[i]]
            if value not in sl:
                sl.append(value)
        if subjectlist[i].lower in synonymdict:
            value=synonymdict[subjectlist[i].lower]
            if value not in sl:
                sl.append(value)
    return pl,sl

# input: string array, string array
# output: string array, string array
def getHeadlines(people,subjects):
    editions = ["truth-o-meter", "global-news", "punditfact"]
    count="2"
    headlines=[]
    statements=[]
    urls=[]
    headlinesubjects=[]
    headlinepeople=[]
    headlinetargets=[]
    photolinks=[]
    rulings=[]
    for i in range(len(people)):
        title=people[i]
        if title != "":
            for j in range(len(editions)):
                url = "http://www.politifact.com/api/statements/"+editions[j]+"/"+"people"+"/"+title+"/json/?n="+count+"&callback=?"
                response = requests.get(url)
                if response:
                    data = response.json()
                    for k in range(len(data)):
                        entry = data[k]
                        headline = entry['ruling_headline'].encode('utf8')
                        statement = entry['statement'].encode('utf8')
                        ruling= entry['ruling']['ruling'].encode('utf8')
                        url = "www.politifact.com"  + entry['statement_url'].encode('utf8')
                        headlinespeaker=entry['speaker']['name_slug']
                        temptarget=entry['target']
                        alltargets=[]
                        for target in temptarget:
                            alltargets.append(target['name_slug'])
                        allsubjects=[]
                        tempsubject = entry['subject']
                        for i in range (len(tempsubject)):
                            allsubjects.append(tempsubject[i]['subject_slug'])
                        headlines.append(headline)
                        statements.append(statement)
                        urls.append(url)
                        headlinepeople.append(headlinespeaker)
                        headlinesubjects.append(allsubjects)
                        headlinetargets.append(alltargets)
                        rulings.append(ruling)


    for i in range(len(subjects)):
        title=subjects[i]
        if title != "":
            for j in range(len(editions)):
                url = "http://www.politifact.com/api/statements/"+editions[j]+"/"+"subjects"+"/"+title+"/json/?n="+count+"&callback=?"
                response = requests.get(url)
                if response:
                    data = response.json()
                    for k in range(len(data)):
                        entry = data[k]
                        headline = entry['ruling_headline'].encode('utf8')
                        statement = entry['statement'].encode('utf8')
                        ruling= entry['ruling']['ruling'].encode('utf8')
                        url = "www.politifact.com"  + entry['statement_url'].encode('utf8')
                        headlinespeaker=entry['speaker']['name_slug']
                        temptarget=entry['target']
                        alltargets=[]
                        for target in temptarget:
                            alltargets.append(target['name_slug'])
                        allsubjects=[]
                        tempsubject = entry['subject']
                        for i in range (len(tempsubject)):
                            allsubjects.append(tempsubject[i]['subject_slug'])
                        headlines.append(headline)
                        statements.append(statement)
                        urls.append(url)
                        headlinepeople.append(headlinespeaker)
                        headlinesubjects.append(allsubjects)
                        headlinetargets.append(alltargets)
                        rulings.append(ruling)

    print(len(headlines))
    print(len(statements))
    print(len(urls))
    print(len(headlinepeople))
    print(len(headlinesubjects))
    print(len(headlinetargets))
    print(len(rulings))
    return headlines,statements,urls,headlinepeople,headlinesubjects,headlinetargets,rulings


# input: string array, string array, string
# output: string, int, string
def getSimilarScore(statements,urls,originalstatement):
    maxScore=0
    best=""
    bestindex=0
    for i in range (len(statements)):
        scoredict = similarity(originalstatement, statements[i])
        score = scoredict["actual_score"]
        print("headline statement "+str(i))
        print(statements[i])
        print(score)
        print("\n")
        if score > maxScore:
            best=statements[i]
            maxScore=score
            bestindex=i
    return best,maxScore,urls[bestindex],bestindex


def getAlexaOutput(score,hlperson, hlsubjects, hltargets, people,subjects,headline,url,ruling):
    #no headline
    if(score<0.2):
        return "I'm sorry. I couldn't find anything for you."

    sendText(headline,url,ruling)

    # high confidence, with a high score
    if score > 0.9:
        return "I think I have something. Check your phone."
    # mid confidence
    if score > 0.7:
        return "Maybe this will help? Check your phone."

    matchingsubject=hasSubject(hlsubjects,subjects)
    matchingperson=hasPeople(hlperson,hltargets,people)
    # lowerconfidence, with a low score
    if score > 0.2:
        # person and subject match
        if(matchingsubject and matchingperson):
            return "I don't know for certain, but this could be useful. Check your phone."
        # no person match
        if(matchingsubject):
            return "I don't know for certain, but here's something else I found on the topic. Check your phone."
        # no subject match
        if(matchingperson):
            return "I don't know for certain, but here's something else I found from the same person. Check your phone."

    return "ERROR"



def hasSubject(hlsubjects,subjects):
    for hlsubject in hlsubjects:
        for subject in subjects:
            if hlsubject == subject:
                return True
    return False

def hasPeople(hlperson,hltargets,people):
    for person in people:
        if hlperson == person:
            return True
    for hltarget in hltargets:
        for person in people:
            if hltarget == person:
                return True
    return False


def sendText(headline,url,ruling):
    welcome = "Hi! This is your fact checker. Your request to check returned this result:"
    finish = "Thanks for using the fact checker!"
    phonenumber = "6512475033"
    rulingintro = "Politifact rules this claim as "
    textmessage = welcome + "\n" + headline + "\n" + url + "\n" + rulingintro + ruling + "\n"+ finish
    requests.post('https://textbelt.com/text', {
      'phone': phonenumber,
      'message': textmessage,
      'key': '0f34d6a08a703c86e9c18f984f21c4d28ba6f2b0v4OUhT8OjUHbHzUUSJFsme6xR',
    })



def main():
    # if __name__ == "__main__":
    #     file_id = 'TAKE ID FROM SHAREABLE LINK'
    #     destination = 'DESTINATION FILE ON YOUR DISK'
    #     download_file_from_google_drive(file_id, destination)

    download_file_from_google_drive('1e9YQ9yN8QmXT0sfHS9XqPDfox8Vc_XKN', '/tmp/oneminutetext.txt')

    data=readOneMinuteText("/tmp/oneminutetext.txt")
    result=semanticAnalysis(data)
    peoplelist,subjectlist=extractKeywords(result)
    print(peoplelist)
    print(subjectlist)
    print("...........")
    peopledict,subjectdict,synonymdict=constructDict()
    people,subjects=getAcceptedKeywords(peoplelist,subjectlist,peopledict,subjectdict,synonymdict)
    print(people)
    print(subjects)
    print("...........")
    headlines,statements,urls,headlinepeople,headlinesubjects,headlinetargets,rulings=getHeadlines(people,subjects)
    # for i in range(len(headlines)):
    #     print headlines[i]
    #     print "----------"
    # print headlinepeople
    # print headlinesubjects
    if len(headlines)==0:
        return "I'm sorry. I couldn't find anything for you."

    best,maxScore,url,index=getSimilarScore(statements,urls,data)
    print("--------------")
    print("Here is the best")
    print(best)
    print(maxScore)
    print(url)
    print(index)

    # print headlinepeople[index]
    # print headlinesubjects[index]
    # print people
    # print subjects
    output=getAlexaOutput(maxScore,headlinepeople[index],headlinesubjects[index],headlinetargets[index],people,subjects,headlines[index],url,rulings[index])

    return output

finaloutput=main()
print("--------------")
print("final output: ")
print(finaloutput)

"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

client = boto3.client('lambda')


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Conversational Fact Checking. " \
                    "Please tell me to check a fact by saying, " \
                    "is that true"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me your favorite color by saying, " \
                    "my favorite color is red."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))



# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def Fact_Check(intent,session):
    speech_output = finaloutput
    session_attributes = {}
    reprompt_text = None
    should_end_session = True
    # return build_response(session_attributes, build_speechlet_response(
    #     speech_output, should_end_session))
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return Fact_Check()



def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "factchecking":
        return Fact_Check(intent,session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
