import requests
import html2text
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from fastapi import UploadFile
import os
import aiofiles


async def create_session_data(session: str, my_resume: UploadFile) -> str:
    session_folder = os.path.join("sessions", session)
    if os.path.exists(session_folder) is not True:
        os.mkdir(session_folder)
    resume_path = os.path.join(session_folder, my_resume.filename)
    async with aiofiles.open(resume_path, 'wb') as out_file:
        content = await my_resume.read()
        await out_file.write(content)
    return resume_path


async def scrape_jd_from_url(job_ad_url, browser_page):
    parsed_url = urlparse(job_ad_url)
    await browser_page.goto(job_ad_url)
    content = await browser_page.content()
    soup = BeautifulSoup(content, "html.parser")
    jd = ''
    if parsed_url.netloc == "join.com":
        job_title = soup.select("div.GRRGN")[0].prettify()
        job_description = soup.select("div.dPvsCO")[0].prettify()
        jd = html2text.html2text(job_title + job_description)
    elif parsed_url.netloc == "www.linkedin.com":
        job_title = soup.select("h1.topcard__title")[0].prettify()
        job_description = soup.select("div.description__text")[0].prettify()
        jd = html2text.html2text(job_title + job_description)
    elif parsed_url.netloc.endswith("indeed.com") is True:
        job_title = soup.select("h1")[0].prettify()
        job_description = soup.find(id="jobDescriptionText").prettify()
        jd = html2text.html2text(job_title + job_description)
    return jd
