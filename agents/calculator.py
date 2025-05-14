from langchain_core.tools import tool
import sympy as sp


@tool    
def calculator(self, query: str) -> str:
    """ A tool to evaluate mathematical expressions. """
    try:
        # Attempt to evaluate the math expression using SymPy
        result = sp.sympify(query)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"
