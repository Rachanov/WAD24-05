import requests

# ทดสอบ health check
response = requests.get('http://localhost:8000/health')
print(response.json())

# ทดสอบการแชท
response = requests.post('http://localhost:8000/chat', json={'message': 'สวัสดีครับ'})
print(response.json())