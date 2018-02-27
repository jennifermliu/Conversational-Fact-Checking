# Conversational-Fact-Checking\

GoogleScript.js: get one-minute text

PastMinute.txt: one-minute text

AnotherMinute.txt: alternative one-minute text (for testing purposes)

subject.json: subject list from Politifact API

people.json: people list from Politifact API

subjectdictionary.csv : csv version of subject.json

peopledictionary.csv : csv version of people.json

SemanticAnalysis.py: get the one-minute text, run the Watson API for get semantic analysis, find keywords and send to text file as input for Politifact API

subjectlist.txt: subject keywords for Politifact API

peoplelist.txt: people keywords for Politifact API

factchecking.html: access the Politifact API by constructing an url from keywords

helper.js: just in case we need a separated js file

statement.txt: original statement for similarity check

headlines.txt: headlines returned by ParallelDots API

similarity.py: use ParallelDots API to find the most matching headline

textbeltpaid.py: takes phone number from user and message output and delivers a text message to a US phone number via Textbelt API
