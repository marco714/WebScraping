import requests
from bs4 import BeautifulSoup
import credetiantial

LOGIN_URL = 'https://the-internet.herokuapp.com/authenticate'
SECURE_URL = 'https://the-internet.herokuapp.com/secure'

payload = {
    'username':credetiantial.username,
    'password':credetiantial.password
}

#Using the context manager so that you are stay connected to the session
with requests.session() as s:
    s.post(LOGIN_URL, data=payload)
    r = s.get(SECURE_URL)
    soup = BeautifulSoup(r.content, 'html.parser')

    print(soup.prettify())
