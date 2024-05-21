import os

import google.generativeai as genai
from mdb import get_user_data , update_inter_chat





def interview_engine(user_query , history , username , role):
        
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


        generation_config = {
          "temperature": 1,
          "top_p": 0.95,
          "top_k": 64,
          "max_output_tokens": 8192,
          "response_mime_type": "text/plain",
        }

        safety_settings = [
            {
              "category": "HARM_CATEGORY_HARASSMENT",
              "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
              "category": "HARM_CATEGORY_HATE_SPEECH",
              "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
              "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
              "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
              "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
              "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
          ]

   
        model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        safety_settings=safety_settings,
        generation_config=generation_config,
        system_instruction=f"you are an AI interviewer taking interview for the role {role} \nhere are the details you should grab :\n1) experience\n2)his logical thinking\n3) Technical skill\n4) Intrest to work on the role\nafter grabbing all the details you should tell him to end the interview",
        )

        chat_session = model.start_chat(history = [])


        response = chat_session.send_message(user_query)
          
        history_status = update_inter_chat(username , chat_session._history) 
        return response.text 
