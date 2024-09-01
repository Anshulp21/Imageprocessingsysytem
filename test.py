from app import db
from app.models.request import ProcessingRequest

request_id = '75f159c8-38c0-42d4-bed2-e67e6319a16d'
request = ProcessingRequest.query.filter_by(request_id=request_id).first()

if request:
    print(request.status)
else:
    print("Request not found")
