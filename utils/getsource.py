import requests
import urllib2
import re
import bs4
import chardet

import HTMLParser as hp

def comment_remover(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " " # note: a space and not an empty string
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)

def clear(data, cr=True):

    data = re.sub(r'[^\x00-\x7F]+', '', str(data))
    data = hp.HTMLParser().unescape(unicode(data)).encode('ascii')
    if(cr):
        data = comment_remover(str(data))

    return data

def find_and_replace(data, words, color):
    tmp = data
    for i in words:
        tmp = tmp.replace(i, color + i + '\x1b[0m')

    return tmp

def view_source(data):
    data = comment_remover(data)
    data = data.replace('function','\x1b[96mfunction\x1b[0m')
    data = find_and_replace(data, ['assert', 'require'], '\x1b[31m')

    print(data)

def getbalance(address):
    result = ''
    apikey = open("~/workspace/contract/ether_scan_api.key", "r").read(1000)
    m= 'account'
    action = 'balance'

    url = 'http://api.etherscan.io/api?module=' + m+ '&action=' + action + '&address=' + address + '&apikey=' + apikey

    response = requests.get(url).json()
    result = response.get('result')

    return result


def sourceget(address):
    '''
    result = ''
    source = ''
    apikey = ''
    m= 'contract'
    action = 'getsourcecode'

    url = 'http://api.etherscan.io/api?module=' + m+ '&action=' + action + '&address=' + address + '&apikey=' + apikey

    response = requests.get(url).json()
    result = response.get('result')

    for i in range(len(result)):
        source += result[i]['SourceCode']
    '''
    token_url = 'https://etherscan.io/address/' + address + '?utm_source=StateOfTheDApps#code'
    source = ''

    try:
        r = requests.get(token_url)
        html = r.text.encode('utf-8')

        soup = bs4.BeautifulSoup(html, 'html.parser')
        parse = str(soup.find('pre', {'class':'js-sourcecopyarea'}))

        #print parse
        source = clear(parse.replace('</pre>', '').split('>')[1].replace('&gt;', '>'), False)
    except:
        print('getsource error!')
        source = ''

    return source

def getcontractname(data):
    tmp = data
    result = []

    while True:
        f = tmp.find('contract')
        if(f < 0):
            break
        f += len('contract')

        s = tmp[f:].find('{')
        if(s < 0):
            break
        s += f

        #print(tmp[f:s].strip())

        result.append(re.findall('[a-z|A-Z|0-9|_]+', tmp[f:s].strip())[0])
        tmp = tmp[s:]

    return result
