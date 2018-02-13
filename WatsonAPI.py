import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, EntitiesOptions, KeywordsOptions, CategoriesOptions, ConceptsOptions, RelationsOptions, SemanticRolesOptions



data=''
with open ("oneminutetext.txt", "r") as myfile:
    data=myfile.read()
    print(data)


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

# print(json.dumps(response, indent=2))

target=[]
sem=response['semantic_roles']
# print(sem)
# print(type(sem))
# print(len(sem))
for i in range (len(sem)):
    # action
    candidate=sem[i]['action']['text']
    target.append(str(candidate))

    # object
    objdict=sem[i]['object']
    for key,value in objdict.iteritems():
        # print(key)
        if(key=='keywords'):
            for j in range (len(value)):
                candidate=value[j]['text']
                target.append(str(candidate))

    # subject
    subdict=sem[i]['subject']
    for key,value in subdict.iteritems():
        # print(key)
        if(key=='keywords'):
            for j in range (len(value)):
                candidate=value[j]['text']
                target.append(str(candidate))

print(target)
