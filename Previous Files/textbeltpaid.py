import requests


welcome = "Hi! This is your fact checker. Your request to check returned this result:"
headline = ""
url = "http://static.politifact.com.s3.amazonaws.com/politifact/mugs/NYT_TRUMP_CAMPAIGN_5.jpg"
finish = "Thanks for using the fact checker!"
phonenumber = "3122413835"

textmessage = url 



requests.post('https://textbelt.com/text', {
  'phone': phonenumber,
  'message': textmessage,
  'key': '0f34d6a08a703c86e9c18f984f21c4d28ba6f2b0v4OUhT8OjUHbHzUUSJFsme6xR',
})
