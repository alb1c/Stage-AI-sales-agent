# stage-ai-sales-agent
get_employees_information_from_pollo.py
This code call the "search" API from Apollo.
Important data passed as a request are: 
  - organization_location
  - person_titles
  - q_organization_domains

The response is a json decoded into a dictionary which is parsed to get only the information we need about the employee.
Then, from line 113 to 157 the working years of employees are calculated using the working history of the given employee.

The built dictionary is then updated to Airtable through API.
