from flask import jsonify


class ErrorResponse:
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def to_json_response(self):
        return jsonify(code=self.code, message=self.message)
