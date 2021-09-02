# This goes and gets the APIs once so the programs run faster

print('Getting things set up. . .')

import requests

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


for name in name_file:
    name = name.split('\n')[0]
    wookieparams['page'] = name
    r = requests.get(wookieurl, params = wookieparams)
    data = r.text
    info = data.split('\\n{{')
    for section in info:
        try:
            data_file.write(section)
        except:
            try:
                mini = section.split('\u2015')
                for bit in mini:
                    data_file.write(bit)
            except:
                continue
    data_file.write('~:~ '+ name)
    data_file.write('\n')
        

print('Finished!')
name_file.close()
data_file.close()