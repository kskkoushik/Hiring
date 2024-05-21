from flask import Flask , render_template , request , redirect , url_for
import google.generativeai as genai
import os
import PyPDF2
import re
from mdb import add_data , get_user_data , update_score , update_proficiency , update_questions , update_logic_questions , update_reason_questions , update_verbal_questions , update_l_score , update_r_score , update_v_score , get_all_data , update_inter_chat , add_job_posting
import smtplib
from flask_mail import Mail, Message
from email.mime.text import MIMEText
from interview import interview_engine



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

def genrate_questions_logical_test(number ):
   
    prompt = "Generate " + number + " mcqs on  such that each question contains 4 options and 1 answers , these questions are for analyzing logical capabilites of " + """ students and this is the format of the questions you should follow : 
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
(D) Dictionary



above given questions are sample questions you should provide questions to test logical capability of student without involving programming knowledge and using their critical thinking features """ 

    response = model.generate_content(prompt)
    return response.text

def genrate_questions_reasoning_test(number ):
   
    prompt = "Generate " + number + " mcqs on  such that each question contains 4 options and 1 answers , these questions are for analyzing reasoning and aptitude capabilites of " + """ students and this is the format of the questions you should follow : 
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
(D) Dictionary



above given questions are sample questions you should provide questions to test reasoning capability of student without involving programming knowledge and using their critical thinking features """ 

    response = model.generate_content(prompt)
    return response.text


def genrate_questions_verbal_test(number ):
   
    prompt = "Generate " + number + " mcqs on  such that each question contains 4 options and 1 answers , these questions are for analyzing verbal and speech capabilites of " + """ students and this is the format of the questions you should follow : 
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
(D) Dictionary



above given questions are sample questions you should provide questions to test verabl and speech capability of student without involving programming knowledge and using their english language grammar skills """ 

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

def send_mail_score(username , mail_address ,s_score , l_score , r_score , v_score ):
    try:
        sender_email = "kskkoushik135@outlook.com"
        receiver_email = mail_address
        password = "KSKkoushik789..."

        message = MIMEText(f""" HIRE-AI Assesment Test score \n
                            Dear ,{username} ,
                            Here is the score of your Hire-AI skill Assessment test \n
                            skill test - {s_score} \n
                            logical test - {l_score} \n
                            reasoning test - {r_score} \n
                            verbal test - {v_score} \n
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

def logic_redi(name):

    user = get_user_data(name)
    questions  = user['logic_quest']
    return redirect(url_for('logic_test', name=name))

def reason_redi(name):

    user = get_user_data(name)
    questions  = user['reason_quest']
    return redirect(url_for('reason_test', name=name))


def  verbal_redi(name):

    user = get_user_data(name)
    questions  = user['verbal_quest']
    return redirect(url_for('verbal_test', name=name))
    


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
def skill_test(name):
     
     user_data = get_user_data(name)
     questions = user_data['questions']    

     return render_template('test.html', questions=questions , test_type = 'skill')

@app.route('/logic_test/<name>')
def logic_test(name):
     
     user_data = get_user_data(name)
     questions = user_data['logic_quest']    

     return render_template('test.html', questions=questions , test_type = 'logic')

@app.route('/reason_test/<name>')
def reason_test(name):
     
     user_data = get_user_data(name)
     questions = user_data['reason_quest']    

     return render_template('test.html', questions=questions , test_type = 'reason')


@app.route('/verbal_test/<name>')
def verbal_test(name):
     
     user_data = get_user_data(name)
     questions = user_data['verbal_quest']    

     return render_template('test.html', questions=questions , test_type = 'verbal')


@app.route('/submit_test', methods=['POST'])
def result():
     
     user_name = request.form['default_value']
     user_data = get_user_data(user_name)
     test_type = request.form['test_type']
     email = user_data['email']

     if test_type == 'skill':
        questions = user_data['questions']
     elif test_type == 'logic':
         questions = user_data['logic_quest']
     elif test_type == 'reason':
         questions = user_data['reason_quest']
     else:
         questions = user_data['verbal_quest']           

    
     score = 0
     i = 0
     score_status = ''
     for i in range(len(questions)):
          
          selected_answer = request.form.get(f'mcq-{i+1}')
          if questions[i]['answer'] == selected_answer:
               score = score+1
     if test_type == 'skill':
        score_status = update_score(user_name , score)
     elif test_type == 'logic':
         score_status = update_l_score(user_name , score)   
     elif test_type == 'reason':
         score_status = update_r_score(user_name , score)
     else:
         score_status = update_v_score(user_name , score)    
     
     
     if score_status == "score updated" and test_type == 'skill':
        return logic_redi(user_name)
     elif score_status == "score updated" and test_type == 'logic':
        return reason_redi(user_name)
     elif score_status == "score updated" and test_type =='reason':
        return verbal_redi(user_name)  
     elif score_status == "score updated" and test_type == 'verbal':
       user_data = get_user_data(user_name)
       s_score  = user_data['s_score']
       l_score  = user_data['l_score']
       r_score  = user_data['r_score']
       v_score  = user_data['v_score']
       mail_status = send_mail_score(user_name , email , s_score ,l_score, r_score , v_score)
       if mail_status == 'Email sent successfully':
           return render_template('congrats.html')
       
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
    logical = genrate_questions_logical_test('1')
    reasoning = genrate_questions_reasoning_test('1')
    verbal = genrate_questions_logical_test('1')
    logic_li = parse_questions(logical)
    reason_li = parse_questions(reasoning)
    verb_li = parse_questions(verbal)
    l_status = update_logic_questions(name , logic_li)
    r_status = update_reason_questions(name , reason_li)
    v_status = update_verbal_questions(name , verb_li)
    if proficiency_status == "proficiency updated":
        send_mail(name, mail_address)
        return render_template('success_email.html') 
    else:
        return render_template('error_page.html')


@app.route('/interview/<role>/<username>')
def interview(role , username):
        return render_template('interview.html', response = 'start by greeting the AI' , username = username ,  role = role)
   

@app.route('/interview_submit' , methods=['POST'])
def interview_submit():
    username = request.form['username']
    role = request.form['role']
    user = get_user_data(username)
    history = user['inter_chat']
    input = request.form['input']
    response = interview_engine(input , history , username , role)
    return render_template('interview.html',  response = response, username = username , role = role)
        
@app.route('/adminstration/view_data/<password>')
def get_application_data(password):

    if password == 'hire_aiaz':
        data = get_all_data()
        return render_template('view_data.html', data = data)
    else:
        return render_template('error_page.html')

@app.route('/adminstration/job_posting/<password>')
def redirect_post_job(password):
    if password == 'hire_aiaz':
        return render_template('job_posting.html')
    else:
        return render_template('error_page.html')
    

@app.route('/add_job_to_db' , methods = ['POST'])
def job_post():
    title = request.form['title']
    description = request.form['description']
    skills = request.form['skills']
    job_post_status = add_job_posting(title, description , skills )
    if job_post_status == 'job added':
        return "Job post added successfully"  

if __name__ == '__main__':
    app.run(debug=True)