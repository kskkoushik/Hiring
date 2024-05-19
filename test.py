
import google.generativeai as genai
import json
import os

import re


resume_text = """September 2023 - September 2024
2026
2020
Korada Sri Krishna Koushik
ML lead at Association for computer machinery
58-15-136/a, Sri Sai Castle, santhinagar, NAD, Visakhapatnam,
Andhra Pradesh, India.
8985183541 | kskkoushik135@gmail.com
Objective
As a dedicated student actively pursuing my undergraduate degree in Artificial Intelligence, I am eager to play a
pivotal role in advancing cutting-edge technologies such as Artificial Intelligence , Deep Learning and Natural
Language Processing. I am seeking a position that enables me to leverage my passion and skills to contribute to
the advancement of these technologies, demystifying the complexities and creating innovative solutions.
Experience
Association for computer machinery (ACM)
ML lead for research
Education
Vignans institute of information technology, Visakhapatnam
Pursuing Btech in cse
Sri Chaitanya English medium school
Higher school
10
Skills
C language
C++17
Python
Flask
Machine learning
Langchain
HTML5
Css
Javascript
React js
Mongodb
Beautiful soup
Web scraping
Fine tuning LLMs
Projects
Tackle-UP
It is an Llama based web integrated AI webapp made using langchain , reactjs and flask which improves
customer relationship between clients and helps in improvement of relationship between service providers and
clients, it provides magical AI tips based on an AI client index . So it avoids sudden loosing out of clients and
Tacke up also acts as a market place to get clients for service providers.
ClarifyAI
It is an AI integrated webapp which clarifies the doubts of Students with their own content rather than from any
external sources. It makes use of langchain, streamlit, flask and Google's magical PALM api. All you need to do
is upload a pdf and aks questions ,  get clarified.
Working on LLMs using feature extraction
Using latest transformer architectures to make a LLM which not just answers but also comes with reasoning
ability. It defines logical analysis based on predefined features extracted during training process
Automatic song recommendation system (c++)
It recommendeds song based on your preferences your previous listening history and and provides new
recommendations through the listenings of people with similar interests like you
Finds next number of a given sequence
It finds the next number in the given sequence of numbers by using different algorithms. It finds the relationship
and gives the accurate result. 
context based search ( for QA systems and browsers)
This uses machine learning techniques to empower searches in browsers and QA system as it relates the
articles as most related and ranks them works based upon tf-idf method 
XO game
It uses an Ai algorithm written to analyse the situation and plays it's move automatically 
Messaging app(java)
It is unique from present traditional messengers as it is server less and delivers messages fast and secure.
Choclate gallery(simple website)
It is a simple choclate theme based website made using html,CSS and javascript,that gives the visitor the feel of
eating an virtual choclate 
https://wondrous-sherbet-6366df.netlify.app/
Achievements & Awards
2⭐ rated in codechef"""

def parse_questions(string):
    questions = re.split(r'\*\*Question \d+:\*\*', string)[1:]
    question_list = []

    for question in questions:
        lines = question.strip().split('\n')
        
        question_text = lines[0].strip()
        choices = {}
        answer = None
        
        for line in lines[1:]:
          
            match = re.match(r'\((.)\) (.*)', line.strip())
            if match:
                choice, text = match.groups()
                choices[choice] = text
            elif line.startswith('**Answer:'):
                answer = line.split()[-1]
        
       
        question_dict = {
            'question': question_text,
            'choices': choices,
            'answer': answer
        }
        
       
        question_list.append(question_dict)

    return question_list


def parse_skills(skill_string):
    
    lines = skill_string.split('\n')
   
    skills = []
    for line in lines:
        
        line = line.strip()
       
        skill = re.sub(r'^\d+\)\s*', '', line)
       
        if skill:
            skills.append(skill)
    return skills

   


genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel("gemini-pro")
prompt = """Generate 5 mcqs on python such that each question contains 4 options and 1 answers , these questions are for intermediate python programmers """
#response = model.generate_content(prompt)

prompt1 = """you are a human resource manager and should extract skills form the given resume text and reutrn them in the below format

            format : 
               1) skill1
               2) skill2
               3) skill3
               4) skill4
               5) skill5
               and so on... 
               here is the resume data """ + resume_text + """
               use this data to extract skills"""

response = model.generate_content(prompt1)
print(response.text)
print("================================================================================================================================")
print(parse_skills(response.text))
