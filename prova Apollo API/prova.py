import requests
import json
import pandas as pd

url = "https://api.apollo.io/v1/auth/health"

querystring = {
    "api_key": "rtafI-P97XlEJloSfTJ43A"
}

headers = {
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, params=querystring)
# print(response.text)

url = "https://api.apollo.io/v1/mixed_people/search"

data = {
    "api_key": "rtafI-P97XlEJloSfTJ43A",
    "q_organization_domains": "aruba.it\nwww.eidosmedia.com",  # SV con \n
    "page": 1,
    "per_page": 10,
    "organization_locations": ["Italy"],
    "person_seniorities": ["senior", "manager"],
    "organization_num_employees_ranges": ["1,1000000"],
    "person_titles": ["sales manager", "engineer manager"]
}

# general manager
# founder
# sales manager

headers = {
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, json=data)

# print(response.text)

decoder = json.JSONDecoder()
diz = decoder.decode(response.text)
peopleList = diz["people"]
print(len(peopleList))

# employment_history lista di dizionari.
# in un dizionario ci sono le chiavi:
#  - "organization_name"
#  - current è true
#  - "updated_at" ci dà idea della qualità del dato

listOfPeopleDict = []
for personDict in peopleList:
    newDict = {k: personDict[k] for k in ("name",
                                          'employment_history', "title", "email", "linkedin_url") if k in personDict}
    employmentHistory = newDict['employment_history']
    for historyDict in employmentHistory:
        if historyDict['current']:
            newDict["organization_name"] = historyDict["organization_name"]
            newDict["updated_at"] = historyDict["updated_at"]
    newDict.pop('employment_history')
    listOfPeopleDict.append(newDict)

for peopleDict in listOfPeopleDict:
    print(peopleDict)

df = pd.DataFrame(listOfPeopleDict)
df.to_csv('test.csv')

# i dati minimi per rappresentare questa persona saranno:
# nome e cognome
# azienda di appartenenza
# email
# ruolo
# data di nascita (per stabilirne l'età) !!!!!!
# link al profilo linkedin
