#Connect Python to MySQL

from getpass import getpass
from mysql.connector import connect, Error
import Mandalore_test_data_collect as dc
import Mandalore_participant_finder as pf
import Mandalore_db_builder as dbb

########################
def add_new_location(location):
    add_location_query = "INSERT INTO locations VALUES (DEFAULT, '" + location + "')"
    cursor.execute(add_location_query)
    connection.commit()
    print('Added a new location: '+ location)
######
def add_new_person(person, homeworld):
    try:
        name = person.split(' ')
        first_name = name[0]
        last_name = name[1]
    except:
        first_name = person
        last_name = 'NULL'
    homeworld_existence = check_location(homeworld)
    if homeworld_existence == False:
        add_new_location(homeworld)
        print('Added the homeworld of ' + homeworld + ' for ' + person)
    add_person_query = 'INSERT INTO people VALUES (DEFAULT, "' + str(first_name) + '", "' + str(last_name) + '", (SELECT location_id FROM locations WHERE name = "' + str(homeworld) + '"))'  
    cursor.execute(add_person_query)
    connection.commit()
    print('Added a new person: ' + person)
######
def add_new_organization(organization, location):
    location_existence = check_location(location)
    if location_existence == False:
        add_new_location(location)
        print('Added the location of ' + location + ' for the organization ' + organization)
    add_organization_query = 'INSERT INTO organizations VALUES (DEFAULT, "' + organization + '",  (SELECT location_id FROM locations WHERE name = "' + location + '"))'
    cursor.execute(add_organization_query)
    connection.commit()
    print('Added a new organization: '+ organization)
######
def add_new_event(event, location, date, result):
    location_existence = check_location(location)
    if location_existence == False:
        add_new_location(location)
        print('Added the location of ' + location + ' for the event '+ event)
    add_event_query = 'INSERT INTO events VALUES (DEFAULT, "' + event + '", (SELECT location_id FROM locations WHERE name = "' + location + '"), "' + date + '", "' + result + '")'
    cursor.execute(add_event_query)
    connection.commit()
    print('Added a new event: ' + event)
######
def add_new_loc_affiliation(location, affiliation):
    add_loc_affiliation_query = 'INSERT INTO location_affiliations VALUES((SELECT location_id FROM locations WHERE name = "' + location + '"), (SELECT organization_id FROM organizations WHERE name = "' + affiliation + '"))'
    cursor.execute(add_loc_affiliation_query)
    connection.commit()  
    print("Added a new affiliation between " + location + " and " + affiliation)
######
def add_new_per_affiliation(person, affiliation):
    try:
        name = person.split(' ')
        first_name = name[0]
        last_name = name[1]
    except:
        first_name = person
        last_name = 'NULL'
    
    add_affiliation_query = 'INSERT INTO people_affiliations VALUES ((SELECT people_id FROM people WHERE first_name = "' + first_name + '" AND last_name = "' + last_name + '"), (SELECT organization_id FROM organizations WHERE name = "' + affiliation + '"))'
    cursor.execute(add_affiliation_query)
    connection.commit()
    print("Added a new affiliation between " + person + " and " + affiliation)
######
def add_new_org_affiliation(organization, affiliation):
    add_org_affiliation_query = 'INSERT INTO organization_affiliations VALUES((SELECT organization_id FROM organizations WHERE name = "' + organization + '"), (SELECT organization_id FROM organizations WHERE name = "' + affiliation + '"))'
    cursor.execute(add_org_affiliation_query)
    connection.commit()  
    print("Added a new affiliation between " + organization + " and " + affiliation)
######
def add_new_participant(person, event, side):
    try:
        name = person.split(' ')
        first_name = name[0]
        last_name = name[1]
    except:
        first_name = person
        last_name = 'NULL'
    
    add_participant_query = 'INSERT INTO participants VALUES((SELECT people_id FROM people WHERE first_name = "' + first_name + '" AND last_name = "' + last_name + '"), (SELECT event_id FROM events WHERE name = "' + event + '"), "' + side + '")'
    cursor.execute(add_participant_query)
    connection.commit()
    print("Added " + person + " participating in " + event + " on side " + side)
###################
def check_location(location):
    get_locations_query = 'SELECT * FROM locations'
    cursor.execute(get_locations_query)
    result = cursor.fetchall()
    already_exists = False
    for row in result:
        if row[1].lower() == location.lower():
            already_exists = True
    return already_exists
######
def check_people(person):
    get_people_query = "SELECT first_name, last_name FROM people"
    cursor.execute(get_people_query)
    result = cursor.fetchall()
    already_exists = False
    try:
        name = person.split(' ')
        first_name = name[0]
        last_name = name[1]
    except:
        first_name = person
        last_name = 'NULL' 
    for row in result:
        if row[0].lower() == first_name.lower() and row[1].lower() == last_name.lower():
            already_exists = True
    return already_exists
######
def check_organization(organization):
    get_organization_query = 'SELECT name FROM organizations'
    cursor.execute(get_organization_query)
    results = cursor.fetchall()
    already_exists = False
    for row in results:
        if row[0].lower() == organization.lower():
            already_exists = True
    return already_exists
######
def check_event(event):
    get_event_query = 'SELECT name FROM events'
    cursor.execute(get_event_query)
    results = cursor.fetchall()
    already_exists = False
    for row in results:
        if row[0].lower() == event.lower():
            already_exists = True
    return already_exists
######
def check_loc_affiliation(location, affiliation):
    check_affiliation(affiliation)
    get_loc_affiliation_query = 'SELECT l.name, o.name from location_affiliations JOIN locations l USING (location_id) JOIN organizations o USING (organization_id)'
    cursor.execute(get_loc_affiliation_query)
    results = cursor.fetchall()
    already_exists = False
    for row in results:
        if row[0].lower() == location.lower() and row[1].lower() == affiliation.lower():
            already_exists = True
    return already_exists
######
def check_per_affiliation(person, affiliation):
    check_affiliation(affiliation)
    try:
        name = person.split(' ')
        first_name = name[0]
        last_name = name[1]
    except:
        first_name = person
        last_name = 'NULL'
    get_affiliations_query = 'SELECT p.first_name, p.last_name, o.name FROM people_affiliations JOIN people as p USING (people_id) JOIN organizations as o USING (organization_id)'
    cursor.execute(get_affiliations_query)
    results = cursor.fetchall()
    already_exists = False
    for row in results:
        if row[0].lower() == first_name.lower() and row[1].lower() == last_name.lower() and row[2].lower() == affiliation.lower():
            already_exists = True
    return already_exists
######
def check_org_affiliation(organization, affiliation):
    check_affiliation(affiliation)
    get_org_affiliations_query = 'SELECT o.name, o2.name FROM organization_affiliations JOIN organizations o USING(organization_id) JOIN organizations o2 ON o2.organization_id = affiliation_id'
    cursor.execute(get_org_affiliations_query)
    result = cursor.fetchall()
    already_exists = False
    for row in result:
        if row[0].lower() == organization.lower() and row[1].lower() == affiliation.lower():
            already_exists = True
        elif row[1].lower() == organization.lower() and row[0].lower() == affiliation.lower():
            already_exists = True
    return already_exists
######
def check_affiliation(affiliation):
    affiliation_existence = check_organization(affiliation)
    if affiliation_existence == False:
        try:
            aff_location = dc.organizations_dict[affiliation]['location=']
        except:
            aff_location = "None"
        location_existence = check_location(aff_location)
        if location_existence == False:
            add_new_location(aff_location)
        add_new_organization(affiliation, aff_location)
######
def check_participant(person, event, side):
    get_participants_query = 'SELECT CONCAT(p.first_name, p.last_name), e.name, pa.side FROM participants pa JOIN people p USING (people_id) JOIN events e USING (event_id)'
    cursor.execute(get_participants_query)
    results = cursor.fetchall()
    already_exists = False
    for row in results:
        if row[0].lower() == person and row[1].lower() == event and row[2] == side:
            already_exists = True
    return already_exists
########################

### Connecting to the MySQL server
try:
    with connect(
        host = 'localhost',
        port = '3306',
        user = input('Username: '),
        password = getpass('Password: '),
        database = 'mandalore',
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(dbb.db_build_query, multi = True)
### Locations
            for location in dc.locations_dict:
                already_exists = check_location(location)
                if already_exists == False:
                    add_new_location(location)
                # else:
                #     print("We already have " + location)
### People
            for person in dc.people_dict:
                already_exists = check_people(person)
                try:
                    homeworld = dc.people_dict[person]['homeworld='][0]
                except:
                    homeworld = dc.people_dict[person]['homeworld=']
                if homeworld != [] and already_exists == False:
                    add_new_person(person, homeworld)
                elif homeworld == [] and already_exists == False:
                    add_new_person(person, 'None')
                # else:
                #     print('We already have ' + person)
### Organizations
            for organization in dc.organizations_dict:
                already_exists = check_organization(organization)
                if already_exists == False:
                    try:
                        location = dc.organizations_dict[organization]['locations='][0]
                        add_new_organization(organization, location)
                    except:
                        print('No location?')
                        add_new_organization(organization, 'None')
### Events
            for event in dc.events_dict:
                already_exists = check_event(event)
                if already_exists == False:
                    try:
                        location = dc.events_dict[event]['place='][0]
                    except:
                        location = 'None'
                    try:
                        date = dc.events_dict[event]['date=['][0]
                    except:
                        date = 'No date'
                    try:
                        result = dc.events_dict[event]['result='][0]
                    except:
                        result = 'None'
                    add_new_event(event, location, date, result)
### Affiliations
        # Locations
            for location in dc.locations_dict:
                affiliations = dc.locations_dict[location]['affiliation=']
                for affiliation in affiliations:
                    already_exists = check_loc_affiliation(location, affiliation)
                    if already_exists == False:
                        add_new_loc_affiliation(location, affiliation)
        # People
            for person in dc.people_dict:
                affiliations = dc.people_dict[person]['affiliation=']
                for affiliation in affiliations:
                    already_exists = check_per_affiliation(person, affiliation)
                    if already_exists == False:
                        add_new_per_affiliation(person, affiliation)
        # Organizations
            for organization in dc.organizations_dict:
                affiliations = dc.organizations_dict[organization]['affiliation=']
                for affiliation in affiliations:
                    already_exists = check_org_affiliation(organization, affiliation)
                    if already_exists == False:
                        add_new_org_affiliation(organization, affiliation)
### Participants
            for mydict in pf.participants:
                for event in dc.events_dict:
                    try:
                        for side in pf.sides:
                            try:
                                for list in mydict[event][side]:
                                    for entity in list:
                                        for person in dc.people_dict:
                                            if person in entity:
                                                already_exists = check_participant(person, event, side)
                                                if already_exists == False:
                                                    add_new_participant(person, event, side)

                            except:
                                continue
                    except:
                            continue

    print('Finished!')           
except Error as e:
    print(e)
