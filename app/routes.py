from flask import jsonify

from app import app
from app.repository_service import get_repository_data


@app.route('/repository/<name>')
def get_repository(name: str):
    try:
        repository = get_repository_data(name)
        return jsonify(repository), 200
    except LookupError:
        return f"Repository with name {name} not found", 404
    except Exception as e:
        return f"Internal error occur while trying to retrieve repository data. error: {e}", 500
