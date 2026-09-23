import threading
import requests

URL = "http://127.0.0.1:8000/bookings/"
HEADERS = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzkwMTkwOTQ2LCJpYXQiOjE3OTAxOTA2NDYsImp0aSI6Ijk5NTJlM2U2MjMxMDRhZjg4MWZlYjJhMDBkYTgzMmEzIiwidXNlcl9pZCI6IjQifQ.8xMcB_MD174nWwzQG4Rw_XhhqHMG1jJI0lkzYcLOgmc"}
DATA = {
    "provider": 1,
    "time": "2026-10-15T11:00:00",   # یه Slot جدید که تا حالا رزرو نکردی
    "duration": "00:30:00"
}

def make_request(name):
    response = requests.post(URL, json=DATA, headers=HEADERS)
    print(f"{name}: Status={response.status_code} | Response={response.json()}")

t1 = threading.Thread(target=make_request, args=("Request A",))
t2 = threading.Thread(target=make_request, args=("Request B",))

t1.start()
t2.start()

t1.join()
t2.join()