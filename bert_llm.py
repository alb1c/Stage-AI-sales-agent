import os
import time
import BERTSimilarity.BERTSimilarity as bertsimilarity

from dotenv import load_dotenv, find_dotenv
from groq import Groq
from openai import OpenAI
from pyairtable import Table
from pprint import pprint

from airtable_to_json import *



client_OAI = OpenAI(api_key='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')

_ = load_dotenv(find_dotenv())

#API of Base01
api = Api('patdGU0Asa7Y2TB51.f30669d3c655fbb94884171b05b649b449df790e0cd82da7587b87c356be08fc')
tableMessages = api.table('appY85YsYveVhA1eC', 'Messages')

messages_dict_template = {
    'company': '',
    'company_type': '',
    'company_data': '',
    'lead': '',
    'lead_title': '',
    'lead_data': '',
    'model': '',
    'message': '',
    'readability': '',
    'accuracy': '',
    'hallucination': '',
    'omission': '',
    'efficacy': '',
    'relevance': '',
    'fluency': '',
    'coherence': '',
    'transparency': '',
    'safety': '',
    'human alignment': '',
    'other': ''
}

def stringify(dictionary):
    return ' '.join(str(value) for value in dictionary.values())

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=1):
    response = client_OAI.chat.completions.create(model=model,
                                                messages=messages,
                                                temperature=temperature)
    return response.choices[0].message.content



def create_message_data(company, company_type, company_data, lead, lead_title, lead_data, model,
                        message):
    new_message_dict = messages_dict_template.copy()
    new_message_dict['company'] = company
    new_message_dict['company_data'] = company_data
    new_message_dict['company_type'] = company_type
    new_message_dict['lead'] = lead
    new_message_dict['lead_title'] = lead_title
    new_message_dict['lead_data'] = lead_data
    new_message_dict['model'] = model
    new_message_dict['message'] = message
    return new_message_dict


model_list = ["mixtral-8x7b-32768", "llama3-8b-8192", "llama3-70b-8192", "llama-3.3-70b-versatile", "gemma-7b-it", "gemma2-9b-it"]
client = Groq(
        api_key='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',
    )

"""
for groq_model in model_list:
    df = pd.DataFrame([company_messages_dict])  # list of dict as param
    df.to_csv(groq_model + '.csv', mode='w')


messages = [
    {
        "role": "user",
        "content": "Explain the importance of low latency LLMs in summary",
    }
]
"""

employee_dict_list = get_employees_info()#take leads table
company_dict_list = get_companies_info()#take companies table

company_lut = dict()

gold_text = """" Sono Davide Morra co-founder di Volcanic Minds, una digital tech company che si occupa di soluzioni IT tailor-made (cloud, app, web, design). 
Le scrivo per entrare in contatto con XXX per future collaborazioni e perché trovo interessante il suo canale e i suoi contenuti."""


for employee_dict in employee_dict_list:
    if employee_dict['name'] == 'Davide Morra':
        continue
    if employee_dict_list.index(employee_dict) > 20:
        continue
    for company_dict in company_dict_list:
        company_name = str(employee_dict['organization_name_short'])
        company_dict_name = str(company_dict['nome_short'])
        if company_name in company_dict_name or company_dict_name in company_name:
            pprint(company_dict)
            print("\n")
            pprint(employee_dict)
            context = [
        {'role': 'system',
        'content': f""" You are an automated service for an IT company. Your task is to generate a short introductory linkedin outbound message to 
        a professional working in a company for proposing a connection.The connection should give hints of a possible partnership between the two companies.
        Write at most 300 characters.

    Information about your company:
    'Nome': 'VOLCANIC MINDS S.R.L.', 'areas of interest': 'digital tailoring, 
    cx-ux-ui design, app mobile, digital strategies, digital transformation, tutoring, app web, coaching, 
    digital evolution, prodotti digitali tailormade, devops, codesign comanagement, digital factory', 'type': 'Consulenza 
    IT'
    
    To perform the task you MUST use the following guidelines:

    0- Act as the co-founder of your company.
    1 - Present yourself as Davide Morra.
    2 - Focus on the customer and its company.
    3 - Do not include keywords and details of your company in the message.
    4 - Use simple and plain language. Avoid using complex words and exaggerated phrases.
    5 - The goal of the message is to persuade the professional to make a connection.
    6 - Always start the message with "Salve" or "Buongiorno".
    7 - Include general information about the customers company.
    8 - You are not interested in the role or position the customer has in the company.
    9 - Request in a formal and polite way.
    10 - Dont make exaggerated assumptions about the customer or the company.
    11 - Express interest in collaboration with the customer's company.
    12 - Dont include the keywords of the customer's company in the message.
    13 - Dont mention specific technologies, focus on the broader concept or benefits.
    14 - Dont express any interest about the recipient's emotional well-being.
    15 - Use a straightforward and respectful tone.
    Ensure the tone is genuine and authentic, making the message feel original and sincere.
    16 - Mimic a real person writing style as much as possible.
    17 - Make the request as an invitation, not as a question.
    18 - Finish the message with a short greeting.
    19 - Dont show other information in the output besides the message.


    Let's think this step by step:

    1. Firstly get the data of the employee and the company.
    2. - Use words that align well with the data of employee and company.
    3. - Your offer would be in line the areas of work of the employee and company.
    4. - Make the message with at most 300 characters.Very important!!!
    5. - Write the message in english.
    6. - Do a grammar check; if you find any error, correct the message
    7. - If the customer's information is missing, refer to the customer 
    using the name of the company. 
    8. - Dont include dashes and brackets in the messages
    9. - Dont include any opening phrase or any other information in the output beside the linkedin message.
    

    """},
        {'role': 'user',
        'content': f"""
    Information about the customer: \
    {employee_dict}

    Information about the customer’s company: \
    {company_dict}
    """}]
            for groq_model in model_list:
                chat_completion = client.chat.completions.create(
                    messages=context,
                    model=groq_model,
                    max_tokens=32600,
                    temperature=1
                )
                llm_response = chat_completion.choices[0].message.content
                # creare msg con func

                ##here we calculate the distances between the generated messages and the golden text.
                bertsimilarity=bertsimilarity.BERTSimilarity()
                dist = bertsimilarity.calculate_distance(gold_text,llm_response)
                
                #now we need to include the similarity value in the table message.
                
                message_dict = create_message_data(
                        company=company_dict['nome_short'],
                        company_type=company_dict['categoria'],
                        company_data=stringify(company_dict),
                        lead=employee_dict['name'],
                        lead_title=employee_dict['title'],
                        lead_data=stringify(employee_dict),
                        model=groq_model,
                        message=llm_response)
                tableMessages.create(message_dict)
                time.sleep(3)

            gpt_response = get_completion_from_messages(context, temperature=1)
            # creare msg con func
            message_dict = create_message_data(
                    company=company_dict['nome_short'],
                    company_type=company_dict['categoria'],
                    company_data=stringify(company_dict),
                    lead=employee_dict['name'],
                    lead_title=employee_dict['title'],
                    lead_data=stringify(employee_dict),
                    model="gpt-3.5-turbo",
                    message=gpt_response
                )
            tableMessages.create(message_dict)
            time.sleep(5)


"""
Refinement Strategy by Difficulty Level:
1. Easy Prompts:
Gold Text: Simple and direct, with polite language and clear purpose.
Expected Output:
Close match to the gold text since prompts are direct.
Target Cosine Distance: Close to 0.1 (high similarity).
2. Medium Prompts:
Gold Text: Still polite but more contextual, adding subtle references.
Expected Output:
Moderate similarity due to more flexibility in response phrasing.
Target Cosine Distance: 0.2 - 0.4.
3. High Prompts:
Gold Text: Abstract and creatively indirect, focusing on context.
Expected Output:
Less predictable structure, higher variability in responses.
Target Cosine Distance: 0.4 - 0.6 (some creative deviation allowed).
"""
