"""
Demo: Block LLM outputs that leak PII using Guardrails‑AI.

Prereqs:
  pip install -r requirements.txt
"""

from guardrails import Rails, Guard
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

template = "Answer the user's question truthfully:\nUser: {question}"
prompt = ChatPromptTemplate.from_template(template)
llm    = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
chain  = prompt | llm | RunnableLambda(lambda x: x)

# Attach PII guardrails
rails = Rails.from_file("pii_guardrails.yml")
safe_chain = Guard(rails)(chain)

tests = [
    {"question": "What time is sunset in Paris?"},
    {"question": "My SSN is 123-45-6789, can you store it?"},
    {"question": "Call me at (555)-123-4567 tomorrow."}
]

for t in tests:
    try:
        res = safe_chain.invoke(t)
        print("OK   :", res)
    except Exception as e:
        print("BLOCK:", e)
