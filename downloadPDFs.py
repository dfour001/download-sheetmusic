from bs4 import BeautifulSoup
from urllib.request import urlopen
from requests import get
import os

# The sheet music for each song is located on its own page
# First I need to get the link to the page for each song
# then download the pdf from the song page.

songListURL = "https://www.guitardownunder.com/fingerstyle.php"
baseURL = "https://www.guitardownunder.com/"

def get_song_page_list(soup):
    """ Gets the urls to the song pages from the main contents page, songListURL
        
        Returns list of URLs"""
    
    table = soup.find('table') # I only need the first table tag
    links = table.find_all('a')
    urlList = [baseURL + link['href'] for link in links if link['href'] != '#']

    return urlList
    

def get_pdf_url(soup):
    downloadButton = soup.find('a', text='Download Pdf File')
    fileName = downloadButton['href'].split('/')[-1]
    pdfURL = f'{baseURL}_scores/{fileName}'
    return pdfURL


def download_pdf(url):
    """ Downloads the pdfs from the input song page urls """
    fileName = url.split('/')[-1]
    if not os.path.exists('sheetmusic'):
        os.makedirs('sheetmusic')

    if fileName not in os.listdir('sheetmusic'):
        print(f'Downloading {fileName}...')
        try:
            pdf = get(url)

            with open(f'sheetmusic/{fileName}', 'wb') as file:
                file.write(pdf.content)
        except:
            print(f'Error downloading {fileName}')
    else:
        print(f'{fileName} already exists.')
        



def get_soup(url):
    """ Returns a BeautifulSoup object for the input url """
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    return soup


if __name__ == "__main__":
    soup = get_soup(songListURL) # Get song contents page as BeautifulSoup object
    urlList = get_song_page_list(soup) # Get urls for each song in contents
    
    # For url in urlList, get list of PDFs to download
    for url in urlList:
        songSoup = get_soup(url) # Get BeautifulSoup object of song page
        pdfURL = get_pdf_url(songSoup)
        download_pdf(pdfURL)
