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
set_api_key("d8v9gnGdk06CfiB3lxGkAd3fiQafeUTPUdmBniHhIoc")


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
    count="6"
    headlines=[]
    urls=[]
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
                        url = "www.politifact.com"  + entry['statement_url'].encode('utf8')
                        headlines.append(headline)
                        urls.append(url)

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
                        url = "www.politifact.com"  + entry['statement_url'].encode('utf8')
                        headlines.append(headline)
                        urls.append(url)

    return headlines,urls

# input: string array, string array, string
# output: string, int, string
def getSimilarScore(headlines,urls,statement):
    maxScore=0
    best=""
    bestindex=0
    for i in range (len(headlines)):
        scoredict = similarity(statement, headlines[i])
        score = scoredict["actual_score"]
        print("headline "+str(i))
        print(headlines[i])
        print(score)
        print("\n")
        if score > maxScore:
            best=headlines[i]
            maxScore=score
            bestindex=i
    return best,maxScore,urls[bestindex]


def getAlexaOutput(score):
    # high confidence, with a high score
    goodone = "I think I have something. Check your phone."
    # mid confidence
    midone="Maybe this will help? Check your phone."
    # lowerconfidence, with a low score
    badones=[]
    # person and subject match
    badones.append("I don't know for certain, but this could be useful. Check your phone.")
    # no person match
    badones.append("I don't know for certain, but here's something else I found on the topic. Check your phone.")
    # no subject match
    badones.append("I don't know for certain, but here's something else I found from the same person. Check your phone.")
    #no headline
    nothing = "I'm sorry. I couldn't find anything for you."
    print goodone
    print midone
    print badones
    print nothing



def main():
    data=readOneMinuteText("oneminutetext.txt")
    result=semanticAnalysis(data)
    peoplelist,subjectlist=extractKeywords(result)
    # print peoplelist
    # print subjectlist
    # print "..........."
    peopledict,subjectdict,synonymdict=constructDict()
    people,subjects=getAcceptedKeywords(peoplelist,subjectlist,peopledict,subjectdict,synonymdict)
    # print people
    # print subjects
    # print "..........."
    headlines,urls=getHeadlines(people,subjects)
    # for i in range(len(headlines)):
    #     print headlines[i]
    #     print "----------"

    # best,maxScore,url=getSimilarScore(headlines,urls,data)
    # print("--------------")
    # print("Here is the best")
    # print(best)
    # print(maxScore)
    # print(url)
    getAlexaOutput(best)

main()
