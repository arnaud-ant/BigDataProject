import os
import socket
import requests
from bs4 import BeautifulSoup
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import wikipedia
wikipedia.set_lang("fr")
class reponse:
  def __init__(self):
    self.texte = ""
    self.valeur = True

questions=[]
reponses=[]
socket.setdefaulttimeout(15)
numQuiz=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
url = 'https://www.laculturegenerale.com/test-de-culture-generale-intermediaire-n'+str(numQuiz[3])
r = requests.get(url)

soup = BeautifulSoup(r.content,'html.parser')
for link in soup.find_all('h3', {"class": "hdq_question_heading"}):
  questions.append(link.get_text())

for link in soup.find_all('span', {"class": "hdq_aria_label"}):
  temp = reponse()
  temp.texte=link.get_text()
  reponses.append(temp)
  
for i,link in enumerate(soup.find_all('div', {"class": "hdq-options-check"})):
  if (str(link.input["value"])=="1"):
    reponses[i].valeur = True
  else:
    reponses[i].valeur = False

for i in range(len(questions)):
  print(questions[i]+"\n")
  print("1. " + reponses[i*4].texte + " | " + str(reponses[i*4].valeur) +"\n" +
        "2. " + reponses[i*4+1].texte + " | " + str(reponses[i*4+1].valeur) +"\n" +
        "3. " + reponses[i*4+2].texte + " | " + str(reponses[i*4+2].valeur) +"\n" +
        "4. " + reponses[i*4+3].texte + " | " + str(reponses[i*4+3].valeur) +"\n")

  try:
    if (reponses[i*4].valeur and wikipedia.search(reponses[i*4].texte)[0].lower() in reponses[i*4].texte.lower()):
      print(wikipedia.summary(reponses[i*4].texte,sentences=2))
    if (reponses[i*4+1].valeur and wikipedia.search(reponses[i*4+1].texte)[0].lower() in reponses[i*4+1].texte.lower()):
      print(wikipedia.summary(reponses[i*4+1].texte,sentences=2))
    if (reponses[i*4+2].valeur and wikipedia.search(reponses[i*4+2].texte)[0].lower() in reponses[i*4+2].texte.lower()):
      print(wikipedia.summary(reponses[i*4+2].texte,sentences=2))
    if (reponses[i*4+3].valeur and wikipedia.search(reponses[i*4+3].texte)[0].lower() in reponses[i*4+3].texte.lower()):
      print(wikipedia.summary(reponses[i*4+3].texte,sentences=2))
  except wikipedia.exceptions.PageError:
    pass
  except wikipedia.exceptions.DisambiguationError:
    pass



class Server(BaseHTTPRequestHandler):

  def do_GET(self):
    texte=[]
    valeur=[]
    for reponse in reponses:
        texte.append(reponse.texte)
        valeur.append(reponse.valeur)
    items = questions,texte,valeur
    print(items)
    try:
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(items).encode())
    except:
        self.send_response(404)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(items).encode())

port = 6060
httpd = HTTPServer(('localhost', port), Server)
print(f"Serveur ouvert sur le port {port}")

httpd.serve_forever()