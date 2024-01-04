import googlesearch as GoogleEngine
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import summary
import Respone_Assis.main as RES_ASSIS

def run(query):
    all_answers_url = ""
    #Search url
    for result in GoogleEngine.search(query, tld="co.in", num=1, stop=1, pause=2):
        url = result
        response = requests.get(url)
        response.close()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Get data from the url
        text_data = ''
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text_data += tag.get_text() + " "
        if len(text_data) > 1024:
            text_data = text_data[:1024]
            
        all_answers_url += text_data + '\n'

    all_answers_url = summary.run(all_answers_url)
    all_answers_url = RES_ASSIS.chatbot(query)
    return all_answers_url
