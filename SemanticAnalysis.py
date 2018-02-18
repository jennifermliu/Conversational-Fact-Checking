import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, EntitiesOptions, KeywordsOptions, CategoriesOptions, ConceptsOptions, RelationsOptions, SemanticRolesOptions



data=''
with open ("statement.txt", "r") as myfile:
    data=myfile.read()
    # print(data)


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

print(json.dumps(response, indent=2))


#################################################
#extract keywords from semantic analysis

subjectlist=[]
peoplelist=[]
# semantic roles
### object
#####keywords
#######text___
### subject
#####keywords
#######text___
sem=response['semantic_roles']
for i in range (len(sem)):
    record=sem[i]

    # action
    # if 'action' in record:
    #     candidate=record['action']['text']
    #     target.append(str(candidate))

    # object
    if 'object' in record:
        objdict=record['object']
        for key,value in objdict.iteritems():
            # print(key)
            if(key=='keywords'):
                for j in range (len(value)):
                    candidate=value[j]['text']
                    subjectlist.append(str(candidate))

    # subject
    if 'subject' in record:
        subdict=record['subject']
        for key,value in subdict.iteritems():
            # print(key)
            if(key=='keywords'):
                for j in range (len(value)):
                    candidate=value[j]['text']
                    subjectlist.append(str(candidate))

# entities
###if type is person
###disambiguation
#####name___add to peoplelist
###no disambiguation
###text___add to peoplelist
###else
#####text___
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


# concepts
### text___
concepts=response['concepts']
for i in range (len(concepts)):
    record=concepts[i]
    if 'text' in record:
        candidate=record['text']
        subjectlist.append(str(candidate))

print(peoplelist)
print(subjectlist)


polipeople={'barack-obama','hillary-clinton'}
peopledict=set(polipeople)

polisubject={'election'}
subjectdict=set(polisubject)



f = open('peoplelist.txt','w')
for i in range (len(peoplelist)):
    temp = peoplelist[i].lower()
    temp = temp.replace(' ','-')
    # print(temp)
    if temp in peopledict:
        f.write(temp+'\n')
f.close()

f = open('subjectlist.txt','w')
for i in range (len(subjectlist)):
    temp = subjectlist[i].lower()
    temp = temp.replace(' ','-')
    if temp in subjectdict:
        f.write(temp+'\n')
f.close()
