import socket
import requests
from bs4 import BeautifulSoup
import json
import wikipedia
wikipedia.set_lang("fr")

"""
{
  "id": 1
}
"""

def lambda_handler(event, context):
  questions=[]
  reponses=[]
  valeurs=[]
  wiki=[]
  socket.setdefaulttimeout(15)
  numQuiz=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
  url = 'https://www.laculturegenerale.com/test-de-culture-generale-intermediaire-n'+str(numQuiz[event['id']])
  r = requests.get(url)

  soup = BeautifulSoup(r.content,'html.parser')
  for link in soup.find_all('h3', {"class": "hdq_question_heading"}):
    questions.append(link.get_text())

  for link in soup.find_all('span', {"class": "hdq_aria_label"}):
    reponses.append(link.get_text())
    
  for link in soup.find_all('div', {"class": "hdq-options-check"}):
    if (str(link.input["value"])=="1"):
      valeurs.append(True)
    else:
      valeurs.append(False)

  for i in range(len(questions)):
    
    try:
      if (valeurs[i*4] and wikipedia.search(reponses[i*4])[0].lower() in reponses[i*4].lower() 
      and "année" not in questions[i] and "pays" not in questions[i] and "combien" not in questions[i] and "Dans" not in questions[i] 
      and "cité" not in questions[i] and "région" not in questions[i] and "ville" not in questions[i]):
        wiki.append(wikipedia.summary(reponses[i*4],sentences=2))
      if (valeurs[i*4+1] and wikipedia.search(reponses[i*4+1])[0].lower() in reponses[i*4+1].lower()
      and "année" not in questions[i] and "pays" not in questions[i] and "combien" not in questions[i] and "Dans" not in questions[i] 
      and "cité" not in questions[i] and "région" not in questions[i] and "ville" not in questions[i]):
        wiki.append(wikipedia.summary(reponses[i*4+1],sentences=2))
      if (valeurs[i*4+2] and wikipedia.search(reponses[i*4+2])[0].lower() in reponses[i*4+2].lower()
      and "année" not in questions[i] and "pays" not in questions[i] and "combien" not in questions[i] and "Dans" not in questions[i] 
      and "cité" not in questions[i] and "région" not in questions[i] and "ville" not in questions[i]):
        wiki.append(wikipedia.summary(reponses[i*4+2],sentences=2))
      if (valeurs[i*4+3] and wikipedia.search(reponses[i*4+3])[0].lower() in reponses[i*4+3].lower()
      and "année" not in questions[i] and "pays" not in questions[i] and "combien" not in questions[i] and "Dans" not in questions[i] 
      and "cité" not in questions[i] and "région" not in questions[i] and "ville" not in questions[i]):
        wiki.append(wikipedia.summary(reponses[i*4+3],sentences=2))
    except wikipedia.exceptions.PageError:
      wiki.append("")
      pass
    except wikipedia.exceptions.DisambiguationError:
      wiki.append("")
      pass

  json_qu = json.dumps(questions,ensure_ascii=False)
  json_re = json.dumps(reponses,ensure_ascii=False)
  json_va = json.dumps(valeurs,ensure_ascii=False)
  json_wi = json.dumps(wiki,ensure_ascii=False)

  response = {'questions': json_qu,
              'reponses': json_re,
              'valeurs': json_va,
              'wiki': json_wi
  }
  return response
