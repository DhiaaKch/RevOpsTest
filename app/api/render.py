def render_greeting(name: str) -> str:
    # BAD: user input inserted into HTML with no escaping
    return f"<h1>Hello, {name}!</h1>"
