import os
import time
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from job_recommendation_prompt import prompt
from job_recommendation_user_preferences import user_preferences
from openai import OpenAI
from openai.types.chat import ChatCompletion
from pydantic import BaseModel, HttpUrl


class Job(BaseModel):
    position: str
    company_name: str
    company_url: Optional[HttpUrl] = None
    location: str
    posted_date: str


class JobScraper:
    BASE_URL = os.environ.get("JOB_POSITIONS_BASE_URL")

    def __init__(self, keywords: str, location: str):
        self.keywords = keywords
        self.location = location
        self.jobs: List[Job] = []
        self.openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), max_retries=4)
        self.system_prompt = prompt()
        self.user_preferences = user_preferences()
        self.model = "gpt-4o"
        self.upper_limit_job_index = 1000
        self.factor_job_index = 50
        self.retries = 5

    def fetch_jobs(self, start_index: int):
        params = {
            "keywords": self.keywords,
            "location": self.location,
            "start": start_index,
        }
        response = requests.get(self.BASE_URL, params=params, timeout=10)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 429:
            wait_time = 2**self.retries  # Exponential backoff
            print(f"Rate limit exceeded. Waiting for {wait_time} seconds...")
            time.sleep(wait_time)
            return self.fetch_jobs(start_index)
        else:
            response.raise_for_status()

    def parse_jobs(self, html_content: str):
        soup = BeautifulSoup(html_content, "html.parser")
        job_listings = soup.find_all("li")

        for job_listing in job_listings:
            # Job Position
            position_tag = job_listing.find("h3", class_="base-search-card__title")
            if not position_tag:
                continue
            position = position_tag.text.strip()

            # Company name and link
            company_tag = job_listing.find(
                "h4", class_="base-search-card__subtitle"
            ).find("a")
            company_name = company_tag.text.strip() if company_tag else "Unknown"
            company_url = (
                company_tag["href"]
                if company_tag and "href" in company_tag.attrs
                else None
            )

            # Location
            location_tag = job_listing.find("span", class_="job-search-card__location")
            location = location_tag.text.strip() if location_tag else "Unknown"

            # Posted Date
            posted_date_tag = job_listing.find(
                "time", class_="job-search-card__listdate"
            )
            posted_date = posted_date_tag.text.strip() if posted_date_tag else "Unknown"

            # Create a Job instance and add to the list
            job = Job(
                position=position,
                company_name=company_name,
                company_url=company_url,
                location=location,
                posted_date=posted_date,
            )
            self.jobs.append(job)

    def scrape(self):
        for start_index in range(0, self.upper_limit_job_index, self.factor_job_index):
            html_content = self.fetch_jobs(start_index)
            self.parse_jobs(html_content)
            time.sleep(1)

    def print_job_positions(self):
        for job in self.jobs:
            print(f"Position: {job.position}")
            print(f"Company: {job.company_name} ({job.company_url})")
            print(f"Location: {job.location}")
            print(f"Posted: {job.posted_date}")
            print("-" * 40)

    def jobs_to_string(self) -> str:
        return "\n\n".join(
            f"Position: {job.position}\n"
            f"Company: {job.company_name} ({job.company_url})\n"
            f"Location: {job.location}\n"
            f"Posted: {job.posted_date}"
            for job in self.jobs
        )

    def extract_chat_completion(self, completion: ChatCompletion):
        return completion.choices[0].message.content

    def generate_job_recommendations(self):
        completion_messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"USER PREFERENCES: {self.user_preferences}"},
            {"role": "user", "content": f"JOB POSITIONS: {self.jobs_to_string()}"},
        ]

        completion = self.openai.chat.completions.create(
            messages=completion_messages,
            model=self.model,
            temperature=0,
        )
        recommendation = self.extract_chat_completion(completion)
        print("RECOMMENDATIONS:\n\n")
        print(f"{recommendation}\n\n")


if __name__ == "__main__":
    scraper = JobScraper(keywords="Software Engineer", location="europe")
    scraper.scrape()
    scraper.generate_job_recommendations()
