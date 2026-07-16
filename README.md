# 🌊 RegPulse AI

> **AI-powered executive intelligence for environmental regulations in the European commercial maritime shipping industry.**

![Python](https://img.shields.io/badge/Python-3.11-blue)
![OpenAI](https://img.shields.io/badge/OpenAI-API-success)
![Gradio](https://img.shields.io/badge/Gradio-UI-orange)
![NewsAPI](https://img.shields.io/badge/NewsAPI-News-red)
![Status](https://img.shields.io/badge/Status-MVP-brightgreen)

---

# 📖 Executive Summary

RegPulse AI is an AI-powered application that helps professionals in the European maritime shipping industry monitor environmental regulations more efficiently.

Instead of reading multiple articles from different sources, users receive an executive briefing containing:

- 📰 A summary of the latest relevant news
- 📊 A business impact assessment
- 🎙️ An AI-generated executive podcast

The application combines News Retrieval, Large Language Models (LLMs) and Text-to-Speech to transform raw information into actionable insights.

Developed as a two-day MVP during the **Ironhack AI Consulting & Integration Bootcamp**, the project demonstrates how AI can support executive decision-making through an end-to-end workflow.

## 🎯 Project Objectives

During this project we aimed to:

- Build a complete end-to-end AI application.
- Apply Prompt Engineering in a real use case.
- Design a modular and scalable architecture.
- Improve the relevance of retrieved news through a better retrieval strategy.
- Deliver an intuitive executive dashboard.
- Demonstrate AI consulting best practices under a two-day MVP constraint.

---

# 🚢 Business Problem

Environmental regulations such as **FuelEU Maritime**, **EU ETS** and **IMO initiatives** are rapidly transforming the European shipping industry.

Companies need to continuously monitor regulatory updates, understand their implications and communicate them internally.

This process is:

- Time-consuming
- Repetitive
- Difficult to scale
- Dependent on reviewing multiple information sources

RegPulse AI automates this workflow by transforming unstructured news into concise executive briefings.

---

# 💡 Our Solution

RegPulse AI provides a simple workflow for maritime professionals.

The user selects:

- 🇪🇺 An EU country
- 📅 A timeframe

The application then:

1. Retrieves recent maritime environmental news.
2. Filters and prioritizes the most relevant articles.
3. Generates an executive summary using OpenAI.
4. Identifies the potential business impact.
5. Creates an AI-generated podcast.
6. Displays everything through an interactive Gradio dashboard.

The goal is to help decision-makers consume relevant regulatory information in just a few minutes.

---

# ✨ Key Features

- 🌍 EU country selection
- 📅 Timeframe selection
- 📰 Maritime news retrieval
- 🎯 Intelligent article filtering and prioritization
- 🤖 AI-generated executive summaries
- 📈 Business impact analysis
- 🎙️ AI-generated executive podcast
- 🖥️ Interactive Gradio interface
- 🧩 Modular architecture
- 🧪 Independent module testing
- ⚠️ Error handling and logging

---

# 🛠️ Tech Stack

### Programming Language

- Python

### AI

- OpenAI API
- GPT Models
- OpenAI Text-to-Speech

### Data Sources

- NewsAPI

### Interface

- Gradio

### Libraries

- requests
- python-dotenv
- matplotlib

### Development

- Git
- GitHub
- VS Code

---
# 🏗️ System Architecture

RegPulse AI follows a modular architecture where each component has a single responsibility. This approach made development, testing and integration significantly easier.

```text
                 User Input
      (Country + Timeframe)
                    │
                    ▼
          News Retrieval Module
                    │
                    ▼
      Search Intelligence Layer
   (Filtering & Article Ranking)
                    │
                    ▼
         LLM Processing Module
                    │
                    ▼
      Executive Summary & Impact
                    │
                    ▼
      Text-to-Speech Generation
                    │
                    ▼
           Gradio Dashboard
```

Each module was developed and tested independently before being integrated into the final application.

---

# 🔍 News Retrieval Strategy

One of the biggest technical challenges was retrieving relevant maritime environmental news.

Initially, we relied on increasingly complex Boolean queries to improve the search results. However, after multiple iterations, we realized that the limitation was not the query itself but the nature of NewsAPI, which is a general-purpose news search engine.

To improve relevance, we redesigned the retrieval strategy.

Instead of sending every retrieved article directly to the LLM, the application now applies a local filtering and prioritization process.

The workflow became:

```text
NewsAPI
      │
      ▼
Candidate Articles
      │
      ▼
Noise Filtering
      │
      ▼
Maritime & Regulatory Signals
      │
      ▼
Article Ranking
      │
      ▼
Top Articles
      │
      ▼
LLM Processing
```

This approach significantly improved the quality of the generated summaries while making the retrieval process easier to understand, debug and improve.

---

# 🤖 Prompt Engineering

Prompt engineering became an essential part of the application architecture.

Instead of generating free-form responses, prompts were iteratively refined to produce structured and consistent outputs.

The prompts were designed to always generate:

- 📄 Executive Summary
- 📈 Business Impact Analysis
- 🎙️ Podcast-ready Script

This reduced inconsistent responses and created a more reliable workflow for the end user.

---

# 📂 Project Structure

```text
regpulse-ai/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
│
├── src/
│   ├── news_fetcher.py
│   ├── llm_processor.py
│   ├── prompts.py
│   └── tts_generator.py
│
├── tests/
│   ├── test_news.py
│   └── test_tts.py
│
└── output/
    └── podcast.mp3
```

---

# 🔄 Application Workflow

The complete workflow follows these steps:

1. The user selects an EU country.
2. The user selects a timeframe.
3. The application retrieves recent maritime environmental news.
4. Candidate articles are filtered and prioritized.
5. OpenAI generates an executive summary and business impact analysis.
6. A podcast script is created.
7. OpenAI Text-to-Speech converts the script into audio.
8. Gradio presents the final executive briefing.

---

# 🧪 Testing Strategy

Each module was validated independently before integration.

The project includes:

- ✅ News Retrieval testing
- ✅ Text-to-Speech testing
- ✅ Syntax validation
- ✅ End-to-end pipeline testing

This modular testing approach simplified debugging and reduced integration issues during development.

---
# 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/regpulse-ai.git
cd regpulse-ai
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key
NEWS_API_KEY=your_newsapi_key
```

---

# ▶️ Running the Application

Start the Gradio application:

```bash
python app.py
```

The application will launch locally in your browser.

---

# 🧪 Running the Tests

Run the News Retrieval tests:

```bash
python -m tests.test_news
```

Run the Text-to-Speech tests:

```bash
python -m tests.test_tts
```

Check Python syntax:

```bash
python -m py_compile app.py
```

---

# 🚧 Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Integrating independently developed modules | We defined clear interfaces between modules and tested each one independently before integration. |
| Retrieving relevant maritime news | We redesigned our retrieval strategy by combining broader searches with local filtering and article prioritization instead of relying only on complex Boolean queries. |
| Prompt consistency | We iteratively refined prompts to generate structured executive summaries, business impact analysis and podcast-ready scripts. |
| End-to-end integration | We connected News Retrieval, LLM Processing, Text-to-Speech and Gradio into a single workflow with consistent data flow. |
| User experience | We improved the Gradio interface using layouts and HTML to create a cleaner and more intuitive executive dashboard. |
| Tight development timeline | We prioritized high-impact improvements while maintaining a stable and functional MVP. |

---

# 📚 Lessons Learned

This project taught us that building AI applications is about much more than simply calling an LLM.

Some of our main learnings include:

- Good software architecture makes integration easier.
- Retrieval quality is just as important as LLM quality.
- Prompt engineering significantly improves output consistency.
- Small UX improvements greatly enhance the perceived quality of an MVP.
- Independent module testing simplifies debugging.
- Iterative development leads to more reliable AI applications.

---

# 🚀 Future Improvements

### Short-term

- Improve article prioritization.
- Add additional trusted news sources.
- Enhance dashboard visualizations.
- Improve audio customization.

### Medium-term

- Export executive briefings as PDF.
- Email notifications.
- Historical briefing archive.
- User authentication.

### Long-term

- Integration with official regulatory sources such as EMSA, IMO and EUR-Lex.
- Multi-source news aggregation.
- Semantic search.
- RAG implementation.
- Cloud deployment.
- Enterprise dashboard with historical analytics.

---

# 👥 Team

| Team Member | Responsibilities |
|-------------|------------------|
| **Andreas** | Project ideation, News Retrieval implementation and NewsAPI integration. |
| **Vincent** | Text-to-Speech implementation and OpenAI audio generation. |
| **Gretel** | System architecture, module integration, Prompt Engineering, retrieval strategy improvements, Gradio interface, UX improvements, testing, debugging and overall product coordination. |

---

# 🙏 Acknowledgements

This project was developed as part of the **Ironhack AI Consulting & Integration Bootcamp**.

Over the course of two days, we designed and implemented an end-to-end AI solution that combines news retrieval, Large Language Models, Text-to-Speech and an interactive dashboard to demonstrate how AI can support executive decision-making.

---

# 📄 License

This repository was created for educational and portfolio purposes.