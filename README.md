# PrivacyChat
This repository contains the full source code for the final undergraduate project titled:
"Privacy-Preserving Data Handling in LLMs through Semantic Randomization and Reversibility".

The project proposes a multi-agent system designed using the LangGraph framework, enabling the anonymization and de-anonymization of sensitive user data in conversational AI pipelines.
It integrates:

A PII detection agent using Microsoft Presidio and spaCy.

A randomization/de-randomization agent powered by Qwen 2.5–7B via Ollama.

A chatbot agent that interfaces with OpenAI GPT-4.

The architecture ensures that personally identifiable information (PII) is never directly exposed to third-party models, enabling secure and reversible data transformation.

The repository includes:

Python source files and agent logic (LangGraph-based state machine).

Presidio configuration and custom regex patterns.

Prompt templates for semantic randomization.
