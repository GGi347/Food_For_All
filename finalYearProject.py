from app import app, db
from app.models import User, Restaurant

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Restaurant': Restaurant}