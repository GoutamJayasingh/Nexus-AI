# Nexus-AI

## Overview

This project demonstrates how AI agents work using external tools.

The agent can:

* Search the web
* Read Excel files
* Execute Python files

The tool outputs are passed to an LLM, which generates the final answer.

## Architecture

User Question
↓
Agent
↓
Choose Tool
↓
Execute Tool
↓
Collect Context
↓
LLM
↓
Answer

## Tools

### Web Search

Uses DDGS to retrieve information from the internet.

### Excel Reader

Reads spreadsheet data using pandas.

### Python Executor

Executes Python files and returns the output.

## Technologies

* Python
* Groq API
* Llama 3.3 70B
* Pandas
* DDGS

## Learning Goals

* Agent Architecture
* Tool Calling
* LLM Integration
* Retrieval Workflows
* AI Engineering Fundamentals
