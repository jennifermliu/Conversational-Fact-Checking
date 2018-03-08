from paralleldots import set_api_key, get_api_key, similarity, ner, taxonomy, sentiment, keywords, intent, emotion, multilang, abuse, sentiment_social
#DO NOT randomly test, limited to 100 calls/day, for testing go to: https://www.paralleldots.com/semantic-analysis
# more API examples here: https://github.com/ParallelDots/ParallelDots-Python-API

set_api_key("d8v9gnGdk06CfiB3lxGkAd3fiQafeUTPUdmBniHhIoc")

# original statement
statement=''
with open ("oneminutetext.txt", "r") as myfile:
    statement=myfile.read()

headlines=[]
urls=[]
count=0
index=0
with open ("thisJSON.txt", "r") as myfile:
    line=myfile.readline()

    count+=1
    while line:
        if index%2==0:
            headlines.append(line)
        else:
            urls.append(line)
        index+=1
        line=myfile.readline()
        count+=1

print("statement: ")
print(statement)
print("--------------")
print("headlines ")
print(headlines)
print("--------------")
print("urls: ")
print(urls)
print("--------------")

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

print("--------------")
print("Here is the best")
print(best)
print(maxScore)
print(urls[bestindex])
