# Job Scraper

A Python-based **BeautifulSoup web scraper** that aggregates IT job postings from multiple Canadian job boards and uses AI to generate job description summaries. This command-line tool scrapes job listings from ITJobs.ca and TechTalent using BeautifulSoup and requests, then combines them into a structured JSON format for easy analysis.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Output](#output)
- [Troubleshooting](#troubleshooting)

---

## Overview

Job Scraper consists of three main Python scripts that work together to collect and process IT job postings:

1. **`main.py`**  
   - Orchestrates the scraping process by importing functions from both scrapers
   - Combines job data from multiple sources
   - Exports results to a single JSON file (`joblist.json`)

2. **`itjobs_data.py`**  
   - Scrapes job postings from [ITJobs.ca](https://www.itjobs.ca/) (pages 1-7)
   - Extracts: Position, Company, Location, and Description
   - Uses standard HTTP requests with user-agent rotation

3. **`techtalent_data.py`**  
   - Scrapes job postings from [TechTalent](https://jobs.techtalent.ca/)
   - Extracts: Position, Company, Location, and Job Description URL
   - Fetches full job descriptions with retry logic (up to 3 attempts)
   - Uses OpenAI's GPT-4 to generate concise summaries of job descriptions

---

## Features

- **Multi-Source Scraping**: Aggregates jobs from ITJobs.ca and TechTalent using BeautifulSoup HTML parsing
- **AI-Powered Summaries**: Uses OpenAI GPT-4 to summarize TechTalent job descriptions
- **Command-Line Tool**: Simple Python script execution with JSON output
- **Smart Rate Limiting**: Implements random delays (15-60 seconds) and retry logic to avoid being blocked
- **User-Agent Rotation**: Uses fake user agents to reduce bot detection
- **Structured Output**: Exports data to JSON format for easy integration with other tools
- **Error Handling**: Robust error handling with retry mechanisms
- **SSL Security**: Uses certified SSL connections for all requests

---

## Prerequisites

- **Python 3.7+**
- **OpenAI API Key** (for job description summaries)

### Required Python Libraries
- `requests`
- `beautifulsoup4`
- `certifi`
- `cloudscraper`
- `fake_useragent`
- `openai`
- `python-dotenv`

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/job-scraper.git
   cd job-scraper
   ```

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```ini
OPENAI_API_KEY=your_openai_api_key_here
```

### Scraper Configuration

**ITJobs Scraper:**
- Target: British Columbia IT jobs
- Pages: 1-7
- Rate limiting: Standard HTTP requests

**TechTalent Scraper:**
- Target: Information Technology jobs in British Columbia
- Retry attempts: Up to 3 per job description
- Rate limiting: 15-60 second random delays
- AI summaries: Powered by OpenAI GPT-4

---

## Usage

Run the main script to start scraping:

```bash
python main.py
```

The program will:
1. Start scraping ITJobs.ca (pages 1-7)
2. Scrape TechTalent job listings
3. Fetch detailed descriptions for each TechTalent job
4. Generate AI summaries for TechTalent descriptions
5. Combine all data and save to `joblist.json`

---

## Output

The program generates a `joblist.json` file with the following structure:

```json
{
  "itjobs": [
    {
      "position": "Software Developer",
      "company": "Tech Company Inc.",
      "location": "Vancouver, BC",
      "description": "Full job description text..."
    }
  ],
  "techtalent": [
    {
      "position": "Full Stack Engineer",
      "company": "Innovation Corp",
      "location": "Victoria, BC",
      "job_description_url": "https://jobs.techtalent.ca/job/12345",
      "summary": "AI-generated summary of the job description..."
    }
  ]
}
```

---

## Troubleshooting

### Common Issues

**OpenAI API Errors:**
- Verify your API key is correct in the `.env` file
- Check your OpenAI account has sufficient credits
- Ensure you have access to GPT-4 model

**Scraping Blocked/Rate Limited:**
- The scripts use random delays and user agents, but sites may still block requests
- Try running at different times of day
- Consider increasing delay ranges in the code

**SSL Certificate Errors:**
- The scripts use `certifi` for secure connections
- Update `certifi` if you encounter SSL issues: `pip install --upgrade certifi`

**Import Errors:**
- Ensure all requirements are installed: `pip install -r requirements.txt`
- Check that you're in the correct directory

**No Job Descriptions Found:**
- Website structure may have changed
- Check if the target websites are accessible
- Review the HTML parsing selectors in the code

---

## Disclaimer

This tool is for educational and personal use only. Please respect the terms of service of the websites being scraped and use responsibly. Be mindful of rate limits and avoid overloading servers with requests.
