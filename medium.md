# Simulating Agents with Simple LLM Calls: Building a Website Intelligence Tool with Python

## Introduction

What if you could simulate the reasoning capabilities of AI agents without complex frameworks like LangChain or AutoGen? What if a handful of carefully structured LLM calls could behave like a purpose-driven agent?

This project explores exactly that: using basic Python, web scraping, and large language models (LLMs) to analyze a website and generate a structured business summary—just like a human analyst or a lightweight autonomous agent would.

---

## Project Overview

**Market Insight Crawler** is a Python-based tool designed to crawl the homepage of any public website, extract internal links, and use an LLM (OpenAI or Gemini) to:

- Identify relevant pages
- Collect textual content
- Summarize the company's mission, products, market, and business opportunities

The final output is a clean, structured Markdown report that can support sales, market research, competitive analysis, or even CRM enrichment.

**But here's the twist**: We've wrapped this intelligence in a **modern, responsive web interface** that makes it accessible to anyone—no coding required.

---

## The Goal

This project was born from a simple idea: **can we simulate agent-like behavior using only LLM calls, prompt design, and modular logic?**

By chaining operations like:

1. Extracting and filtering internal links
2. Parsing and aggregating page content
3. Sending that content to an LLM for summary generation

…we effectively **simulate planning, tool use, and reasoning** without a full agent architecture.

And then we made it **accessible to everyone** through a beautiful web interface.

---

## Tech Stack

### Backend
- **Python 3.10+**
- **Flask** for the web server
- `requests` and `BeautifulSoup4` for scraping
- `dotenv` for managing API keys
- `openai` and `google.generativeai` for LLM interaction
- Optional streaming support for real-time output

### Frontend
- **HTML5, CSS3, JavaScript** for the interface
- **Modern design** with gradients, blur effects, and smooth animations
- **Responsive layout** that works on desktop and mobile
- **Real-time feedback** with loading spinners and progress bars

### Supported LLMs
- GPT-4 (via OpenAI)
- Gemini 1.5 Flash (via Google Generative AI)

---

## Architecture: From Script to Web App

### The Core Script (`script.py`)

The heart of our intelligence system remains a clean, modular Python script:

#### 1. **Homepage Scraping**

We begin by loading the target homepage and extracting all `<a>` and `<img>` tags. This gives us the raw content and potential navigation paths.

#### 2. **Link Classification with LLM**

We pass the list of links to the LLM with a system prompt like:

> "You are an LLM specialized in URL analysis. Classify each link as 'Relevant' or 'Not Relevant' based on the domain and URL structure..."

This allows the LLM to filter out cookie policies, login pages, or external links.

#### 3. **Content Aggregation**

We scrape the homepage and each relevant internal link, aggregating the `title`, `text`, and `metadata` into a unified content object.

#### 4. **Summary Generation via LLM**

With the full content assembled, we ask the LLM to generate a **business-oriented summary** in Markdown. The prompt instructs it to identify:

- Mission and vision
- Products and services
- Target market
- Value proposition
- Technology and innovation
- Business opportunities

### The Web Interface (`app.py` + `templates/index.html`)

We wrapped this intelligence in a **Flask web application** that provides:

#### **Modern, Minimalist Design**
- Gradient backgrounds and glass-morphism effects
- Smooth animations and hover states
- Responsive design that works on any device

#### **Intelligent URL Handling**
- Automatic `https://` addition
- Real-time validation
- User-friendly error messages

#### **Real-time Streaming**
- Watch the analysis being generated live
- Progress indicators and status updates
- Formatted Markdown output with syntax highlighting

#### **Zero Configuration**
- No need to edit code or configure URLs
- Just enter any website URL and click "Analyze"
- Results displayed in a clean, scrollable format

---

## How It Works: The Complete Flow

### 1. **User Experience**
```
User enters URL → Clicks "Analyze" → Watches real-time analysis → Gets structured report
```

### 2. **Backend Processing**
```
Flask receives URL → Calls script.py functions → LLM processes content → Streams results back
```

### 3. **Intelligence Pipeline**
```
Web scraping → Link classification → Content aggregation → Business summary
```

---

## Streaming Output

Both OpenAI and Gemini support streaming responses, which we integrate for real-time feedback as the summary is being generated—improving usability and responsiveness.

The web interface captures this streaming output and displays it to the user in real-time, creating an engaging experience where you can watch the AI "think" as it analyzes the website.

---

## Why It Matters

This project demonstrates a powerful principle: **LLMs are capable of agent-like behavior** when you:

- Structure your pipeline modularly
- Design system and user prompts with care
- Think in terms of reasoning and context windows
- **Make it accessible to non-technical users**

It's a minimalist, interpretable, and maintainable way to build AI-powered workflows—ideal for prototyping or production use in resource-constrained environments.

### **The Democratization of AI**

By wrapping complex LLM operations in a simple web interface, we've made powerful business intelligence accessible to:

- Sales teams doing client research
- Marketing teams analyzing competitors
- Founders scouting opportunities
- Anyone who needs to understand a company quickly

---

## Example Use Cases

- **Sales teams** doing research on potential clients
- **Market analysts** exploring competitive positioning
- **Founders** scouting partnership opportunities
- **CRM enrichment** bots for internal company data
- **Business development** teams identifying opportunities
- **Competitive intelligence** gathering

---

## Getting Started

### Installation
```bash
git clone https://github.com/yourusername/market-insight-crawler.git
cd market-insight-crawler
pip install -r requirements.txt
```

### Configuration
Create a `.env` file with your API keys:
```env
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
```

### Running the Application
```bash
python app.py
```

Then visit `http://localhost:5000` in your browser and start analyzing websites!

---

## What's Next?

Some ideas for expanding this project:

- **Export functionality**: Save reports as PDF or Markdown files
- **Batch processing**: Analyze multiple websites at once
- **Integration**: Connect to LangChain or CrewAI for orchestration
- **Advanced crawling**: Add support for sitemap parsing
- **Competitive analysis**: Compare multiple competitors side-by-side
- **Historical tracking**: Store and compare analyses over time
- **API endpoints**: Make the intelligence available via REST API

---

## The Code Philosophy

This project embodies several important principles:

### **Simplicity Over Complexity**
We chose simple LLM calls over complex agent frameworks, making the code easy to understand and modify.

### **Modularity**
Each function has a single responsibility, making the system easy to extend and debug.

### **User-Centric Design**
The web interface makes powerful AI accessible to non-technical users.

### **Maintainability**
Clean, well-documented code that can be easily adapted for different use cases.

---

## Conclusion

You don't always need a full agent framework to get intelligent behavior from LLMs. With thoughtful prompt design and modular thinking, **LLM calls can become your agents.**

And when you wrap that intelligence in a beautiful, accessible interface, you create tools that can transform how people work with AI.

The combination of **powerful LLM intelligence** with **simple, elegant interfaces** is the future of AI applications. This project shows how to build that future, one website analysis at a time.

If you'd like to try the project yourself, check out the [GitHub repository](https://github.com/yourusername/market-insight-crawler).

---

## 🧠 Questions or Feedback?

Feel free to leave a comment or fork the repo to adapt it to your own use case! The beauty of this approach is its simplicity—you can easily modify the prompts, add new features, or integrate it into your own workflows.

---

*This project demonstrates that sometimes the most powerful AI applications are the ones that make complex intelligence accessible through simple, beautiful interfaces.* 
