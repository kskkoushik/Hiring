from flask import Flask , render_template , request
import google.generativeai as genai
import os
import PyPDF2
import re
from mdb import add_data , get_user_data , update_score , update_proficiency , update_questions 
import smtplib
from flask_mail import Mail, Message
from email.mime.text import MIMEText



# Define the schema for the desired output
app = Flask(__name__)

# Create a Gemini model instance
genai.configure(api_key= "AIzaSyDXInMq_3VVc96niTrRjp2RLpWFhl_09mY")
model = genai.GenerativeModel("gemini-pro")


def genrate_questions(technology , level , number ):
   
    prompt = "Generate " + number + " mcqs on " + technology +" such that each question contains 4 options and 1 answers , these questions are for " + level + " " + technology + """ programmers and this is the format of the questions you should follow : 
**Question 1:**

Which of the following is NOT a method of the `argparse` module for parsing command-line arguments?

(A) `add_argument()`
(B) `parse_args()`
(C) `add_parser()`
(D) `get_args()`

**Answer: D**

**Question 2:**

What is the purpose of the `yield` keyword in a generator function?

(A) To pause the execution of the function and return the current value
(B) To iterate over a sequence of values
(C) To define a new variable within the function
(D) To terminate the execution of the function

**Answer: A**

**Question 3:**

Which of the following is a benefit of using decorators in Python?

(A) To add functionality to existing functions without modifying the source code
(B) To create new classes from existing classes
(C) To improve code readability
(D) To speed up program execution

**Answer: A**

**Question 4:**

What is the difference between a class and an object in Python?

(A) A class is a template for creating objects, while an object is an instance of a class.
(B) An object is a template for creating classes, while a class is an instance of an object.
(C) A class and an object are both the same thing.
(D) A class is a variable, while an object is a value.

**Answer: A**

**Question 5:**

Which of the following data structures is best suited for storing a list of unique elements?

(A) List
(B) Tuple
(C) Set
(D) Dictionary""" 
    response = model.generate_content(prompt)
    return response.text

def extract_skills(resume_text):
    
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
    return response.text    


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


def pdf_text_extractor(uploaded_file):
   
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ''
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            return text







def send_mail(username , mail_address):
    try:
        sender_email = "kskkoushik135@outlook.com"
        receiver_email = mail_address
        password = "KSKkoushik789..."

        message = MIMEText(f""" HIRE-AI Assesment Test \n
                           Click the following link to take the skill test: http://localhost:5000/skill_test/{username}
                            All the best """)
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = "Skill Test Invitation"

        # Establish a connection to the SMTP server
        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()  # Start TLS for security
            server.login(sender_email, password)  # Login to the server
            server.sendmail(sender_email, receiver_email, message.as_string())  # Send the email

        return("Email sent successfully")
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to send email")

def send_mail_score(username , mail_address ,score):
    try:
        sender_email = "kskkoushik135@outlook.com"
        receiver_email = mail_address
        password = "KSKkoushik789..."

        message = MIMEText(f""" HIRE-AI Assesment Test score \n
                            Dear ,{username} you scored {score} in the Hire-AI skill Assessment test
                            All the best """)
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = "Skill Test Invitation"

        # Establish a connection to the SMTP server
        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()  # Start TLS for security
            server.login(sender_email, password)  # Login to the server
            server.sendmail(sender_email, receiver_email, message.as_string())  # Send the email

        return("Email sent successfully")
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to send email")

def level_analyze(num):
    num = int(num)
    if num == 1:
        return "beginner"
    elif num == 2:
        return "intermediate"
    elif num == 3:
        return "advanced"
    else:
        return "expert"

      
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['POST'])
def get_data():
    questions_list = []
    name = request.form['name']
    mail = request.form['mail']
    resume = request.files['resume']
    resume_data = pdf_text_extractor(resume)
    skills = extract_skills(resume_data)
    list_skills = parse_skills(skills)

    status = add_data(name , mail , list_skills , questions_list)
    if status != "data added":
         return render_template('error_page.html')
    else :
        return render_template('proficiency.html' , skills = list_skills , name = name)

@app.route('/skill_test/<name>')
def test(name):
     
     user_data = get_user_data(name)
     questions = user_data['questions']    

     return render_template('test.html', questions=questions)


@app.route('/submit_test', methods=['POST'])
def result():
     
     user_name = request.form['default_value']
     user_data = get_user_data(user_name)
     email = user_data['email']
     questions = user_data['questions']
     score = 0
     i = 0
     for i in range(len(questions)):
          
          selected_answer = request.form.get(f'mcq-{i+1}')
          if questions[i]['answer'] == selected_answer:
               score = score+1

     score_status = update_score(user_name , score)
     if score_status == "score updated":
        score_mail = send_mail_score(user_name ,email , score)
        return render_template('congrats.html', score=score)

@app.route('/proficiency_data' , methods = ['POST'])
def add_proficiency_data():

    questions_list = []
    proficiency = []
    name = request.form['default_value']
    user = get_user_data(name)
    mail_address = user['email']
    list_skills = user['skills']
    i = 0
    for i in range(len(list_skills)):
        p = request.form[f'{i+1}']
        proficiency.append(p)                

    proficiency_status = update_proficiency(name , proficiency)
    user = get_user_data(name)
    i = 0
    for i in range(len(list_skills)):
         skill = list_skills[i]
         level = level_analyze(user['proficiency'][i])
         questions = (genrate_questions(skill , level , '2' ))
         questions_list.extend(parse_questions(questions))
    
    question_status = update_questions(name , questions_list)
    if proficiency_status == "proficiency updated":
        send_mail(name, mail_address)
        return render_template('success_email.html') 
    else:
        return render_template('error_page.html')         
          

if __name__ == '__main__':
    app.run(debug=True)