
import requests
import json
import re 
from flask import request

from dotenv import load_dotenv
load_dotenv()

import os
app_id = os.environ.get('APP_ID')
app_key = os.environ.get('APP_KEY')

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

# @app.route('/404.html')
# def error_page():
#   return render_template('404.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/werd/')

@app.route('/werd/<werdname>')

def werd():

    # to get the varaibles sent over the form you need to use the request.args.get method (and import the flask request)
    werdname = request.args.get('werdname')

    print("WORD NAME IS ",werdname)

    url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/en-gb/' + werdname.lower() + '?fields=etymologies&strictMatch=false';
    
    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
    
    data = json.loads(r.text)
    print(data)

    # data looks like this
    """
    This is a multi line comment, using triple quotation marks
    {'id': 'word', 'metadata': {'operation': 'retrieve', 'provider': 'Oxford University Press', 'schema': 'RetrieveEntry'}, 'results': [{'id': 'word', 'language': 'en-gb', 'lexicalEntries': [{'entries': [{'etymologies': ['Old English, of Germanic origin; related to Dutch woord and German Wort, from an Indo-European root shared by Latin verbum ‘word’']}], 'language': 'en-gb', 'lexicalCategory': {'id': 'noun', 'text': 'Noun'}, 'text': 'word'}, {'language': 'en-gb', 'lexicalCategory': {'id': 'verb', 'text': 'Verb'}, 'text': 'word'}, {'language': 'en-gb', 'lexicalCategory': {'id': 'interjection', 'text': 'Interjection'}, 'text': 'word'}], 'type': 'headword', 'word': 'word'}], 'word': 'word'}
    """
    all_etymologies = []

    if 'results' not in data:
      return render_template('another.html', werdname=werdname)

    for werd in data['results']:
        for lexicalEntry in werd['lexicalEntries']:
            if 'entries' in lexicalEntry:
                for entry in lexicalEntry['entries']:
                    if 'etymologies' in entry:
                        for etymology in entry['etymologies']:
                            all_etymologies.append(etymology)
    
    if len(all_etymologies) == 0:
      return render_template('another.html', werdname=werdname)

    print (all_etymologies)
  
    def listToString(s): 
      str1 = "; " 
      return (str1.join(s))

    s = all_etymologies
    roots_text = listToString(s) 

    ## pass the data to the html template
    return render_template('werd.html', all_etymo=roots_text, werdname=werdname) 

if __name__ == '__main__':
  #app.run(debug=True)
  app.run(
    host='0.0.0.0',
    debug=True,
    port=8080
  )
