from bs4 import BeautifulSoup
import json
import re
import requests
import requests.exceptions
from urlparse import urlsplit


def get_emails(url):
    parts = urlsplit(url)
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    response = requests.get(url)
    soup = BeautifulSoup(response.text)

    emails = {}
    new_urls = set()

    for td in soup.find_all("td", class_="views-field views-field-field-add-image-fid"):
        for anchor in td.find_all("a"):
            link = anchor.attrs["href"] if "href" in anchor.attrs else ''
            if link.startswith('/'):
              link = base_url + link
            print link
            new_urls.add(link)

    f = open('emails.json', 'w')

    for url in new_urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text)
        pub_title = str(soup.h1.contents[0])
        email_soup = soup.find_all(
            'div',
            class_="field field-type-email field-field-contact-email"
        )[0]
        new_email = str(BeautifulSoup(re.findall('<a href=".*?">', email_soup.text)[0].split("\'+\'")[1]))
        emails.update({pub_title: new_email})
        print pub_title
    return emails

url1 = 'http://www.pw.org/literary_magazines?genre=Poetry&subgenre=All&perpage=100&format=All&pay=no'
url2 = 'http://www.pw.org/literary_magazines?page={}&genre=Poetry&subgenre=All&perpage=100&format=All&pay=no'
emails = {}
emails.update(get_emails(url1))
for i in range(1, 4):
    emails.update(get_emails(url2.format(i)))

f = open('emails.json', 'w')
f.write(json.dumps(emails))
f.close()
