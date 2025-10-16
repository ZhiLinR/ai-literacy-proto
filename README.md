# ai-literacy-proto
This repo contains the Proof-Of-Concept implementation for LAW 4067 AI: Digital Literacy for Lawyers, an experimental implementation of a chatbot with a RAG layer with divorce cases on unreasonable behaviour. This aims to provide a concept for AI 

1. [PDF Report](https://drive.google.com/file/d/1aD7YA_hh1RoNVzAwCb5wzjq_7Ylirgvg/view?usp=sharing)
2. [Youtube Demo (Sped up) ](https://youtu.be/xui0y0U2oys)
3. [Slide Deck](https://drive.google.com/file/d/1dH3cMvRqnGvcFXax4s3tUoNb4X5UmldC/view?usp=drive_link)

## Base
- OpenAI gpt5-nano using Responses API
    - [File Search](https://platform.openai.com/docs/guides/tools-file-search)
    - [Function Calling](https://platform.openai.com/docs/guides/function-calling)
    - Streaming
- Chainlit (frontend framework for building conversational AI)
    - Basic user session implementation

## Tools provided to the model
- Mailgun API: Includes a template built within Mailgun, which emails the firm after an inquiry has been deemed complete. 
- Calendly API: For scheduling. 

## Cases Referenced
- Castello Ana Paula Costa Fusillier v Lobo Carlos Manuel Rosado
- Teo Hoon Ping v Tan Lay Ying Angeline [2009] SGHC 244
- Wong Siew Boey v Lee Boon Fatt [1994] 1 SLR(R) 0323
