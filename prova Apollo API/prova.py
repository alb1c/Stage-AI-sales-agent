import requests
import json
import pandas as pd

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
}

response = requests.request("GET", url, headers=headers, params=querystring)
print(response.text)

""" 
    people API Search
    
    richiesta di persone filtrate per dominio, locazione, seniority e titles
    la risposta è un json con header richiesta e lista di persone
    
    il json viene formattato in dizionario e se ne costruisce un altro più ridotto coi soli dati di intersse
    poi viene convertito in CSV con panda
    
"""

url = "https://api.apollo.io/v1/mixed_people/search"

data = {
    "api_key": "rtafI-P97XlEJloSfTJ43A",
    "q_organization_domains": "aruba.it\nwww.eidosmedia.com",  # SV con \n
    "page": 1,
    "per_page": 10,
    "organization_locations": ["Italy"],
    "person_seniorities": ["senior", "manager"],
    "organization_num_employees_ranges": ["1,1000000"],
    # An array of intervals to include people belonging in an organization having number of employees in a range
    "person_titles": ["sales manager", "founder", "general manager"]
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
    # "name", 'employment_history', "title", "email", "linkedin_url"
    filteredPersonDict = {k: personDict[k] for k in ("first_name", "last_name", "id",
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
    for historyDict in employmentHistory:
        if historyDict['current']:
            filteredPersonDict["organization_name"] = historyDict["organization_name"]
            filteredPersonDict["updated_at"] = historyDict["updated_at"]

    # elimino employment_history dal dizionario
    filteredPersonDict.pop('employment_history')

    # appendo il dizionario filtrato
    listOfFilteredPeopleDict.append(filteredPersonDict)

for peopleDict in listOfFilteredPeopleDict:
    print(peopleDict)

"""
    People API non permette di accedere alle mail personali.
    Bisogna utilizzare l'endpoint Enrich.
    Dati in input il nome o l'azienda o altro, questa API restituisce una lista di persone
        le cui informazioni coincidono.
    
    Utilizzo i dati già ricavati delle persone per ricavare la loro mail
    E' necessario fare una request per ogni persona (molto costoso)
"""

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

df = pd.DataFrame(listOfFilteredPeopleDict)
# df.groupby(['organization_name'])
df.to_csv('test.csv')

# manca la data di nascita della persona
