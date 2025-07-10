# 📬 MailSummarizer

A **local AI agent** that reads your unread emails and summarizes them in a few words — built using the **Qwen 3 8B** model from **Ollama**, and powered by **LangGraph**, **LangChain**, and **IMAPTools**.

> ✅ 100% local processing — your data never leaves your machine.

---

## 🔧 Features

- 🔍 Reads **unread emails** from your mailbox using IMAP
- 🧠 Summarizes emails using **Qwen 3 8B** via Ollama
- ⚙️ Modular agent flow built with **LangGraph** + **LangChain**
- 🔐 All operations are fully local — **no cloud API calls**

---

## 🧱 Tech Stack

- [Ollama](https://ollama.com) – runs the Qwen LLM locally
- [LangGraph](https://www.langgraph.dev/) – agent flow as a graph
- [LangChain](https://www.langchain.com/) – framework for LLM apps
- [IMAPTools](https://imap-tools.readthedocs.io/) – access unread emails

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/mailsummarizer.git
cd mailsummarizer
```

### 2. Install Dependencies

Make sure **Python 3.10+** is installed.

```bash
pip install langchain langgraph imap-tools python-dotenv
```
### 3. Pull the Ollama Model 
```ollama pull qwen:8b
```

### 4. Running the Agent
```python run_agent.py
```
