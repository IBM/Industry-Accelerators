#Sample Materials, provided under license.
#Licensed Materials - Property of IBM.
#© Copyright IBM Corp. 2024,2025. All Rights Reserved.
#US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP Schedule Contract with IBM Corp.

#The Python Imaging Library (PIL) is
#
#    Copyright © 1997-2011 by Secret Labs AB
#    Copyright © 1995-2011 by Fredrik Lundh and contributors
#
#Pillow is the friendly PIL fork. It is
#
#    Copyright © 2010-2024 by Jeffrey A. Clark and contributors

import streamlit as st
from pydantic import BaseModel
import requests
import time
import uuid
import re
import base64

from dotenv import dotenv_values, find_dotenv

server_config = dotenv_values(find_dotenv())

#######################
#theme configuration
dashboard_theme= {
    "theme.base": "light",
    "theme.backgroundColor": "#F4F4F4",
    "theme.primaryColor": "#5591f5",
    "theme.secondaryBackgroundColor": "#D1D1D1",
    "theme.textColor": "#0a1464"
}

for theme_key, theme_val in dashboard_theme.items(): 
    if theme_key.startswith("theme"): st._config.set_option(theme_key, theme_val)

# read default RAG function credentials from environment
if 'QNA_RAG_DEPLOYMENT_URL' in server_config:
    try:
        QNA_RAG_DEPLOYMENT_URL = server_config['QNA_RAG_DEPLOYMENT_URL']
        if "/ai_service?" in QNA_RAG_DEPLOYMENT_URL:
            print("using QnA RAG 2.x based deployment")
            QNA_DEPLOYMENT_VERSION="2.0"
        else: 
            print("using QnA RAG 1.x based deployment")
            QNA_DEPLOYMENT_VERSION="1.x"
    except:
        QNA_RAG_DEPLOYMENT_URL = ''

if 'QNA_RAG_ENV_TYPE' in server_config:
    try:
        QNA_RAG_ENV_TYPE = server_config['QNA_RAG_ENV_TYPE']
    except:
        QNA_RAG_ENV_TYPE = ''

if 'QNA_RAG_SAAS_IAM_APIKEY' in server_config:
    try:
        QNA_RAG_SAAS_IAM_APIKEY = server_config['QNA_RAG_SAAS_IAM_APIKEY']
    except:
        QNA_RAG_SAAS_IAM_APIKEY = ''

if 'QNA_RAG_ONPREM_CPD_USERNAME' in server_config:
    try:
        QNA_RAG_ONPREM_CPD_USERNAME = server_config['QNA_RAG_ONPREM_CPD_USERNAME']
    except:
        QNA_RAG_ONPREM_CPD_USERNAME = ''

if 'QNA_RAG_ONPREM_CPD_APIKEY' in server_config:
    try:
        QNA_RAG_ONPREM_CPD_APIKEY = server_config['QNA_RAG_ONPREM_CPD_APIKEY']
    except:
        QNA_RAG_ONPREM_CPD_APIKEY = ''

# set expert recommendation
if 'ENABLE_EXPERT_RECOMMENDATION' in server_config:
    try:
        EXPERT_RECOMMENDATION= ( True if server_config['ENABLE_EXPERT_RECOMMENDATION'].lower() == "true" else False)
    except:
        EXPERT_RECOMMENDATION = False

# set sample expert recommendation
sample_recommendation=""
if 'IS_EXPERT_SAMPLE' in server_config:
    try:
        sample_recommendation= ( "This is synthetic expert profile generated using watsonx.ai." if server_config['IS_EXPERT_SAMPLE'].lower() == "true" else "")
    except:
        sample_recommendation = ''

feedback_expert_text=""
if EXPERT_RECOMMENDATION: 
    feedback_expert_text="If you want to know better answer for this question, Please click on above expert recommendation! \n Otherwise post your next question. "


# model for single chat message
class msg_entry(BaseModel):
    id: str
    role: str = 'assistant'
    text: str = 'write'
    documents: list[dict] = []
    show_documents: bool = False
    log_id: str = ''
    rating_options: int = 5

# retrieve and cache IAM access token
AccessToken = ''
AccessTokenExpires = 0
def get_token(force=False):
    global AccessToken, AccessTokenExpires
    now = time.time()
    if AccessTokenExpires <= now or force:

        if QNA_RAG_ENV_TYPE == "saas":
            if not QNA_RAG_SAAS_IAM_APIKEY or not QNA_RAG_DEPLOYMENT_URL:
                st.error("Please provide RAG function credentials for watsonx.ai aas")
                return ''
            # get access token for watsonx.ai SaaS 
            response = requests.post('https://iam.cloud.ibm.com/identity/token', data={'apikey': QNA_RAG_SAAS_IAM_APIKEY, 'grant_type': 'urn:ibm:params:oauth:grant-type:apikey'})
            if response.status_code == 200:
                resp = response.json()
                if not 'access_token' in resp:
                    st.error("Unexpected token format.")
                    return ''
            
                AccessToken = resp['access_token']
                # calculate expiration time (as a precaution, subtract 5 minutes)
                AccessTokenExpires = ( now + resp['expires_in'] if 'expires_in' in resp else ( resp['expiration'] if 'expiration' in resp else now ) ) - 300
        else:
            st.error("QNA_RAG_ENV_TYPE as on-prem or saas only supported")
            return ''

    return AccessToken


# call RAG function
def exec_request(payload, qna_url, ignore_errors=False ):
    header={}
    if QNA_RAG_ENV_TYPE == "on-prem":
        if not QNA_RAG_ONPREM_CPD_USERNAME or not QNA_RAG_ONPREM_CPD_APIKEY or not QNA_RAG_DEPLOYMENT_URL:
            st.error("Please provide all credentials required for watsonx.ai on-prem")
            return ''
        # get access token for watsonx.ai On Prem
        user_pass_string=QNA_RAG_ONPREM_CPD_USERNAME+ ':' +  QNA_RAG_ONPREM_CPD_APIKEY
        AccessToken=base64.b64encode(user_pass_string.encode()).decode()
        header={'Content-Type': 'application/json', 'Authorization': 'ZenApiKey '+AccessToken}
    else:
        header = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Bearer '+get_token()}
    status_code = 0
    try:
        response = requests.post(qna_url, json=payload, headers=header, verify=False)
        status_code = response.status_code
        if not status_code == 200 and not ignore_errors:
            st.error(f"Error with status code: {status_code}")
    except:
        st.error(f"Connecting RAG function failed.")
        response = None

    return response


# run RAG function to generate response
def get_response(prompt):
    qna_url=QNA_RAG_DEPLOYMENT_URL
    if QNA_DEPLOYMENT_VERSION=="1.x":
        
        response_scoring = exec_request({"input_data": [{"fields": ["Text"], "values": [[prompt]]}]}, qna_url)
        # extract response, source documents and log id
        if response_scoring == None:
            return 'I am not able to reply due to a technical issue..', [], ''
        
        response = response_scoring.json()
        text = response['predictions'][0]['values'][0][0]['response']
        documents = response['predictions'][0]['values'][0][0].get('source_documents', [])
        log_id = response['predictions'][0]['values'][0][0].get('log_id', '')
    else:
        qna_url = QNA_RAG_DEPLOYMENT_URL.replace("/ai_service?", "/ai_service/qna?")
        response_scoring = exec_request({"question": prompt}, qna_url)
        # extract response, source documents and log id
        if response_scoring == None:
            return 'I am not able to reply due to a technical issue..', [], ''
        
        response = response_scoring.json()
        text = response['result']['response']
        documents = response['result'].get('source_documents', [])
        log_id = response['result'].get('log_id', '')
        
    return text, documents, log_id


# run RAG function to update feedback 
def send_feedback(log_id, value, comment=None):
    st.session_state.active = ''
    
    if not log_id == '':
        feedback_Value=int(value)
        if feedback_Value < 100 and comment == None:
            st.session_state.feedback = value
            st.session_state.log_id = log_id
            new_msg = msg_entry(id=str(uuid.uuid4()), role='assistant', text='Thanks for your feedback! Please add a comment in below input box.')
            st.session_state.history.append(new_msg)
            return None
        else:
            if QNA_DEPLOYMENT_VERSION=="1.x":
                qna_url=QNA_RAG_DEPLOYMENT_URL
                response_update = exec_request({"input_data": [{"fields": ["log_id", "value", "comment"], "values": [[log_id, value, comment if not comment == None else '']]}]}, qna_url)
                if feedback_Value < 100:
                    new_msg = msg_entry(id=str(uuid.uuid4()), role='assistant', \
                    text='Thanks! Feedback has been sent. \n'+ feedback_expert_text  if response_update.status_code == 200 and response_update.json()['predictions'][0]['values'][0][0] == 'ok' else 'Feedback update got failed' + feedback_expert_text)
                    st.session_state.expert_disabled=False
                    if EXPERT_RECOMMENDATION:
                        st.button('Recommended Expert for this question', 'expert_toggle'+new_msg.id, on_click=get_expert_recommendation, args=(log_id,),disabled=st.session_state.expert_disabled)
                else: 
                    new_msg = msg_entry(id=str(uuid.uuid4()), role='assistant', \
                    text='Thanks! Feedback has been sent. \n Type your next question in input box.' if response_update.status_code == 200 and response_update.json()['predictions'][0]['values'][0][0] == 'ok' else 'Feedback update got failed. Type your next Question in input box')
            else:
                qna_url = QNA_RAG_DEPLOYMENT_URL.replace("/ai_service?", "/ai_service/log_feedback?")
                response_update = exec_request({"log_id":log_id, "value":value, "comment":comment if not comment == None else ''}, qna_url)
                if feedback_Value < 100:
                    new_msg = msg_entry(id=str(uuid.uuid4()), role='assistant', \
                    text='Thanks! Feedback has been sent. \n'+ feedback_expert_text  if response_update.status_code == 200 and response_update.json()['status'] == 'ok' else 'Feedback update got failed' + feedback_expert_text)
                    st.session_state.expert_disabled=False
                    if EXPERT_RECOMMENDATION:
                        st.button('Recommended Expert for this question', 'expert_toggle'+new_msg.id, on_click=get_expert_recommendation, args=(log_id,),disabled=st.session_state.expert_disabled)
                else: 
                    new_msg = msg_entry(id=str(uuid.uuid4()), role='assistant', \
                    text='Thanks! Feedback has been sent. \n Type your next question in input box.' if response_update.status_code == 200 and response_update.json()['status'] == 'ok' else 'Feedback update got failed. Type your next Question in input box')          
            if comment == None:
                st.session_state.history.append(new_msg)
                return None
            else:
                return new_msg

# run RAG function to get expert recommendation 
def get_expert_recommendation(log_id):
    st.session_state.active = ''
    st.session_state.expert_recommendation = ''
    if not log_id == '':
        if QNA_DEPLOYMENT_VERSION=="1.x":
            qna_url=QNA_RAG_DEPLOYMENT_URL
            expert_response_update = exec_request({"input_data": [{"fields": ["_function", "log_id"], "values": [["recommend_top_experts", log_id]] }]}, qna_url)
            expert_msg = msg_entry(id=str(uuid.uuid4()), role='assistant', \
                text=str(sample_recommendation) + " Please contact below expert for more details." 
                + "\n \n **Name**: "+ expert_response_update.json()['predictions'][0]['values'][0][0][0]["name"]
                + ",\n \n **Email**: " + expert_response_update.json()['predictions'][0]['values'][0][0][0]["email"]
                + ",\n \n **Designation**: " + expert_response_update.json()['predictions'][0]['values'][0][0][0]["position"]
                + ",\n \n **Industry**: " + expert_response_update.json()['predictions'][0]['values'][0][0][0]["domain"]
                + ".\n \n Please type your next question in below input box!" if expert_response_update.status_code == 200 and 'expert_details' in expert_response_update.json()['predictions'][0]['values'][0][1] else "No Experts found on this topic, Please ask next Question!")
    
        else:
            qna_url = QNA_RAG_DEPLOYMENT_URL.replace("/ai_service?", "/ai_service/recommended_experts?")
            expert_response_update = exec_request({"log_id": log_id}, qna_url)
            expert_msg = msg_entry(id=str(uuid.uuid4()), role='assistant', \
                text=str(sample_recommendation) + " Please contact below expert for more details." 
                + "\n \n **Name**: "+ expert_response_update.json()['recommended_top_experts'][0]["name"]
                + ",\n \n **Email**: " + expert_response_update.json()['recommended_top_experts'][0]["email"]
                + ",\n \n **Designation**: " + expert_response_update.json()['recommended_top_experts'][0]["position"]
                + ",\n \n **Industry**: " + expert_response_update.json()['recommended_top_experts'][0]["domain"]
                + ".\n \n Please type your next question in below input box!" if expert_response_update.status_code == 200 and 'expert_details' in expert_response_update.json()['expert_status'] else "No Experts found on this topic, Please ask next Question!")
   
        # text='Please contact expert '+response_update.json()['predictions'][0]['values'][0][0][0]["name"] + ' , Email id: '+ response_update.json()['predictions'][0]['values'][0][0][0]["email"] + 'Profile Info: '+ response_update.json()['predictions'][0]['values'][0][0][0]["text"] if response_update.status_code == 200 and response_update.json()['predictions'][0]['values'][0][1] == 'expert_details retrieved from log records' else 'No Experts found on this topic')
        st.session_state.expert_disabled=True
        st.session_state.history.append(expert_msg)
        
    return None

# ping RAG function
def ping():
    qna_url=QNA_RAG_DEPLOYMENT_URL
    if QNA_DEPLOYMENT_VERSION=="1.x":
        default_payload={"input_data": [{"fields": [""], "values": [[""]] }]}
    else:
        default_payload={"":""}
    response_ping = exec_request(default_payload, qna_url, ignore_errors=True)
    status_code = response_ping.status_code if not response_ping == None else 0
    if not status_code == 200:
        return False, status_code 
    return  True, status_code


def get_msg_by_id(id):
    if not 'history' in st.session_state:
        return None
    hits = [index for index in range(len(st.session_state.history)) if st.session_state.history[index].id == id]
    return st.session_state.history[hits[0]] if len(hits) > 0 else None

# toggle displaying documents in chat message
def show_hide_documents(id):
    hits = [index for index in range(len(st.session_state.history)) if st.session_state.history[index].id == id]
    if len(hits) > 0:
        st.session_state.history[hits[0]].show_documents = not st.session_state.history[hits[0]].show_documents


# print single chat message
def print_message(msg: msg_entry, save=False):
    with st.chat_message(msg.role):
        st.markdown(msg.text)
        if msg.show_documents:
            m = f''
            if len(msg.documents) > 0:
                m = f'{m}<table><thead><th>Title/Source</th><th style="text-align: center;">Document</th></thead><tbody>'
                
                for d in msg.documents:
                    m = f'{m}<tr><td><a href="{d["metadata"]["document_url"]}">{d["metadata"]["title"]}</a></td><td style="text-align: left;">{d["page_content"]}</td></tr>'
                
                m = f'{m}</tbody></table><br><br><hr>'
            else:
                m = f'{m}No documents were used.'
            st.markdown(m,unsafe_allow_html=True)
        if not msg.log_id == '':
            disabled = not msg.id == st.session_state.active
            st.session_state.expert_disabled = True
            cols = st.columns([1 for _ in range(msg.rating_options)] + [9 - msg.rating_options])
            #                0      1      2     3      4    5-ok    6     7      8
            options_list = ['👎', '👍', '😡', '😠', '🙁', '😐', '🙂', '😀', '🤩']
            options_selector = [[0,1],[3,5,7],[2,3,7,8],[2,3,5,7,8]]
            for _i in range(msg.rating_options-1, -1, -1):
                cols[msg.rating_options-_i-1].button(options_list[options_selector[msg.rating_options-2][_i]], f"opt{str(_i)}{msg.id}", \
                                on_click=send_feedback, args=(msg.log_id,str(round(100*(_i/(msg.rating_options-1)))),), disabled=disabled)
            st.button(('Hide' if msg.show_documents else 'Show') + ' source documents', 'toggle'+msg.id, on_click=show_hide_documents, args=(msg.id,))
    if save:
        st.session_state.history.append(msg)



##########################################################################################
## Refresh page

# feedback value to be sent after comment imput
if not 'feedback' in st.session_state:
    st.session_state.feedback = ''

# current log id
if not 'log_id' in st.session_state:
    st.session_state.log_id = ''

# msg id with active feedback buttons
if not 'active' in st.session_state:
    st.session_state.active = ''

# default feedback rating options
if not 'rating_options' in st.session_state:
    st.session_state.rating_options = int(server_config["FEEDBACK_RATING_OPTIONS"])

st.set_page_config(page_title='QnA with RAG Bot', layout = "wide")
st.title("Q&A with RAG interactive streamlit based UI app")
st.session_state.connection=False
#st.QNA_DEPLOYMENT_VERSION=QNA_DEPLOYMENT_VERSION

ok, status_code = ping()
if ok:
    st.session_state.connection=True
else:
    st.error(f"Connection test failed, status code: {str(status_code)}")
    st.session_state.connection=False

_sub_title_description , _reset_button = st.columns([0.85,0.15], gap="large")

if not st.session_state.connection:
    _sub_title_description.error("This dashboard cannot be generated! Please configure your app with deployment function properly! Contact Adminstrator")
    st.stop()
else:
    match = re.search(r'/deployments/([^/]*)/', QNA_RAG_DEPLOYMENT_URL)
    _sub_title_description.markdown("This is QnA chatbot - Retrieval Augmented Generation by calling deployment function "+ f"**{match.group(1)}**" + " of watsonx.ai " + QNA_RAG_ENV_TYPE )
    _sub_title_description.markdown(f"\nTo clear chat history, click on reset chat button on the right side." )

if _reset_button.button('Reset chat'):
    if 'history' in st.session_state:
        del st.session_state.history
        st.session_state.feedback = ''
        st.session_state.active = ''
        st.session_state.log_id = ''
        st.session_state.expert_disabled = True

# chat history (with welcome message)
if not 'history' in st.session_state:
    st.session_state.history = [msg_entry(id=str(uuid.uuid4()), role='assistant', \
        text="Hi there! I am a QnA chatbot, please type your question in below input box!")]

# user's input
if prompt := st.chat_input("Ask questions and share feedback comment in this same input box."):

    # print chat (all feedback buttons inactive)
    st.session_state.active = ''
    for _msg in st.session_state.history:
        print_message(_msg)

    new_msg = msg_entry(id=str(uuid.uuid4()), role='user', text=prompt)
    print_message(new_msg, save=True)

    if not st.session_state.feedback == '':
        # update feedback
        new_msg = send_feedback(st.session_state.log_id, st.session_state.feedback, prompt)
        st.session_state.feedback = ''
    #elif not st.session_state.recommendation == '':

    else:
        # run RAG function
        with st.spinner("Please wait, QnA chatbot is typing.."):
            text, documents, log_id = get_response(prompt)
            new_msg = msg_entry(id=str(uuid.uuid4()), role='assistant', text=text, documents=documents, log_id=log_id, rating_options=st.session_state.rating_options )

    st.session_state.active = new_msg.id if not new_msg.log_id == '' else ''
    print_message(new_msg, save=True)

else:
    # print chat (with active feedback button)
    for _msg in st.session_state.history:
        print_message(_msg)
