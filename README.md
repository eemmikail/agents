[TR]

# Basitten Zora Agent Örnekleri

Dökümantasyon için: https://mikailkaradeniz.dev/pages/tutorial/tutorial.php

[EN]

# Simple to Difficult Agent Examples

Documentation: https://mikailkaradeniz.dev/pages/tutorial/tutorial.php
Anthropic Doc: https://www.anthropic.com/engineering/building-effective-agents

## Table of Contents

1. [Google AI API Integration](#1-google-ai-api-integration)
2. [Tool Integration Example (Weather)](#2-tool-integration-example)
3. [Retrieval Example (Customer Service)](#3-retrieval-example)
4. [Workflow and Prompt Chaining](#4-workflow-and-prompt-chaining)
5. [Message Routing System](#5-message-routing)
6. [Parallel Processing](#6-parallel-processing)
7. [Orchestrator and Evaluator](#7-orchestrator-and-evaluator)

## Documentation

### 1. Google AI API Integration

This example demonstrates how to connect an agent with Google's AI APIs, enabling access to powerful language models for generating responses, translations, and content creation.

### 2. Tool Integration Example (Weather)

Shows how to augment an agent with external tools like weather services. This enables the agent to access real-time data through APIs to provide accurate, current information. According to Anthropic, tools are a fundamental part of effective agents, allowing them to extend beyond their training data and interact with external services.

### 3. Retrieval Example (Customer Service)

Illustrates how to build agents that retrieve information from knowledge bases to answer customer queries. This implements Retrieval-Augmented Generation (RAG) patterns where agents access documentation to provide precise answers. Anthropic notes this is particularly effective for customer support scenarios where agents need access to customer data, order history, and knowledge base articles.

### 4. Workflow and Prompt Chaining

Demonstrates sequential processing where the output of one prompt becomes input for the next. Anthropic defines this as a workflow that "decomposes a task into a sequence of steps, where each LLM call processes the output of the previous one." This pattern is ideal when a task can be cleanly divided into fixed subtasks, trading latency for higher accuracy by making each LLM call an easier task. Examples include generating content in one step, then translating it in another, or creating an outline before writing a full document.

### 5. Message Routing System

Shows how to direct messages to appropriate specialized agents based on content analysis. Anthropic describes this as a workflow that "classifies an input and directs it to a specialized followup task." This pattern works well for complex tasks with distinct categories that are better handled separately. Examples include directing different types of customer service queries (general questions, refunds, technical support) to different downstream processes.

### 6. Parallel Processing

Illustrates how to process multiple tasks concurrently for improved efficiency. Anthropic identifies two key variations:

- **Sectioning**: Breaking a task into independent subtasks run in parallel
- **Voting**: Running the same task multiple times to get diverse outputs

This pattern is effective when subtasks can be parallelized for speed or when multiple perspectives are needed for higher confidence results.

### 7. Orchestrator and Evaluator

Demonstrates systems that coordinate multiple agents and evaluate their outputs. According to Anthropic, these include:

- **Orchestrator-Workers workflow**: A central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results. This is well-suited for complex tasks where subtasks can't be predicted in advance, like making changes to multiple code files.

- **Evaluator-Optimizer workflow**: One LLM generates a response while another provides evaluation and feedback in a loop. This is effective when there are clear evaluation criteria and iterative refinement provides measurable value, similar to a human editing process.

Both patterns can be combined to create more sophisticated agent systems that handle complex, open-ended tasks while maintaining quality through feedback loops.
