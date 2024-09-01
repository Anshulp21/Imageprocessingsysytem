from app import db

class ProcessingRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.String(36), unique=True, nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    input_urls = db.Column(db.Text, nullable=False)
    output_urls = db.Column(db.Text)
    status = db.Column(db.String(50), default='Pending')

    def __repr__(self):
        return f'<ProcessingRequest {self.product_name}>'
