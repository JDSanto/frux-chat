"""User namespace module."""

from flask import jsonify
from flask_restx import Namespace, Resource

ns = Namespace("Health", description="Status endpoint",)


@ns.route('')
class health(Resource):
    """Health check endpoint"""

    def get(self):
        return jsonify(status='ok')
