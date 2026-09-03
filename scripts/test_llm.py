from app.services.llm import generate_response

response = generate_response("Explain what an IP address is in one sentence.")

print(response)
