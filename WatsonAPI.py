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
  features=Features(
    entities=EntitiesOptions(
      limit=50),
    keywords=KeywordsOptions(
      limit=50),
    semantic_roles=SemanticRolesOptions(
        entities=True,
        keywords=True,
        limit=50)),
  return_analyzed_text=True)

print(json.dumps(response, indent=2))
