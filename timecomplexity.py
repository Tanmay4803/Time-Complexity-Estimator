import streamlit as st
import ast
import textwrap
import requests
import re

# HF token and API setup
HF_TOKEN = "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"
API_URL = "https://router.huggingface.co/together/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def query_llm(prompt):
    payload = {
        "messages": [
            {"role": "system", "content": "You are a time complexity analysis expert."},
            {"role": "user", "content": prompt}
        ],
        "model": "mistralai/Mistral-7B-Instruct-v0.3",
        "temperature": 0.2,
        "max_tokens": 300
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        return f"API Error: {response.status_code} - {response.text}"
    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception:
        return "Error parsing LLM response. Try again later."

class TimeComplexityAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.loop_nesting = 0
        self.max_nesting = 0
        self.recursive_calls = 0
        self.func_name = ""
        self.contains_recursion = False

    def visit_FunctionDef(self, node):
        self.func_name = node.name
        self.generic_visit(node)

    def visit_For(self, node):
        self.loop_nesting += 1
        self.max_nesting = max(self.max_nesting, self.loop_nesting)
        self.generic_visit(node)
        self.loop_nesting -= 1

    def visit_While(self, node):
        self.loop_nesting += 1
        self.max_nesting = max(self.max_nesting, self.loop_nesting)
        self.generic_visit(node)
        self.loop_nesting -= 1

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == self.func_name:
            self.recursive_calls += 1
            self.contains_recursion = True
        self.generic_visit(node)

    def analyze(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return f"Syntax Error: {e}"
        self.visit(tree)
        return {
            "max_loop_nesting": self.max_nesting,
            "recursive_calls": self.recursive_calls,
            "contains_recursion": self.contains_recursion
        }

def generate_prompt(code, features):
    return textwrap.dedent(f"""
    You are an expert software engineer.

    Analyze the following Python function and provide the **average-case time complexity** using Big-O notation. 

    Return only the average-case complexity with a brief explanation. do not discuss best or worst-case or optimized versions but explain briefly about the code.

    Code:
    {code}

    Features extracted:
    - Max Loop Nesting: {features['max_loop_nesting']}
    - Contains Recursion: {features['contains_recursion']}
    - Recursive Calls: {features['recursive_calls']}

    Your answer should be focused, accurate, and end with the line:
    Time Complexity: O(...)
    """)

def extract_big_o(text):
    match = re.search(r"O\([^()]+\)", text)
    return match.group(0) if match else None

def estimate_time_complexity(code):
    analyzer = TimeComplexityAnalyzer()
    features = analyzer.analyze(code)
    if isinstance(features, str):  # Error string
        return features

    prompt = generate_prompt(code, features)
    raw_response = query_llm(prompt)

    big_o = extract_big_o(raw_response)
    if big_o:
        raw_response += f"\n\n**Time Complexity: {big_o}**"
    else:
        raw_response += "\n\n**Time Complexity: Not found**"

    return raw_response

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Time Complexity Estimator", layout="centered")
st.title("🧠 Time Complexity Estimator (AST + Mistral 7B)")

code_input = st.text_area("Enter Python code below:", height=250, value="""
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
""")

if st.button("Estimate Time Complexity"):
    with st.spinner("Analyzing..."):
        result = estimate_time_complexity(code_input)
    st.subheader("📊 Estimated Time Complexity:")
    st.markdown(result)
