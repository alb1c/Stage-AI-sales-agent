from pyairtable import Api

api = Api('patJOb9tIJFKIWWgY.b819e373ca873b166c123d2f45128d9b26ae2f59ee8621c4a048c65f2a685bac')
table = api.table('appgT3WMtNOvBcQSo', 'Leads info')

list_of_dict_row = table.all()
print(list_of_dict_row)
list_of_worker_dict = []
for row in list_of_dict_row:
    unfiltered_row = row['fields']
    filtered_row = {k: unfiltered_row[k] for k in ('name', "anni di lavoro", "Job List",
                                                   'education', "title", "organization_name", "Formazione") if
                    k in unfiltered_row}
    list_of_worker_dict.append(filtered_row)

for worker in list_of_worker_dict:
    print(worker)

table = api.table('appgT3WMtNOvBcQSo', 'Foglio1')
list_of_dict_row = table.all()
list_of_company_dict = []

for row in list_of_dict_row:
    unfiltered_row = row['fields']
    filtered_row = {k: unfiltered_row[k] for k in ('Nome', "Keywords", "categoria", "Riassunti") if
                    k in unfiltered_row}
    list_of_company_dict.append(filtered_row)

for company in list_of_company_dict:
    print(company)
