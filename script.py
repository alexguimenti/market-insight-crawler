# site_summary.py

# === INITIAL CONFIGURATION ===
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import openai
import google.generativeai as genai
import re
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the URL of the site you want to analyze
TARGET_URL = "https://example.com/"

# Alternative between OpenAI and Gemini
LLM_PROVIDER = 'gemini'  # or 'openai'

# Production settings
REQUEST_TIMEOUT = 30  # seconds
MAX_CONTENT_SIZE = 50000  # characters per page
MAX_PAGES_TO_SCRAPE = 10  # limit number of pages

# Load API keys
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
gemini_api_key = os.getenv('GEMINI_API_KEY')

if LLM_PROVIDER == 'gemini':
    genai.configure(api_key=gemini_api_key)


# === SCRAPER ===
class WebScraper:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.title = None
        self.text = None
        self.links = []
        self.images = []
        self.full_content = None
        self.fetch_and_parse()

    def fetch_and_parse(self):
        try:
            # Add headers to mimic real browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(
                self.url, 
                timeout=REQUEST_TIMEOUT,
                headers=headers,
                allow_redirects=True
            )
            response.raise_for_status()
            
            # Check content size
            if len(response.text) > MAX_CONTENT_SIZE:
                logger.warning(f"Content too large for {self.url}: {len(response.text)} chars")
                response.text = response.text[:MAX_CONTENT_SIZE]
            
            self.soup = BeautifulSoup(response.text, 'html.parser')
            self.extract_content()
            
        except requests.Timeout:
            logger.error(f"Timeout fetching {self.url}")
            self.full_content = f"Title: Timeout Error\n\nText: Request timed out after {REQUEST_TIMEOUT} seconds\n\nLinks: []\n\nImages: []"
        except requests.RequestException as e:
            logger.error(f"Error fetching {self.url}: {e}")
            self.full_content = f"Title: Network Error\n\nText: Unable to fetch content: {str(e)}\n\nLinks: []\n\nImages: []"
        except Exception as e:
            logger.error(f"Unexpected error fetching {self.url}: {e}")
            self.full_content = f"Title: Error\n\nText: Unexpected error: {str(e)}\n\nLinks: []\n\nImages: []"

    def extract_content(self):
        if not self.soup:
            return
        
        try:
            self.title = self.soup.title.string.strip() if self.soup.title else "No title found"
            self.text = self.soup.get_text(separator=' ', strip=True)
            
            # Limit text size
            if len(self.text) > MAX_CONTENT_SIZE:
                self.text = self.text[:MAX_CONTENT_SIZE] + "... [truncated]"
            
            self.links = [urljoin(self.url, a['href']) for a in self.soup.find_all('a', href=True)]
            self.images = [urljoin(self.url, img['src']) for img in self.soup.find_all('img', src=True)]
            
            if self.text:
                self.full_content = f"Title: {self.title}\n\nText: {self.text}\n\nLinks: {self.links}\n\nImages: {self.images}"
            else:
                self.full_content = f"Title: {self.title}\n\nText: No readable content found\n\nLinks: {self.links}\n\nImages: {self.images}"
        except Exception as e:
            logger.error(f"Error extracting content from {self.url}: {e}")
            self.full_content = f"Title: Error extracting content\n\nText: Unable to extract content from this page\n\nLinks: []\n\nImages: []"


# === LINK CLASSIFICATION ===
def analyze_links_with_openai(links, site_domain):
    try:
        # Limit number of links to analyze
        if len(links) > 50:
            logger.warning(f"Too many links ({len(links)}), limiting to 50")
            links = links[:50]
        
        system_prompt = """
You are an LLM specialized in URL analysis. You will receive a list of links extracted from a website's homepage. Your task is to classify each link as Relevant or Not Relevant based only on the URL structure, without accessing the actual content of the pages.

Relevance Criteria:
- A link is Relevant if the URL indicates it belongs to the same domain and points to meaningful internal sections of the site.
- A link is Not Relevant if the URL suggests:
  - External domains (e.g., facebook.com, linkedin.com)
  - Legal, policy, or utility pages (/privacy, /cookies, /login, /terms, etc.)

Return the output in JSON format as a list of dictionaries, where each item contains:
- "url": the URL string
- "classification": either "Relevant" or "Not Relevant"
- "justification": a brief explanation

Respond with only the JSON, without any additional explanation or formatting.
"""
        user_prompt = f"Website domain: {site_domain}\nLinks:\n" + "\n".join(links)

        if LLM_PROVIDER == 'openai':
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
                timeout=60  # Add timeout for API calls
            )
            return response.choices[0].message.content

        elif LLM_PROVIDER == 'gemini':
            model = genai.GenerativeModel('gemini-2.5-flash')
            chat = model.start_chat()
            response = chat.send_message(f"System: {system_prompt}\n\nUser: {user_prompt}")
            return response.text
    except Exception as e:
        logger.error(f"Error analyzing links: {e}")
        return "[]"


def get_relevant_links_from_url(url):
    try:
        scraper = WebScraper(url)
        if not scraper.links:
            return []

        raw_response = analyze_links_with_openai(scraper.links, url)
        raw_response = raw_response.strip() if raw_response else ""

        if not raw_response:
            return []

        try:
            json_start = raw_response.find('[')
            json_end = raw_response.rfind(']') + 1
            cleaned_response = raw_response[json_start:json_end]
            json_response = json.loads(cleaned_response)
            links = [item["url"] for item in json_response if item.get("classification") == "Relevant"]
        except Exception:
            lines = raw_response.splitlines()
            links = []
            for line in lines:
                line = line.strip()
                if line.startswith("*") or line.startswith("-"):
                    match = re.search(r'https?://[^\s\)]+', line)
                    if match:
                        link = match.group(0).strip('`').strip()
                        links.append(link)

        # Remove duplicates and filter irrelevant domains
        seen = set()
        filtered_links = []
        excluded_domains = [
            "facebook.com", "twitter.com", "linkedin.com", "instagram.com",
            "youtube.com", "news.ycombinator.com", "patents.google.com"
        ]

        for link in links:
            cleaned_link = link.strip('`').strip()
            domain = urlparse(cleaned_link).netloc
            if not any(ex in domain for ex in excluded_domains):
                if cleaned_link not in seen:
                    seen.add(cleaned_link)
                    filtered_links.append(cleaned_link)

        # Limit number of pages to scrape
        if len(filtered_links) > MAX_PAGES_TO_SCRAPE:
            logger.warning(f"Too many relevant links ({len(filtered_links)}), limiting to {MAX_PAGES_TO_SCRAPE}")
            filtered_links = filtered_links[:MAX_PAGES_TO_SCRAPE]

        return filtered_links
    except Exception as e:
        logger.error(f"Error getting relevant links from {url}: {e}")
        return []


# === CONTENT COLLECTION ===
def get_full_content_from_site(url):
    contents = []
    home_scraper = WebScraper(url)
    if home_scraper.full_content:
        contents.append({"url": url, "content": home_scraper.full_content})
    
    relevant_links = get_relevant_links_from_url(url)
    for link in relevant_links:
        try:
            page_scraper = WebScraper(link)
            if page_scraper.full_content:
                contents.append({"url": link, "content": page_scraper.full_content})
        except Exception as e:
            logger.error(f"Error scraping {link}: {e}")
    
    return contents


# === MARKDOWN SUMMARY ===
def summarize_company_from_site(url):
    try:
        MAX_CHARS_PER_PAGE = 2000
        content_data = get_full_content_from_site(url)
        
        # Check if we have any content to analyze
        if not content_data:
            print("## Error: No Content Found\n\nUnable to extract content from the provided URL. Please check if the URL is accessible and contains readable content.")
            return

        system_prompt = """
You are an expert language model trained in business intelligence. You will receive a collection of web page contents from a company's website, including the homepage and all pages deemed relevant based on their URL structure.

Your task is to analyze this content and generate a clear, structured summary of the company, with a focus on identifying information relevant to business development and commercial opportunities.

Your summary should include:
- Company Overview: mission, vision, positioning, and key messages.
- Products and Services: what the company offers and to whom.
- Target Audience or Market: who they are trying to serve.
- Value Proposition: what differentiates them.
- Use of Technology or Innovation (if applicable).
- Potential Business Opportunities: ideas for partnerships, sales, integrations, or use cases.

Use clear language and avoid quoting long excerpts from the site. You are not summarizing each page, but synthesizing the information into actionable insights.

Do not speculate beyond what is supported by the content. If some information is unclear or missing, note it as a limitation.

**Format your entire response using Markdown (## headings, bullet points, etc.).**
"""

        user_prompt = "Here is the content extracted from the website:\n\n"
        for entry in content_data:
            if entry.get('content'):
                truncated = entry['content'][:MAX_CHARS_PER_PAGE]
                user_prompt += f"URL: {entry['url']}\nCONTENT:\n{truncated}\n\n"

        if LLM_PROVIDER == 'openai':
            client = openai.OpenAI()
            stream = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                stream=True,
                timeout=120  # 2 minutes timeout for streaming
            )
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end="", flush=True)

        elif LLM_PROVIDER == 'gemini':
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(
                f"System: {system_prompt}\n\nUser: {user_prompt}",
                stream=True
            )
            for chunk in response:
                if chunk.text:
                    print(chunk.text, end="", flush=True)
    
    except Exception as e:
        print(f"## Error: Analysis Failed\n\nAn error occurred during the analysis: {str(e)}\n\nPlease check the URL and try again.")


# === FINAL EXECUTION ===
if __name__ == "__main__":
    summary = summarize_company_from_site(TARGET_URL)
    print(summary)

