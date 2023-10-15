from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def search_duckduckgo(query):
    search_url = f'https://duckduckgo.com/html?q={query}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = []
    for result in soup.find_all('a', class_='result__a'):
        title = result.text
        url = result['href']
        if url.startswith('http'):
            results.append({'title': title, 'url': url})
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    duckduckgo_results = search_duckduckgo(query)
    return render_template('results.html', query=query, duckduckgo_results=duckduckgo_results)

if __name__ == '__main__':
    app.run(debug=True)
