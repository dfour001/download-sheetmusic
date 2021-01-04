from bs4 import BeautifulSoup
from urllib.request import urlopen

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
    linkList = [baseURL + link['href'] for link in links if link['href'] != '#']

    return linkList
    



def download_pdfs(urls):
    """ Downloads the pdfs from the input song page urls """
    pass


def get_soup(url):
    """ Returns a BeautifulSoup object for the input url """
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    return soup


if __name__ == "__main__":
    soup = get_soup(songListURL)

tables = soup.find_all("table")
print(type(tables[0]))