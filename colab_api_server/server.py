import json
from flask import Flask, request, jsonify, url_for
from flask_ngrok import run_with_ngrok
import pickle
import base64

class ColabAPIServer:
    def __init__(self):
        """Initialize the ColabAPIServer class and define routes."""
        self.app = Flask(__name__)
        run_with_ngrok(self.app)

        @self.app.route('/execute', methods=['POST'])
        def execute():
            """
            Handle the code execution request.
            :return: The result of the code execution.
            """
            data = request.get_json(force=True)

            code = data.get('code', '')
            base64_input_data = data.get('input_data', '')
            pickled_input_data = base64.b64decode(base64_input_data)
            input_data = pickle.loads(pickled_input_data)

            result = self.execute_code(code, input_data)

            pickled_result = pickle.dumps(result)
            base64_result = base64.b64encode(pickled_result).decode('utf-8')
            return jsonify({'result': base64_result})

    def execute_code(self, code, input_data):
        """
        Execute the provided code with the given input data.
        :param code: The code to be executed.
        :param input_data: The input data for the code execution.
        :return: The result of the code execution or an error message.
        """
        try:
            local_namespace = {'input_data': input_data}
            exec(code, globals(), local_namespace)
           
