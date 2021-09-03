# This goes and gets the APIs once so the programs run faster

print('Getting things set up. . .')

import requests
import json

wookieurl = 'https://starwars.fandom.com/api.php'
name_file = open('Mandalore_people_list.txt','r')
data_file = open('Mandalore_data_list.txt', 'w')

### Wookiepedia Page Search
page = ''
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

sw_info = {}


for name in name_file:
    print(f"Processing {name}")
    name = name.strip()
    wookieparams['page'] = name
    r = requests.get(wookieurl, params = wookieparams)
    data = json.loads(r.text)
    try:
        sw_info[name] = data['parse']['wikitext']
    except Exception as e:
        print(e)
    # data_file.write('~:~ '+ name)
    # data_file.write('\n')

data_file.write(json.dumps(sw_info))
        

print('Finished!')
name_file.close()
data_file.close()