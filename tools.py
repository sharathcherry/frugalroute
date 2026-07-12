import re

def _safe_eval(expr):
    try:
        expr = expr.replace('^', '**')
        # Only allow numbers and basic math operators
        expr = re.sub(r'[^0-9\+\-\*\/\(\)\.\s]', '', expr)
        if not expr:
            return "Error: Empty expression"
        return str(eval(expr, {"__builtins__": None}, {}))
    except Exception as e:
        return f"Error: {e}"

def calculator(expression: str) -> str:
    """Evaluate a mathematical expression."""
    return _safe_eval(expression)

def web_search(query: str) -> str:
    """Real web search using DDGS, with yfinance fallback for stocks."""
    if "stock" in query.lower() or "price" in query.lower():
        try:
            import yfinance as yf
            import re
            # Try to extract ticker from query
            words = query.upper().split()
            ticker = next((w for w in words if w in ["AMD", "AAPL", "MSFT", "GOOGL", "NVDA", "TSLA"]), "AMD")
            stock = yf.Ticker(ticker)
            price = stock.fast_info.last_price
            return f"Search Results:\n[1] {ticker} Stock Price is currently ${price:.2f}"
        except Exception as e:
            pass
            
    try:
        from ddgs import DDGS
        results = DDGS().text(query, max_results=3)
        if not results:
            return f"No search results found for '{query}'."
        
        context = []
        for i, r in enumerate(results):
            title = r.get("title", "")
            body = r.get("body", "")
            context.append(f"[{i+1}] {title}: {body}")
        
        return "Search Results:\n" + "\n".join(context)
    except Exception as e:
        return f"Search Error: {e}"

def execute_tool(tool_name: str, tool_input: str) -> str:
    tool_name = tool_name.strip()
    tool_input = tool_input.strip()
    if tool_name == "calculator":
        return calculator(tool_input)
    elif tool_name == "web_search":
        return web_search(tool_input)
    return f"Error: Unknown tool '{tool_name}'"
