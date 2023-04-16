import json
import pickle
from flask import Flask, request, jsonify, url_for, send_file
from flask_ngrok import run_with_ngrok
from io import BytesIO

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
            code_file = request.files['code']
            code = code_file.read().decode('utf-8')

            input_data_file = request.files['input_data']
            input_data = pickle.load(input_data_file)

            result = self.execute_code(code, input_data)

            pickled_result = BytesIO()
            pickle.dump(result, pickled_result)
            pickled_result.seek(0)

            return send_file(pickled_result, attachment_filename='result.pkl', as_attachment=True)

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
            return local_namespace.get('result', None)
        except Exception as e:
            return {'error': str(e)}

    def run(self):
        """Run the Colab API server and display the public URL."""
        with self.app.test_request_context():
            public_url = url_for('execute', _external=True)

        print(" * Starting Colab API server...")
        print(f" * Public URL: {public_url}")
        self.app.run()
``
