# Market Insight Crawler

A Python tool that uses web scraping and language models (OpenAI or Gemini) to extract and summarize business insights from any public website.

## 🚀 Features

- 🌐 **Modern Web Interface**: Flask interface with minimalist and responsive design  
- 🤖 **Intelligent Analysis**: Uses OpenAI or Gemini to classify relevant links  
- 🧠 **Business Summary**: Generates summaries focused on commercial opportunities  
- 📝 **Markdown Output**: Structured and readable analysis  
- ⚡ **Real-time Streaming**: LLM responses in real-time  
- 🔄 **Dynamic URL**: Interface allows analyzing any URL without editing code  
- 🛡️ **Production Ready**: Optimized for deployment with timeouts and error handling

## 🎯 Project Goal

This project explores how simple LLM calls—when well-structured with carefully designed prompts—can simulate the behavior of intelligent agents without requiring complex frameworks like LangChain, CrewAI, or AutoGen.

By chaining steps such as link extraction, filtering, and content summarization, the tool mimics agent-like planning and reasoning while keeping the code clean and maintainable.

## 🛠️ Technologies Used

- **Backend**: Python 3.10+, Flask  
- **Frontend**: HTML5, CSS3, JavaScript  
- **Web Scraping**: BeautifulSoup4, Requests  
- **LLMs**: OpenAI API, Google Gemini  
- **Configuration**: dotenv  
- **Production**: Gunicorn, WSGI

## 📦 Installation

```bash
git clone https://github.com/yourusername/market-insight-crawler.git
cd market-insight-crawler
pip install -r requirements.txt
```

## 🔐 Environment Variables

Create a `.env` file with:

```env
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
LLM_PROVIDER=gemini  # or openai
FLASK_ENV=development  # or production
```

## ⚙️ Usage

### Development

```bash
python app.py
```

Access `http://localhost:5000` in your browser.

### Production

```bash
# Using Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app

# Or using the Procfile (Heroku/Railway)
# Procfile is already configured
```

### Command Line

Edit the `TARGET_URL` in `script.py` and run:

```bash
python script.py
```

## 🚀 Production Deployment

### Environment Configuration

Set these environment variables for production:

```env
FLASK_ENV=production
LLM_PROVIDER=gemini
OPENAI_API_KEY=your_key
GEMINI_API_KEY=your_key
PORT=5000
WORKERS=4
```

### Platform-Specific Deploy

#### Heroku
```bash
heroku create your-app-name
heroku config:set FLASK_ENV=production
git push heroku main
```

#### Railway
```bash
railway login
railway init
railway up
```

#### DigitalOcean App Platform
- Connect your GitHub repo
- Set environment variables
- Deploy automatically

### Production Considerations

- **Timeouts**: Configured for 3-5 minute limits
- **Memory**: Limited to 512MB-1GB per request
- **Rate Limiting**: Implemented to prevent abuse
- **Error Handling**: Graceful degradation on failures
- **Logging**: Structured logging for monitoring

## 🎨 Web Interface

The web interface offers:

- **Modern Design**: Gradients, blur effects and smooth animations  
- **Responsive**: Works on desktop and mobile  
- **Visual Feedback**: Loading spinners and progress bars  
- **Validation**: Automatically adds `https://` if needed  
- **Formatted Results**: Displays analysis in Markdown with syntax highlighting  
- **Error Handling**: Graceful error messages and retry options

## 💡 Use Cases

- **Market Intelligence**: Competitor analysis  
- **Opportunity Discovery**: B2B lead identification  
- **CRM Enrichment**: Structured data about companies  
- **Competitive Analysis**: Positioning comparison  

## 🧩 Future Enhancements

- Export summary to `.md` or `.pdf`  
- Integrate with LangChain or CrewAI  
- Add support for sitemap parsing  
- Compare differences between competitor sites  
- Analysis history  
- Advanced scraping configurations  

## 📄 License

MIT License. Free to fork and adapt!
