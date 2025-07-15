# pii_guardrails_demo
PAC blocker for PII info shared in a prompt

THIS EXAMPLE IS FOR AN AI GOVERNANCE MODULE for an intern training course.
Class participants can fork the provided LCEL chain and attach a Guardrails YAML that:
• blocks PII leaks.

Test Prompt is: "My name is John Doe and my SSN is 123-45-6789."

It shows how to wrap **any LCEL chain** with a Guardrails rule that **blocks** if the response contains personally identifiable information.

---

## 1 · Create the Guardrails policy

`pii_guardrails.yml`

```yaml
validators:
  - type: pii
    mode: block        # refuse to return if PII is detected
    on_fail: "block"   # raises GuardrailsError
```

That’s it—no enforced output schema, just a single validator.

---

## 2 · Python wrapper

`pii_guardrails_demo.py`

```python
"""
Demo: block model outputs that leak PII using Guardrails‑AI
Prereqs: pip install langchain-openai guardrails-ai
"""

from guardrails import Rails, Guard
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

# --- 1. Minimal LCEL chain ------------------------------------
template = "Answer the user's question truthfully:\nUser: {question}"
prompt = ChatPromptTemplate.from_template(template)
llm    = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
chain  = prompt | llm | RunnableLambda(lambda x: x)   # passthrough

# --- 2. Attach PII guardrails ---------------------------------
rails = Rails.from_file("pii_guardrails.yml")
safe_chain = Guard(rails)(chain)

# --- 3. Test prompts ------------------------------------------
tests = [
    {"question": "What time is sunset in Paris?"},
    {"question": "My name is John Doe and my SSN is 123-45-6789."},
    {"question": "Call me at (555)‑123‑4567 tomorrow."}
]

for t in tests:
    try:
        out = safe_chain.invoke(t)
        print("OK  :", out)
    except Exception as e:
        print("BLOCK:", e)
```

Expected console output:

```
OK  : Paris sunset is at 9:45 PM today.
BLOCK: PII detected in content → output blocked
BLOCK: PII detected in content → output blocked
```

---

### How to run

```bash
python pii_guardrails_demo.py
```

Commit `pii_guardrails.yml` and `pii_guardrails_demo.py` to your fork—done!
Students now have a working template that prevents PII leakage while leaving the rest of the chain unchanged.
