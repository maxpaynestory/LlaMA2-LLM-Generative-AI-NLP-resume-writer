import os

from PyPDF2 import PdfReader
from langchain.chains import LLMChain
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate

from helpers import scrape_jd_from_url

MODEL_PATH = "D:\\llm-models\\TheBloke\\Llama-2-7b-Chat-GGUF\\llama-2-7b-chat.Q8_0.gguf"

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
DEFAULT_SYSTEM_PROMPT = """You are a professional resume writer.
                        Your goal is to help people and create a customized resume according to the job Ad requirements.
                        Divide resume into sections: Full name, Contact Information, Address, Social links, Objective Statement, Skills, Experiences, Education."""


def load_model():
    llm = LlamaCpp(
        model_path=MODEL_PATH,
        n_threads=4,
        temperature=0.5,
        max_tokens=5000,
        top_p=0.95,
        verbose=False,  # Verbose is required to pass to the callback manager
        n_ctx=4090
    )
    instruction = "User: {user_input} \n\nAI:"
    template = get_prompt(instruction)
    prompt = PromptTemplate(
        input_variables=["user_input"], template=template
    )
    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
    )
    return llm_chain


def get_prompt(instruction, new_system_prompt=DEFAULT_SYSTEM_PROMPT):
    system_prompt = B_SYS + new_system_prompt + E_SYS
    prompt_template = B_INST + system_prompt + instruction + E_INST
    return prompt_template


def resume_to_job(pdf_resume_path, job_ad_url, session, llm_chain):
    jd = scrape_jd_from_url(job_ad_url)
    jd_file_path = os.path.join('sessions', session, 'jd.txt')
    with open(jd_file_path, "w", encoding="utf-8") as f:
        f.write(jd)
        f.close()

    user_input = "This is my resume\n\n"
    reader = PdfReader(pdf_resume_path)
    for i in range(len(reader.pages)):
        page = reader.getPage(i)
        user_input += page.extractText() + "\n\n"
    user_input += "Here is the job Ad that i want to apply for\n\n" + jd
    new_resume = llm_chain.predict(user_input=user_input)
    response_jd_file_path = os.path.join('sessions', session, 'response_resume.txt')
    with open(response_jd_file_path, "w", encoding="utf-8") as f1:
        f1.write(new_resume)
        f1.close()
    return new_resume