import json
from flask import Flask, request, jsonify, url_for
from flask_ngrok import run_with_ngrok
import pickle

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
            pickled_input_data = data.get('input_data', b'')
            input_data = pickle.loads(pickled_input_data)

            result = self.execute_code(code, input_data)

            pickled_result = pickle.dumps(result)
            return jsonify({'result': pickled_result})

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

if __name__ == "__main__":
    server = ColabAPIServer()
    server.run()
