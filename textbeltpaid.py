import requests


welcome = "Hi! This is your fact checker. Your request to check returned this result:"
headline = ""
url = ""
finish = "Thanks for using the fact checker!"
phonenumber = "4127600306"

textmessage = welcome + headline + url + finish



requests.post('https://textbelt.com/text', {
  'phone': phonenumber,
  'message': textmessage,
  'key': '0f34d6a08a703c86e9c18f984f21c4d28ba6f2b0v4OUhT8OjUHbHzUUSJFsme6xR',
})
