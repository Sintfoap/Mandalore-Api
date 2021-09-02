# Make the list of pages to look through

import requests

name_file = open('Mandalore_people_list.txt','w')
wookieurl = 'https://starwars.fandom.com/api.php'

### Wookie Base Page Search
page = 'Mandalorian'
action = 'parse'
format = 'json'
prop = 'wikitext'
rvprop = 'content'
wookieparams = {
    'action': action,
    'format': format,
    'prop': prop,
    'page': page,
    'rvslots': '*',
    'rvprop':rvprop,
    'formatversion': '2',
    'redirects':''
}

r = requests.get(wookieurl, params = wookieparams)
data = r.text
undesirables = ['File', ':', 'Star Wars', '1','2','3','4','5','6','7','8','9','0']
check_list = []

datasplit = data.split('==Behind the scenes==')
info = datasplit[0].split('[[')
for section in info:
    line = section.split(']]')[0]
    if not any(word in line for word in undesirables) and line.islower() is False:
        if '|' in line:
            line = line.split('|'[0])
            check_list.append(line[0])
        else:
            check_list.append(line)
set_list = set(check_list)
for name in set_list:
    name_file.write(name + '\n')

name_file.close()