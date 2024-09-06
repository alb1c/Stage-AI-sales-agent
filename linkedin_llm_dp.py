import os
import time

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
tableMessages = api.table('appY85YsYveVhA1eC', 'Messages_DoublePrompt')

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

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
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

# "mixtral-8x7b-32768", "gemma-7b-it", "llama3-8b-8192"
model_list = ["llama3-70b-8192","mixtral-8x7b-32768", "gemma-7b-it", "llama3-8b-8192"]
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

for employee_dict in employee_dict_list:
    if employee_dict['name'] == 'Davide Morra':
        continue

    if employee_dict_list.index(employee_dict) > 50:#just two messagges
        continue

    for company_dict in company_dict_list:
        company_name = str(employee_dict['organization_name_short']).strip().lower()
        company_dict_name = str(company_dict['nome_short']).strip().lower()
        
        if company_name == company_dict_name or company_name in company_dict_name or company_dict_name in company_name:
            context = [
            {'role': 'system',
            'content': f""" You are an automated service for an IT company. Your task is to generate a short introductory outbound message to 
            a professional working in a company for proposing a connection in linkedin.The connection should give hints of a possible partnership between the two companies.Write at most 300 characters.

            Information about your company:
            'Nome': 'VOLCANIC MINDS S.R.L.', 'areas of interest': 'digital tailoring, 
            cx-ux-ui design, app mobile, digital strategies, digital transformation, tutoring, app web, coaching, 
            digital evolution, prodotti digitali tailormade, devops, codesign comanagement, digital factory', 'type': 'Consulenza 
            IT'
            
            Here are some examples of cold outreach messages you can learn from but do not copy them!
            Examples:
            
            message 1) Salve Steven, sono Davide Morra,
            co-founder di Volcanic Minds, una digital tech company specializzata in soluzioni tailor-made ad alto contenuto innovativo e di alta qualità. Ha senso presentarci per capire se possiamo esservi d'aiuto in IRA?
            A presto, Davide
            https://volcanicminds.com
            
            message 2) Salve Marco, sono Davide Morra,
            co-founder di Volcanic Minds (https://volcanicminds.com), una digital tech company specializzata in soluzioni tailor-made di alta qualità. Può aver senso presentarci?
            
            message 3) Buongiorno Giorgio,
            sono Davide Morra co-founder di Volcanic Minds.
            Le chiedo il collegamento perché vorrei farle conoscere la nostra realtà specializzata in IT e progetti ad alto contenuto tecnologico. Spero di sentirla presto per una chiacchierata conoscitiva.
            Buon lavoro, Davide

            message 4) Salve Heidi, 
            sono Davide Morra co-founder di Volcanic Minds, una digital tech company che si occupa di soluzioni IT tailor-made (cloud, app, web, design). Le scrivo per entrare in contatto con XXX per future collaborazioni e perché trovo interessante il suo canale e i suoi contenuti.
            
            To perform the task you MUST use the following guidelines:

            0 - Make the message at most 300 characters in english language.
            1 - Dont show any other information beside the message.
            2 - Act as the co-founder of your company and present yourself as Davide Morra.
            3 - Start the message with a short information about the customer's company based on the data that is provided you.
            4 - Make it seem like you have a lot of information about the customer's company in the market.
            5 - The goal of the message is to persuade the professional to make a connection.
            6 - Use simple professional language.
            7 - Avoid using complex words and exaggerated phrases.
            8 - Express interest in collaboration with the customer's company.
            9 - Dont mention specific technologies, focus on the broader concept or benefits.
            10 - Dont express any emotion.
            11 - Dont make assumptions about the customer or the company.
            12 - Dont give information about your company.
            13 - Make the message in english.
            14 - Dont show that you followed the guidelines.
            """},
                {'role': 'user',
                'content': f"""
            Information about the customer: /{employee_dict}
            Information about the customer’s company: /{company_dict}
                """}]
            for groq_model in model_list:
                chat_completion = client.chat.completions.create(
                    messages=context,
                    model=groq_model,
                    max_tokens=8192,
                    temperature=1
                )
                llm_response = chat_completion.choices[0].message.content
                #print('First response')
                #print(groq_model)
                #print('-------------------')
                #print(llm_response)
                time.sleep(3)
                refinement_context = [
                {'role': 'system',
                'content': f""" You are an automated service for an IT company.
                You have a message that you want to communicate effectively to your audience. 
                This message needs translation to ensure clarity, impact, and engagement for italian people.

                Refine this message based on the following guidelines:

                0 - Translate the message in italian.
                2 - Dont show any other information beside the message.
                3 - Ensure the tone is genuine and authentic, making the message feel original and sincere.
                4 - Always start the message with "Salve" or "Buongiorno".
                5 - Replace any word that conveys emotios with simple words that show professionalism.
                6 - Finish the message with a short greeting.
                7 - Dont show other information in the output besides the message.
                8 - Be careful of syntactical, semantical and grammatical errors.
                9 - If the customer's information is missing, refer to the customer using the name of the company.
                10 - Check if you followed all the guidelines I have provided to you.
                """},
                {'role': 'user',
                'content': f"""
                Message to be translated:/{llm_response}
                """}]
                chat_completion = client.chat.completions.create(messages = refinement_context,model=groq_model,
                max_tokens=8192,
                temperature=1)
                response = chat_completion.choices[0].message.content
                #print('Refined response')
                #print(groq_model)
                #print('-------------------')
                print(response)
                # creare msg con func
                message_dict = create_message_data(
                        company=company_dict['nome_short'],
                        company_type=company_dict['categoria'],
                        company_data=stringify(company_dict),
                        lead=employee_dict['name'],
                        lead_title=employee_dict['title'],
                        lead_data=stringify(employee_dict),
                        model=groq_model,
                        message=response)
                tableMessages.create(message_dict)
                print(message_dict['message'])
                time.sleep(3)

            gpt_response = get_completion_from_messages(context, temperature=1)
            gpt_context = [
                {'role': 'system',
                'content': f""" You are an automated service for an IT company.
                You have a message that you want to communicate effectively to your audience. 
                This message needs translation to ensure clarity, impact, and engagement for italian people.

                Refine this message based on the following guidelines:

                0 - Translate the message in italian.
                2 - Dont show any other information beside the message.
                3 - Ensure the tone is genuine and authentic, making the message feel original and sincere.
                4 - Always start the message with "Salve" or "Buongiorno".
                5 - Replace any word that conveys emotios with simple words that show professionalism.
                6 - Finish the message with a short greeting.
                7 - Dont show other information in the output besides the message.
                8 - Be careful of syntactical, semantical and grammatical errors.
                9 - If the customer's information is missing, refer to the customer using the name of the company.
                10 - Check if you followed all the guidelines I have provided to you.
                """},
                {'role': 'user',
                'content': f"""
                Message to be translated:/{gpt_response}
                """}]
            gpt_refined = get_completion_from_messages(gpt_context, temperature=1)
            
            message_dict = create_message_data(
                    company=company_dict['nome_short'],
                    company_type=company_dict['categoria'],
                    company_data=stringify(company_dict),
                    lead=employee_dict['name'],
                    lead_title=employee_dict['title'],
                    lead_data=stringify(employee_dict),
                    model="gpt-3.5-turbo",
                    message=gpt_refined
                )
            tableMessages.create(message_dict)
            print(message_dict['message'])
            time.sleep(3)
