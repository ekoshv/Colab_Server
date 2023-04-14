import json
from flask import Flask, request, jsonify, url_for
from flask_ngrok import run_with_ngrok
import pandas as pd
import os


class ColabAPIServer:
    def __init__(self):
        """Initialize the ColabAPIServer class and define routes."""
        self.app = Flask(__name__)
        run_with_ngrok(self.app)

        @self.app.route('/upload/<key>', methods=['POST'])
        def upload(key):
            if not os.path.exists('uploaded_files'):
                os.makedirs('uploaded_files')

            file_path = os.path.join('uploaded_files', key)
            with open(file_path, 'wb') as f:
                f.write(request.data)

            return jsonify({'status': 'ok'})

        @self.app.route('/execute', methods=['POST'])
        def execute():
            """
            Handle the code execution request.
            :return: The result of the code execution.
            """
            data = request.get_json(force=True)

            code = data.get('code', '')

            # Load input data from uploaded files
            input_data = {}
            for key in request.files:
                file_path = os.path.join('uploaded_files', key)
                input_data[key] = self.load_file(key, file_path)

            result = self.execute_code(code, input_data)
            return jsonify(result)

    def load_file(self, key, file_path):
        if file_path.endswith('.parquet'):
            return pd.read_parquet(file_path)
        else:
            with open(file_path, 'r') as f:
                return json.load(f)

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
        
