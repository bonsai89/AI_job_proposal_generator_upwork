import glob, os, openai, requests, time
from ner import get_client_name
from get_samples import *
import gradio as gr
import urllib.parse

openai.api_key = 'API_key'
def chatgpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                    {"role": "system", "content": "You are a freelancer in Upwork specialized in subtitling, captioning, translation, and so on."},
                    {"role": "user", "content": prompt},
                ],
            request_timeout=60
        )
        result = ''
        for choice in response.choices:
            result += choice.message.content
            
        if result == "":
            time.sleep(3)
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                        {"role": "system", "content": "You are a freelancer in Upwork specialized in subtitling, captioning, translation, and so on."},
                        {"role": "user", "content": prompt},
                    ],
                request_timeout=60
            )
            result = ''
            for choice in response.choices:
                result += choice.message.content
    except:
        time.sleep(3)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": "You are a freelancer in Upwork specialized in subtitling, captioning, translation, and so on."},
                    {"role": "user", "content": prompt},
                ],
            request_timeout=60
        )
        result = ''
        for choice in response.choices:
            result += choice.message.content
    return result

    
def generate_proposal(job_url):
    job_details = job_url
    #job_details = job_details + "\n" + "Skills and expertise required: " + output['expertise']
    
    print("Getting Client Name")
    client_name = "Client" #get_client_name(job_url)
    
    print("Generating Proposal")
    prompt = f"""
    Client's requirements:\n
    {job_details}\n\n
    For the above requirement, capture all the keywords and put them in this sentence format: "I am very interested in working on this [] project... I have expertise in ..."
    Do not mention you are a native speaker or your years of experience or you are a certified translator or rates or contact me. Not more than 35 words. You are an expert-level copy writer. 
    """
    
    first_para = chatgpt(prompt)
    time.sleep(2)

    job_types = ["translation and proofreading", "subtitling", "transcription", "none"]
    prompt = f"""
    Client's requirements:\n
    {job_details}\n\n
    What type of job does it fall under? {{{", ".join(job_types)}}}\n\n
    Just output the type name from the second bracket above
    """
    result = chatgpt(prompt).lower()
    if result == "none" or result not in job_types:
        result = ""
    else:
        result = result + " "

    optional_para = f"8+ years of Experience in translation & subtitling\n500+ Satisfied Customers \u2B50\u2B50\u2B50\u2B50\u2B50\nReady To Start Immediately\n\nhttps://www.upwork.com/freelancers/weavlog\n\n(I am available now, Let's have a quick chat)\n\nCreate your Subtitles with a Seasoned Expert with 8+ years of Experience in translation, Top Rated Plus on Upwork."
    second_para = f"Having more than 8 years of experience providing quality {result}services, I am confident in handling this project."
    print("Gathering Relevant Work Samples")
    samples_text = get_samples_text(job_details)
    proposal = f"{optional_para}\n\nDear {client_name},\n\n{first_para}\n\n{second_para}\n\nDon’t just take my word. Check my portfolio and client reviews.\n\n{samples_text}Looking forward to discussing this further with you over chat. I’m just a message away!\n\nBest Regards,\nNithilan"
    print("=== Generated Proposal ===\n")
    print(proposal)
    print("\n")

    proposal = proposal.replace("\"","")
    return proposal

job_url = gr.Textbox(label="Upwork Job Details:")
proposal_out = gr.Textbox(label="Generated Proposal")

iface = gr.Interface(fn=generate_proposal, 
                     inputs=job_url, 
                     outputs=proposal_out.style(show_copy_button=True),
                     title="Proposal Generator", enable_queue=True)
    
iface.launch()
