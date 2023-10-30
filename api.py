from typing import Annotated
from fastapi import FastAPI, APIRouter, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from llama_cpu import load_model, resume_to_job
from helpers import create_session_data
import os

app = FastAPI()
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
router = APIRouter()

if os.path.exists("sessions") is not True:
    os.mkdir('sessions')

app.llm_chain = load_model()


@router.post("/convert")
async def convert_resume(my_resume: UploadFile, job_ad_url: Annotated[str, Form()], session: Annotated[str, Form()]):
    resume_path = await create_session_data(session, my_resume)
    new_resume = resume_to_job(resume_path, job_ad_url, session, app.llm_chain)
    return {"newResume": new_resume}


app.include_router(router, prefix="/api")
