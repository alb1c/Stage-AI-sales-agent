import datetime
import json
import pandas as pd
import requests

from dateutil.relativedelta import relativedelta
from pyairtable import Api

now = datetime.datetime.now()

""" 
    Autenticazione API
    
    per essere autorizzati all'utilizzo delle API
"""
url = "https://api.apollo.io/v1/auth/health"

querystring = {
    "api_key": "rtafI-P97XlEJloSfTJ43A"
}

headers = {
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/json',
    "x-daily-requests-left": None
}

response = requests.request("GET", url, headers=headers, params=querystring)
print(response.text)
print(response.headers)

""" 
    people API Search
    
    richiesta di persone filtrate per dominio, locazione, seniority e titles
    la risposta è un json con header richiesta e lista di persone
    
    il json viene formattato in dizionario e se ne costruisce un altro più ridotto coi soli dati di intersse
    poi viene convertito in CSV con panda
    
    "aruba.it\n"www.eidosmedia.com"
    "https://synesthesia.it\n" + 
    
    "person_titles": ["sales manager",
                      "founder",
                      "co-founder",
                      "general manager",
                      "CTO",
                      "CEO",
                      "partnership manager"
                      ]
"""

url = "https://api.apollo.io/v1/mixed_people/search"

data = {
    "api_key": "rtafI-P97XlEJloSfTJ43A",
    "q_organization_domains": "volcanicminds.com\nhttps://adoratorio.studio/",  # SV con \n
    "page": 1,
    "per_page": 50,
    "organization_locations": ["Italy"],
    "person_locations": ["Italy"],
    "organization_num_employees_ranges": ["1,1000000"],
    "person_titles": ["sales manager",
                      "founder",
                      "co-founder",
                      "co-fondatore",
                      "general manager",
                      "CTO",
                      "CEO",
                      "partnership manager"
                      ]
}

headers = {
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, json=data)
# print(response.text)

# decoder per convertire json in dict
decoder = json.JSONDecoder()

# conversione
diz = decoder.decode(response.text)

# estrazione della lista di dizionari di persone
peopleList = diz["people"]

# employment_history lista di dizionari.
# in un dizionario ci sono le chiavi:
#  - "organization_name"
#  - "current" è un booleano: true se è il lavoro corrente, false altrimenti
#  - "updated_at" data di aggiornamento del dato, ci potrebbe dare idea della qualità del dato

# lista che contiene i dizionari delle persone con i soli campi di interesse, riguardanti il lavoro corrente
listOfFilteredPeopleDict = []

for personDict in peopleList:
    # prendo solamente i campi che mi interessano:
    filteredPersonDict = {k: personDict[k] for k in ("first_name", "last_name", 'name', "id",
                                                     'employment_history', "title", "email", "linkedin_url") if
                          k in personDict}

    # employment_history: lista di dizionari.
    # ogni dizionario contiene i dati di un'esperienza lavorativa
    # in un dizionario ci sono in particolare le chiavi:
    #  - "organization_name"
    #  - "current" è un booleano: true se è il lavoro corrente, false altrimenti
    #  - "updated_at" data di aggiornamento del dato, ci potrebbe dare idea della qualità del dato
    employmentHistory = filteredPersonDict['employment_history']
    # prendo solamente l'esperienza lavorativa corrente e copio i dati che mi interessano
    possibleCurrentJob = employmentHistory[0]
    if possibleCurrentJob['current']:
        filteredPersonDict["organization_name"] = possibleCurrentJob["organization_name"]
        # filteredPersonDict["updated_at"] = possibleCurrentJob["updated_at"]

    # Non è detto che l'ultimo elemento sia il lavoro meno recente.
    # Bisognerebbe cercarlo nella lista usando start date e calcolare il min.
    # Chiedere quanto è importante anni di lavoro

    firstJob = [2100, 1, 1]
    firstJobFormat = datetime.datetime(firstJob[0], firstJob[1], firstJob[2])

    # conto quante esperienze di quel tipo o gli anni?
    # inizio col conto
    jobDict = {}
    for employmentDict in employmentHistory:

        allKeys = jobDict.keys()
        jobKey = employmentDict['title']
        if jobKey in allKeys:
            jobDict[jobKey] += 1
        else:
            jobDict[jobKey] = 1

        startDate = employmentDict['start_date']

        if startDate:
            startDateDecomposed = startDate.split('-')
            startDateFormat = datetime.datetime(int(startDateDecomposed[0]), int(startDateDecomposed[1]),
                                                int(startDateDecomposed[2]))
            difference = relativedelta(firstJobFormat, startDateFormat)  # è solo in anni
            if difference.years > 0:
                firstJobFormat = startDateFormat

    difference = relativedelta(now, firstJobFormat)

    anniDiLavoro = ""
    if difference.years > 0:
        anniDiLavoro = difference.years
    else:
        anniDiLavoro = 0

    filteredPersonDict['anni di lavoro'] = anniDiLavoro

    # firstEmploymentFake = employmentHistory[-1]
    # fakeStartDate = firstEmploymentFake['start_date']

    # print(filteredPersonDict['last_name'] + "; data primo lavoro --> " + str(firstJobFormat.year) + "-" +
    # str(firstJobFormat.month) + "-" + str(firstfJobFormat.day))
    # difference = relativedelta(now, startDateFormat)
    #             anniDiLavoro = str(difference.years)

    # print("fake start date:", fakeStartDate)

    # elimino employment_history dal dizionario
    filteredPersonDict.pop('employment_history')

    # appendo il dizionario filtrato
    jobString = ""
    for job, count in jobDict.items():
        jobString += job + ":" + str(count) + ";"

    filteredPersonDict['jobListCount'] = jobString
    listOfFilteredPeopleDict.append(filteredPersonDict)

for peopleDict in listOfFilteredPeopleDict:
    print(peopleDict)

# csv
# df = pd.DataFrame(listOfFilteredPeopleDict)
# df.to_csv('test.csv')

# airtable
api = Api('patJOb9tIJFKIWWgY.b819e373ca873b166c123d2f45128d9b26ae2f59ee8621c4a048c65f2a685bac')
table = api.table('appgT3WMtNOvBcQSo', 'Leads info')

for peopleDict in listOfFilteredPeopleDict:
    exDict = peopleDict
    table.create(exDict)

"""
    People API non permette di accedere alle mail personali.
    Bisogna utilizzare l'endpoint Enrich.
    Dati in input il nome o l'azienda o altro, questa API restituisce una lista di persone
        le cui informazioni coincidono.
    
    Utilizzo i dati già ricavati delle persone per ricavare la loro mail
    E' necessario fare una request per ogni persona (molto costoso)


url = "https://api.apollo.io/v1/people/match"
# per ogni persona che ho trovato devo fare una richiesta per avere la mail

# siccome un iteratore non è modificabile, scorro la lista di dizionari con un indice
numOfPeople = len(listOfFilteredPeopleDict)

for i in range(numOfPeople):
    peopleDict = listOfFilteredPeopleDict[i]
    data = {
        "api_key": "rtafI-P97XlEJloSfTJ43A",
        "id": peopleDict["id"], # identificatore univoco
        "reveal_personal_emails": True,
    }

    response = requests.request("POST", url, headers=headers, json=data)

    # conversione da json a dizionario
    jsonToDic = decoder.decode(response.text)

    # estrazione della lista di dizionari di persone (chiave "person")
    personInfoDic = jsonToDic["person"]

    # estrazione della mail
    email = personInfoDic['email']

    # aggiorno l'informazione sul mio oggetto
    peopleDict['email'] = email

# manca la data di nascita della persona
"""
