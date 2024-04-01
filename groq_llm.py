from groq import Groq
from dotenv import load_dotenv, find_dotenv

import os
import openai
import pandas as pd

_ = load_dotenv(find_dotenv())

openai.api_key = os.getenv('OPENAI_API_KEY')


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


# creare lista con stringhe API dei modelli
# ciclo e ad ogni iterazione cambio il param model con lista[i] per i = 0..2
# store output lista o file
# un csv per ogni model

model_list = ["mixtral-8x7b-32768", "llama2-70b-4096"]
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

company_messages_dict = {'message': '',
                         'readability': '',
                         'hallucination': '',
                         'omission': '',
                         'efficacy': ''
                         }
"""
messages = [
    {
        "role": "user",
        "content": "Explain the importance of low latency LLMs in summary",
    }
]
"""

context = [
    {'role': 'system',
     'content': """
You are an automated service for an IT company.
Your task is to write a cold outbound message to a prospective customer for proposing a partnership between your and their's companies.
The user will provide information about the customer and his/her company, so use them!

Information about your company: \
'Nome': 'VOLCANIC MINDS S.R.L.', 'areas of interest': 'digital tailoring, cx-ux-ui design, app mobile, digital strategies, digital transformation, tutoring, app web, coaching, digital evolution, prodotti digitali tailormade, devops, codesign comanagement, digital factory', 'type': 'Consulenza IT'

Here are some examples of cold outreach messages you can learn from but do not copy them!

examples:

message 1) Gentile Denis,

sono Davide Morra, co-founder di Volcanic Minds, una società specializzata in soluzioni IT su misura di alta qualità 
e con design ben curati, di cui siamo molto orgogliosi.

Ho notato con interesse che Sunnyvale condivide con noi, non solo la sede in Piemonte, ma anche un’attenzione particolare alla qualità e una propensione all’innovazione tecnologica che si riflette in un portafoglio clienti di alto profilo. La vostra expertise in ambiti quali lo sviluppo, il cloud, le infrastrutture e la cyber security, unita alla nostra competenza in soluzioni IT personalizzate, potrebbe tradursi in una sinergia strategica vantaggiosa per entrambe le nostre aziende.

<Vi lascio qualche risorsa utile per contestualizzarci:

- Sito istituzionale volcanicminds.com;
- Business playbook su come operiamo in trasparenza playbook.volcanicminds.com;
- Breve presentazione della nostra realtà volcanicminds-pitch.pdf.>

---Se ha senso anche per voi, propongo di organizzare una chiacchierata introduttiva dove presentare le nostre rispettive realtà ed individuare eventuali sinergie o progetti su cui potremmo collaborare insieme. 

Per velocizzare, può trovare qui il mio calendario https://calendly.com/davide-morra/booking. 
In alternativa, se mi fornisce delle date papabili che meglio si adattino alla sua agenda provvedo a mandare quanto prima l’invito.
---
A presto e buon lavoro,
Davide Morra

message 2) Salve Daniele,

sono Davide Morra co-founder di Volcanic Minds. 
Vorrei farle conoscere la nostra realtà specializzata in progetti IT e soluzioni ad alto contenuto tecnologico. 

Abbiamo una forte esperienza nella creazione di piattaforme per la gestione di servizi come teleconsulti, videoconsulti, sistemi di fatturazione specifici per professionisti e pazienti, la definizione di percorsi terapeutici tramite calendari ed email transazionali e altre caratteristiche proprie di un sistema ambizioso di questo tipo. Per una nota startup simile alla vostra, abbiamo gestito con successo la parte devOps, il backend e backoffice e sviluppato sia l’app specialisti (b2b) sia l’app per i clienti finali (b2c) garantendogli un vantaggio tecnologico tangibile.

Credo che questi siano, anche per Serenis, punti importanti e strategici.
Inoltre, ci distinguiamo, perché utilizziamo tecnologie all'avanguardia per garantire un approccio future-proof.

<Vi lascio dei link utili per meglio inquadrarci:
- Sito istituzionale volcanicminds.com;
- Business playbook su come operiamo in trasparenza playbook.volcanicminds.com;
- Breve presentazione della nostra realtà volcanicminds-pitch.pdf.>

---Spero che possa nascere l’interesse per una possibile collaborazione. Nel caso, potremmo organizzare un incontro la prossima settimana. Potete scegliere un orario comodo dal mio calendario https://calendly.com/davide-morra/booking.---

Cordiali saluti, 
Davide Morra

The parts in diamond brackets are examples of proposing resources about your company.
Always include a part of this kind in your message with the links provided.

The parts in triple dashes are examples of proposing a meeting to the customer.
Always include a part of this kind in your message with the link provided.

To perform the task you MUST use the following guidelines:
0 - include information about Volcanic Minds contained in the examples if relevant
1 - never display the information you use to write the message, that means only output the message
6 - don't be too formal
8 - mimic a real person writing style as much as possible
9 - if the string in the angle brackets appears in your message, replace it \
with the string in square brackets without writing the brackets. <Chief Executive Officer>, [CEO]
10 - mention any similarity between your and the customer's company
11 - the 'working life' field contains the years the customer worked in the roles contained in the field 'career'
12 - always use the informations about the company and the customer to write the message
13 - focus on the roles in the customer's career
14 - use a respectful tone


To perform the task use the following actions, let's think this step by step:
1 - write the message in italian
5 - do a grammar check; if you find any error, correct the message
6 - if the 'customer's company' has as type consultancy company, then the type of partnership you \
have to propose is outsourcing service.
Here is an example of how you should propose the outsourcing service:

example) Mi permetto di suggerire una possibile collaborazione tra le nostre realtà, che \
potrebbe portare vantaggi reciproci. Data la vostra expertise come società di consulenza, vi \
propongo di valutare insieme una collaborazione per la gestione dei vostri \
progetti, che potrebbe liberare risorse interne ed ottimizzare i vostri risultati.

Reformulate the example to write this part in the message.
This step must be done in every message so ALWAYS DO THIS STEP!!!.

7 - if the 'customer's company' has as type Non IT, then the type of partnership \
you have to propose is as a consultancy company.
This step must be done in every message so ALWAYS DO THIS STEP!!!.

8 - if the 'customer's company' has as type IT, then the type of partnership \
you have to propose is as an enhancement company.
you must propose to improve their digital evolution, growth \
enhancement, helping reaching the deadlines, and increase the working areas.
This step must follow the instruction provided!
This step must be done in every message so ALWAYS DO THIS STEP!!!.
9 - the message should contain only one among these steps: 6, 7 and 8.
the steps 7, 8 and 9 are mutually exclusive.
9 - you must include a paraphrasis of the parts in diamond brackets!! the paraphrasis must include all the links provided in the bullet list.
10 - you must include a paraphrasis of the parts between triple dashes and always use the link!!
11 - if the customer's information is missing, refer to the customer using the name of the company.
12 - if you wrote more paragraphs about the same topic, just pick one and delete the other.
13 - if the message contains triple dashes, YOU MUST delete them.
14 - if the message contains diamond brackets, YOU MUST  delete them.
15 - if the message contains square brackets, YOU MUST delete them.
16 - check if you missed anything on previous steps.
17 - if the message does not contain a paragraph about the customer, add the paragraph \
to the message.
17 - check if you followed all the guidelines I have provided to you.


"""},
    {'role': 'user',
     'content': """
Information about the customer: \
'name': 'Riccardo Recalchi', 'working life': 23, 'career': 'Chief Executive Officer, Partner & Board Member, Sales & Business Development Director', 'title': 'Chief Executive Officer', 'organization_name': 'Synesthesia', 'Formazione': 'Università degli Studi di Torino-'

Information about the customer’s company: \
'Nome': "SYNESTHESIA S.R.L. SOCIETA' BENEFIT", 'areas of interest': 'mobile apps, content management systems, ecommerce, web sites, web applications, mobile marketing, gaming, gamification, augmented reality, elearning, digital transformation, blockchain, ux, ui design, digital marketing, digital strategies, training, events, marketing, branding, public relations', 'type': 'consultancy company'

"""}]

for groq_model in model_list:
    chat_completion = client.chat.completions.create(
        messages=context,
        model=groq_model
    )
    # print("\n\n", model, ":", "\n", chat_completion.choices[0].message.content)
    llm_response = chat_completion.choices[0].message.content
    company_messages_dict['message'] = llm_response
    df = pd.DataFrame([company_messages_dict])  # list of dict as param
    df.to_csv(groq_model + '.csv')

gpt_response = get_completion_from_messages(context, temperature=1)
company_messages_dict['message'] = gpt_response
df = pd.DataFrame([company_messages_dict])  # list of dict as param
df.to_csv('GPT.csv')
