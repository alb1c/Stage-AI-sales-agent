from groq import Groq
from dotenv import load_dotenv, find_dotenv
import pprint
import json
import time
from airtable_to_json import *
import os
from openai import OpenAI

client_OAI = OpenAI(api_key='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')
import pandas as pd

_ = load_dotenv(find_dotenv())

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = client_OAI.chat.completions.create(model=model,
                                              messages=messages,
                                              temperature=temperature)
    return response.choices[0].message.content

employees_messages = {}
# creare lista con stringhe API dei modelli
# ciclo e ad ogni iterazione cambio il param model con lista[i] per i = 0..2
# store output lista o file
# un csv per ogni model

for i in range(5):
    model_list = ["mixtral-8x7b-32768", "llama3-70b-8192", "gemma-7b-it", "llama3-8b-8192"]
    client = Groq(
        api_key='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',
    )

    company_messages_dict = {'message': '',
                            'readability': '',
                            'hallucination': '',
                            'omission': '',
                            'efficacy': '',
                            'relevance': '', 'fluency': '', 'coherence': ''
                            }
    """
    messages = [
        {
            "role": "user",
            "content": "Explain the importance of low latency LLMs in summary",
        }
    ]
    """


    employee_dict = get_employees_info()[i]
    company_dict = get_companies_info()[i]
    employee_name = employee_dict.get("name")
    employees_messages[employee_name] = {}


    #pprint.pprint(employee_dict)
    #pprint.pprint(company_dict)

    context = [
        {'role': 'system',
        'content': f""" You are an automated service for an IT company. Your task is to generate a short introductory linkedin outbound message to 
        a professional working in a company for proposing a connection in the social network.The connection should give hints of a possible partnership between the two companies.The message should be simple, natural and not overwhelming.Write at most 300 characters.

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
    0 - Focus on the customer and its company.
    1 - Do not include keywords and details of your company in the message.
    2 - Never display the information you use to write the message, that means only output the message.
    3 - The goal of the message is to persuade the professional to make a connection.
    4 - Always start the message with "Salve" or "Buongiorno".
    5 - Include information about the customers company.
    6 - Don't be too formal.
    7 - Request in a polite way.
    8 - The request for the connection should be written in a professional and persuasive way.
    9 - Mimic a real person writing style as much as possible
    10 - Express interest in collaboration with the customer's company.
    11 - Dont include the keywords of the customer's company in the message.
    12 - Focus on the fields of work of the customer company.
    13 - Act as the co-founder of your company.
    14 - Use phrases that describe the work of that company based on company information provided.
    15 - Use a respectful tone
    16 - Make the request as an invitation, not as a question.
    17 - Use simple words.
    18 - Finish the message with a greeting.
    19 - Present yourself as Davide Morra.
    20 - Dont show other information in the output besides the message and the total number of characters.


    Let's think this step by step:
    0 - Start with a friendly subject line.
    1 - Introduce yourself and offer your support.
    3 - Make the message with at most 300 characters.Very important!!!
    4 - Write the message in italian
    5 - Do a grammar check; if you find any error, correct the message
    6 - If the customer's information is missing, refer to the customer 
    using the name of the company. 
    7 - If the message contains triple dashes, YOU MUST delete them. 
    8 - If the message contains diamond 
    brackets, YOU MUST  delete them. 
    9 - If the message contains square brackets, YOU MUST delete them. 
    10 - Check if you missed anything on previous steps. 
    11 - Check if you followed all the guidelines I have provided to you.
    12 - Check again if the message is entirely in italian.
    13 - Make the message with at most 300 characters.Very important!!!

    """},
        {'role': 'user',
        'content': f"""
    Information about the customer: \
    {employee_dict}

    Information about the customer’s company: \
    {company_dict}
    """}]
    messages = {}
    #for groq_model in model_list:
    #    responses = []

        # Iterate 5 times for each model
    #    for _ in range(5):
            # Generate completion for the current context and model
    #        chat_completion = client.chat.completions.create(
    #            messages=context,
    #            model=groq_model,
    #            max_tokens=32600,
    #            temperature=1
    #        )
    #        time.sleep(3)
            # Get the response from the completion
    #        llm_response = chat_completion.choices[0].message.content
    #        print(llm_response)
    #        print("\n")
            # Append the response to the list
    #        responses.append(llm_response)

    #    messages[groq_model] = responses
    responses = []
    for _ in range(5):
        gpt_response = get_completion_from_messages(context, temperature=1)
        print(gpt_response)
        company_messages_dict['message'] = gpt_response
        responses.append(gpt_response)
        time.sleep(3)
    messages["GPT"] = responses

    employees_messages[employee_name] = messages

with open('employees_messages1.json', 'w') as json_file:
    json.dump(employees_messages, json_file, indent=4)

pprint(employees_messages)