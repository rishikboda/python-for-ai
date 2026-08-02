import requests
def chatgpt(question):
    response=requests.get(f"https://claude.ai/new{question}=answer")
    data=response.json
    return data['answer']
x = chatgpt("what is your name")
print(x)
