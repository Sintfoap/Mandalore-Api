#Get the list of names and search for criteria on them

print('Getting things set up. . .')

import requests

########################
def debracket(line, word):
    mylist = []
    nonbar = line.split('\\n|')
    for phrase in nonbar:
        if word in phrase and word != 'result=':
            norightbar = phrase.split(']]')
            for element in norightbar:
                noslashn = element.split('\\n')
                for bit in noslashn:
                    if ':' not in bit and '&' not in bit and '(' not in bit and '|' not in bit:
                        if '*[[' in bit:
                            if bit[2] == '[' and bit[3]!='[':
                                mylist.append(bit[3:])
                            else:
                                noleftbar = bit.split('[[')
                                mylist.append(noleftbar[1])  
                        elif '=[[' in bit: 
                            noleftbar = bit.split('[[')
                            mylist.append(noleftbar[1]) 

    # Getting the whole phrase for results=
        elif word in phrase and word == 'result=':
            noasterisk = phrase.split('*')
            for element in noasterisk:
                mystring = ''
                noref = element.split('ref')
                goal = noref[0]
                if len(noref) > 2 and '\\n' not in noref[2] and '=' not in noref[2] and noref[2] != '>':
                    goal = str(noref[0][:-1]) + str (noref[2][1:])
                noleftbar= goal.split('[[')
                for bit in noleftbar:
                    norightbar = bit.split(']]')
                    for smidge in norightbar:
                        if '|' in smidge:
                            smidge = smidge.split('|')[1]
                        if  'result=' not in smidge:
                            mystring = mystring + smidge
                        elif smidge != 'result=':
                            mystring = mystring + smidge[7:]
            if mystring != '':
                mylist.append(mystring[:-1])
    return mylist  
######
def format_results(data,attributes):
    propdict={}
    data = data.split('\\n{')
    for attribute in attributes:
        for line in data:
            if attribute in line:
                propdict[attribute] = debracket(line, attribute)
    return propdict
########################

wookieurl = 'https://starwars.fandom.com/api.php'
data_file = open('Mandalore_data_list.txt', 'r')
people_dict = {}
locations_dict = {}
organizations_dict = {}
events_dict = {}

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
attributes = [
    'homeworld=',
    'locations=', 
    'affiliation=', 
    'subgroup=',
    'leader=', 
    'clan=',
    'conflict=',
    'place=',
    'date=[',
    'result='
    ]

### Formatting the results
for information in data_file:
    info = information.split('~:~')
    data = info[0]
    try:
        name = info[1][1:-1]
        formatted = format_results(data, attributes)
        if formatted != {}:
            if 'homeworld=' in formatted:
                people_dict[name] = formatted
            elif 'sector=' in data:
                locations_dict[name] = formatted
            elif 'constructed='in data:
                locations_dict[name] = formatted
            elif 'leader=' in data:
                organizations_dict[name] = formatted
            elif 'commander=' in data:
                organizations_dict[name] = formatted
            elif 'established=' in data:
                organizations_dict[name] = formatted
            elif 'result=' in data:
                events_dict[name] = formatted
            elif 'conflict=' in data:
                events_dict[name] = formatted
    except:
        continue


### If I run this by itself, do this
if __name__ == '__main__':

    print('PEOPLE')
    for person in people_dict:
        print(person)
    #     try:
    #         print(people_dict[person])
    #     except:
    #         print('No result')

    print('\n\nLOCATIONS')
    for location in locations_dict:
        print(location)
        # try:
        #     print(locations_dict[location])
        # except:
        #     print('No result')

    print('\n\nORGANIZATIONS')
    for organization in organizations_dict:
        print(organization)
    #     try:
    #         print(organizations_dict[organization])
    #     except:
    #         print('No result')

    print('\n\nEVENTS')
    for event in events_dict:
        print(event)
    #     # events_file.write(event + '\n')
    #     try:
    #         print(events_dict[event])
    #     except:
    #         print('No result')

    # print(len(people_dict))
    # print(len(locations_dict))
    # print(len(organizations_dict))
    # print(len(events_dict))
        
    
### Closing all the files
data_file.close()
