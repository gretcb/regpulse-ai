# RegPulse AI

AI-powered environmental intelligence for the European shipping industry.

RegPulse AI retrieves recent maritime environmental and regulatory news,
analyzes its business impact with OpenAI, and generates a short executive
podcast using Text-to-Speech.

## MVP Workflow

1. The user selects an EU country.
2. The user selects a timeframe:
   - Last Week
   - Last Month
3. The application retrieves relevant maritime news.
4. OpenAI generates:
   - Executive Summary
   - Business Impact
   - Podcast Script
5. OpenAI Text-to-Speech generates an MP3 file.
6. Gradio displays the results.

## Project Structure

```text
regpulse-ai/
├── app.py
├── src/
│   ├── __init__.py
│   ├── news_fetcher.py
│   ├── prompts.py
│   ├── llm_processor.py
│   └── tts_generator.py
├── tests/
│   ├── __init__.py
│   ├── test_news.py
│   ├── test_llm.py
│   └── test_tts.py
├── output/
├── examples/
├── requirements.txt
├── .env.example
└── .gitignore