# 🧠 Time Complexity Estimator (AST + Mistral 7B)

This is a Streamlit-based AI tool that estimates the **average-case time complexity** of Python functions using:

- 🔍 Static Code Analysis (via Python AST)
- 🤖 Mistral-7B-Instruct-v0.3 via Hugging Face's Together API

No OpenAI key needed. 100% free LLM-powered analysis with clean, understandable explanations.

---

## 🚀 Features

- 🧠 Extracts structural info from your code: loops, recursion, nesting, etc.
- 📤 Sends metadata to a local LLM prompt powered by Mistral 7B
- 📊 Returns **only the average-case time complexity** (e.g., `O(n log n)`)
- ✅ Built entirely with Streamlit
- 🆓 Uses Hugging Face Together API (no OpenAI API key required)

---

## 📦 Requirements

- Python 3.7+
- `streamlit`
- `requests`

Install with:

```bash
pip install streamlit requests
```

---

## 📁 File Structure

```
.
├── timecomplexity.py      # Main Streamlit app
├── README.md              # Project documentation
└── requirements.txt       # Dependencies
```

---

## 🔐 Hugging Face Token Setup

You’ll need a Hugging Face Together API token.

### Option 1: Use the included default token

> Already configured in `timecomplexity.py` as:
>
> `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`  
> *(Note: This is a public demo token and may be rate-limited)*

### Option 2: Set your own Hugging Face token securely

1. Get a token from: https://huggingface.co/settings/tokens  
2. Add it as an environment variable:

```bash
export HF_TOKEN=your_token_here
```

Then modify the code to read from `os.environ["HF_TOKEN"]`.

---

## 🧪 How to Run

```bash
streamlit run timecomplexity.py
```

Then visit: [http://localhost:8501](http://localhost:8501)

---

## 💡 Example Input

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### ✅ Output

> The function recursively calls itself twice per input, leading to exponential growth.  
> **Time Complexity: O(2ⁿ)**

---

## 📷 Screenshot

![Screenshot](screenshot.png)

---

## 📚 Models Used

- [`mistralai/Mistral-7B-Instruct-v0.3`](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3)
- API Provider: [Together](https://together.ai)

---

## 🛡️ Limitations

- Token may hit rate limits or API usage limits
- Does not analyze optimized alternatives unless explicitly coded
- Only average-case complexity is returned (not best/worst/memoized)

---


## 🙋‍♂️ Author

**Tanmay Saxena**  
[GitHub](https://github.com/tanmay-saxena) • [LinkedIn](https://www.linkedin.com/in/tanmay-saxena/)

---

