# RAG Fullstack Application

This repository contains the full-stack implementation for the RAG (Retrieve, Answer, Generate) application. It provides a web interface and backend API to interact with a language model, perform keyword extraction, and generate word clouds based on retrieved information.

## Features

- **Frontend**: Built with React to provide an interactive web interface.
- **Backend**: Developed using FastAPI to handle API requests.
- **Vector Store**: Utilizes Qdrant for vector storage and retrieval.
- **Language Model**: Powered by OpenAI's GPT-3.5-turbo for generating answers.
- **Keyword Extraction**: Uses TF-IDF vectorization to extract keywords from text responses.
- **Word Cloud Generation**: Creates visual representations of word frequency using extracted keywords.

## Requirements

- Python 3.12
- Node.js and npm
- Qdrant
- OpenAI API Key (set as environment variable `OPENAI_API_KEY`)


### Contribute

1. Clone the repository:

   ```bash
   git clone https://github.com/<username>/RAG-Fullstack-Backend.git
   cd RAG-Fullstack-Backend
