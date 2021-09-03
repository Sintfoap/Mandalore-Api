# Gets the events from dc.data_collect and finds the participants


import Mandalore_test_data_collect as dc
import json

########################
def parse_data(sw_info):
    participants_list = []
    for name in data_file:
        data = sw_info[name]
        participants_dict = {}
        try:
            for event in dc.events_dict:
                side_dict = {}
                if name == event:
                    nobar = data.split('\n|')
                    for byte in nobar:
                        for side in sides:
                            side_list = []
                            for commander in commanders:
                                if side in commander:
                                    commander_list= []
                                    if commander in byte and byte != commander:
                                        try:
                                            noquote = byte.split('Quote')
                                            byte = noquote[0]
                                        except:
                                            continue
                                        if '*' in byte:
                                            noast = byte.split('*')
                                            for bit in noast:
                                                sentence = debracket(bit)
                                                if sentence != '':
                                                    commander_list.append(sentence)
                                        else:
                                            sentence = debracket(byte)
                                            if sentence != '':
                                                    commander_list.append(sentence)
                                        if commander_list != '':
                                            side_list.append(commander_list)
                            if side_list != []:
                                side_dict[side] = side_list
                if side_dict != {}:
                    participants_dict[event] = side_dict
        except:
            continue

        if participants_dict != {}:
            participants_list.append(participants_dict)
    return participants_list  
######
def debracket(phrase):
    debracketed = ''
    noref = phrase.split('ref')
    for bit in noref:
        if 'name=' not in bit and bit != ' ' and bit !='':
            if ']]' in bit:
                norbar = bit.split(']]')
                # if '[[' in norbar[1] and '{{' not in norbar:
                #     print('norbar[1]')
                #     print(norbar[1])
                for smidge in norbar:
                    nolbar = smidge.split('[[')
                    for sentence in nolbar:
                        nolt = sentence.split('<') 
                        for word in nolt:
                            if '<' not in word:
                                if '|' in word:
                                    nobar = word.split('|')[0]
                                    debracketed += nobar 
                                elif '=' in word:
                                    noeq = word.split('=')[1]
                                    if noeq != '':
                                        debracketed += noeq 
                                else:
                                    debracketed += word 
            else:
                if '<' in bit:
                    smidge = bit.split('<')[0]
                    if '&' in smidge:
                        word = smidge.split('&')[0]
                        debracketed += word 
                    elif '=' in smidge:
                        word = smidge.split('=')[1]
                        debracketed += word 
    return debracketed            
########################

data_file = open('Mandalore_data_list.txt', 'r')
data_file_contents = data_file.read()
sw_info = json.loads(data_file_contents)
commanders = ['commanders1=',
    'commanders2=',
    'commanders3=',
    'commanders4=',
    'participants=',
    'keyparties=',
    'side1=',
    'side2=',
    'side3=',
    'side4=',
    'forces1=',
    'forces2=',
    'forces3=',
    'forces4='
    ]
sides = ['1', 
    '2',
    '3',
    '4'
    ]
### The Actual Program
participants = parse_data(sw_info)

if __name__ == '__main__':
    print(participants)

### Close all the files
data_file.close()