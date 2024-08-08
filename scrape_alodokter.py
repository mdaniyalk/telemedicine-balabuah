import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os
from fake_useragent import UserAgent
import html
import time




def scrape_link(url, base_path):
    """
    Scrape links from a given URL and return a list of links.

    This function sends an HTTP GET request to the specified URL, scrapes links from the HTML content,
    and returns a list of links. It uses the BeautifulSoup library for HTML parsing and the 'fake_useragent'
    library to generate a random User-Agent for the request.

    Parameters:
    - `url` (str): The URL to scrape links from.
    - `base_path` (str): The base path to prepend to each scraped link.

    Returns:
    - `links` (list): A list of links scraped from the specified URL.

    Example usage:
    url = 'https://example.com'
    base_path = 'https://example.com'
    scraped_links = scrape_link(url, base_path)
    """

    links = []
    session = requests.Session()
    user_agent = UserAgent()

    random_user_agent = user_agent.random

    headers = {'user-agent': random_user_agent}
    response = session.get(url, headers=headers)
    session.close()
    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')


        articles_result_div = soup.find('div', {'id': 'articles-result'})


        if articles_result_div:
        
            card_post_elements = articles_result_div.find_all('card-post-index')

        
            for card_post in card_post_elements:
                url_path = card_post.get('url-path')
                links.append(f'{base_path}{url_path}')
    return links



def get_html_data(link):
    """
    Retrieve HTML content from the specified link.

    This function uses the requests library to send an HTTP GET request to the given link. It sets up a session,
    generates a random user agent, and adds it to the request headers for anonymity.

    Parameters:
    - `link` (str): The URL from which to retrieve the HTML content.

    Returns:
    - `html_data` (str): The HTML content retrieved from the specified link.

    Example usage:
    html_content = get_html_data('https://example.com')
    if html_content:
        print(html_content)
    """

    try:
        session = requests.Session()
        user_agent = UserAgent()

        random_user_agent = user_agent.random

        headers = {'user-agent': random_user_agent}
        response = session.get(link, headers=headers)
        session.close()
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve HTML content. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def parse_html(html_content):
    """
    Parse HTML content to extract title and content information.

    This function uses BeautifulSoup to parse the HTML content and extract relevant information:
    - `title`: Extracted from the title tag.
    - `content`: Extracted from the div with class 'post-content'.

    Parameters:
    - `html_content` (str): The HTML content to be parsed.

    Returns:
    - `text` (str): A formatted text containing the extracted title and content information.

    Example usage:
    html_content = "<html>...</html>"
    result = parse_html(html_content)
    print(result)
    """

    try:
    
        soup = BeautifulSoup(html_content, 'html.parser')

    
        title = soup.title.text.strip()

    
        content_div = soup.find('div', class_='post-content')
        content = content_div.get_text(separator='\n').strip() if content_div else ''

        
        text = f"Judul: {title}\nKonten:\n{content}"
        return text
    except Exception as e:
        print(f"An error occurred while parsing HTML: {e}")
        return '\n'



def parse_html_komunitas(html_data):
    """
    Parse HTML data from a Komunitas page and extract relevant information.

    This function takes HTML data as input, uses BeautifulSoup for parsing, and extracts the question, 
    doctor's answer, and doctor's name from the Komunitas page.

    Parameters:
    - `html_data` (str): HTML data to be parsed.

    Returns:
    - `text` (str): Formatted text containing the question, doctor's answer, and doctor's name.

    Example usage:
    html_data = '<html>...</html>'
    result_text = parse_html_komunitas(html_data)
    """
    
    try:
        soup = BeautifulSoup(html_data, 'html.parser')


        question_element = soup.select_one('detail-topic')
        question = question_element.get('member-topic-content')
        question = html.unescape(question)


        doctor_answer_element = soup.select_one('doctor-topic')
        doctor_answer = doctor_answer_element.get('doctor-topic-content')
        doctor_answer = html.unescape(doctor_answer)

        doctor_name = soup.find('doctor-topic').get('doctor-name-title')
        
        text = f"Pertanyaan:\n{question}\nJawaban dari {doctor_name}:\n{doctor_answer}"
        return text
    except Exception as e:
        print(f"An error occurred while parsing HTML: {e}")
        return '\n'




if __name__ == "__main__":
    queries = ['diabetes', 'hipertensi', 'kolesterol', 
               'stroke', 'jantung', 'ginjal', 
               'asma', 'tbc', 'mpasi',
               'stunting', 'demam', 'batuk',
               'flu', 'pilek', 'diare',
               'Gangguan%20Tidur', 'Gangguan%20Mood', 'Kesehatan%20Mental']
    for query in queries:
        url = f'https://www.alodokter.com/search?s={query}&page='
        base_path = 'https://www.alodokter.com'
        filename = 'scraped_text_files/alodokter2'
        

        for i in range(5,10):
            _url = f'{url}{i}'
            links = scrape_link(_url, base_path)
            for j, link in enumerate(tqdm(links, desc=f'Scraping Data From Links page {i}')):
                with open(f'{filename}/{query}-{i}-content-{j}.txt', "a") as file:
                    html_data = get_html_data(link)
                    if html_data is not None:
                        if 'komunitas/' in link:
                            konten = parse_html_komunitas(html_data)
                        else:
                            konten = parse_html(html_data)
                        
                        file.write(f"{konten}\n\n")
                    else:
                        print(f'Error in url: {link}')
        
        
    queries2 = ['alergi', 'infeksi', 'penyakit%20autoimun',
           'kanker', 'arthritis', 'gastroenteritis',
           'hipoglikemia', 'hiperkolesterolemia', 'obesitas',
           'depresi', 'ansietas', 'gangguan%20makan',
           'migrain', 'vertigo', 'tuli',
           'peradangan', 'sepsis', 'penyakit%20paru',
           'kecelakaan', 'trauma', 'patah%20tulang']

    for query in queries2:
        url = f'https://www.alodokter.com/search?s={query}&page='
        base_path = 'https://www.alodokter.com'
        filename = 'scraped_text_files/alodokter2'
        

        for i in range(1,10):
            _url = f'{url}{i}'
            links = scrape_link(_url, base_path)
            for j, link in enumerate(tqdm(links, desc=f'Scraping Data From Links page {i}')):
                with open(f'{filename}/{query}-{i}-content-{j}.txt', "a") as file:
                    html_data = get_html_data(link)
                    if html_data is not None:
                        if 'komunitas/' in link:
                            konten = parse_html_komunitas(html_data)
                        else:
                            konten = parse_html(html_data)
                        
                        file.write(f"{konten}\n\n")
                    else:
                        print(f'Error in url: {link}')
