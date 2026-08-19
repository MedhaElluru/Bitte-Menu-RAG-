# Bitte Menu RAG

A Streamlit chatbot that answers questions about the Bitte menu using **Retrieval-Augmented Generation (RAG)**. It connects to OpenAI's Responses API and searches a pre-built vector store so answers are grounded in your uploaded menu documents rather than general model knowledge.

## What it does

- Provides a web-based chat interface for asking questions about the Bitte menu
- Retrieves relevant context from an OpenAI vector store via the **File Search** tool
- Supports **multi-turn conversations** so follow-up questions keep context
- Accepts optional **image uploads** alongside text prompts
- Lets users **clear the conversation** and start fresh from the sidebar

## How it works

```
User prompt (+ optional images)
        │
        ▼
  Streamlit UI (app.py)
        │
        ▼
  OpenAI Responses API  ──►  gpt-5-nano
        │
        ▼
  File Search tool  ──►  Vector Store (menu documents)
        │
        ▼
  Grounded answer displayed in chat
```

1. **Environment setup** — On startup, the app loads `OPENAI_API_KEY` and `VECTOR_STORE_ID` from a `.env` file (via `python-dotenv`).

2. **User input** — The user types a message in the chat input. They can optionally upload image files (JPEG, JPG, WebP, or PDF). Uploaded images are base64-encoded and sent to the API as `input_image` content.

3. **Request building** — The app constructs a request with:
   - A **developer/system prompt** instructing the model to answer only from the vector store
   - The user's text and any attached images

4. **API call** — The app calls `client.responses.create()` with:
   - Model: `gpt-5-nano`
   - The `file_search` tool pointed at your vector store (up to 10 results)
   - `previous_response_id` to maintain conversation continuity across turns

5. **Display** — The assistant's response is shown in the chat and stored in session state for the conversation history.

> **Note:** The vector store must be created and populated separately in the OpenAI platform before running this app. This project assumes that work is already done and only needs the vector store ID.

## Prerequisites

- Python 3.10 or later
- An [OpenAI API key](https://platform.openai.com/api-keys)
- A pre-built OpenAI **Vector Store** containing your Bitte menu documents

## Setup

### 1. Clone or download the project

```bash
cd "Bitte RAG"
```

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
VECTOR_STORE_ID=your_vector_store_id_here
```

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `VECTOR_STORE_ID` | ID of the vector store containing Bitte menu documents |

Do not commit `.env` to version control.

## Running the app

With the virtual environment activated:

```bash
streamlit run app.py
```

Streamlit will print a local URL (typically **http://localhost:8501**). Open it in your browser to use the chatbot.

To stop the server, press `Ctrl+C` in the terminal.

## Project structure

```
Bitte RAG/
├── app.py              # Streamlit application
├── requirements.txt    # Python dependencies
├── .env                # API keys and config (not committed)
├── README.md           # This file
└── venv/               # Virtual environment (not committed)
```

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web UI framework |
| `openai` | OpenAI Responses API client |
| `python-dotenv` | Load environment variables from `.env` |
| `pillow` | Image handling support |

## Troubleshooting

| Issue | Fix |
|---|---|
| `OPENAI_API_KEY is not set` | Add your API key to the `.env` file and restart the app |
| `VECTOR_STORE_ID is not set` | Add your vector store ID to the `.env` file |
| Port already in use | Streamlit will try the next available port (e.g. 8502); check the terminal output for the correct URL |
| App not loading in browser | Confirm the terminal shows "You can now view your Streamlit app" and use the URL it prints |
