import base64
import io
from flask import Flask, request, jsonify, url_for
from flask_ngrok import run_with_ngrok

class ColabAPIServer:
    def __init__(self):
        self.app = Flask(__name__)
        run_with_ngrok(self.app)

        @self.app.route('/execute', methods=['POST'])
        def execute():
            data = request.get_json(force=True)
            code = data.get('code', '')
            input_data = data.get('input_data', {})
            result = self.execute_code(code, input_data)
            return jsonify(result)

    def execute_code(self, code, input_data):
        try:
            local_namespace = {'input_data': input_data}
            exec(code, globals(), local_namespace)
            result_object = local_namespace.get('result', None)

            if result_object is not None:
                model_buffer = io.BytesIO()
                result_object.save(model_buffer)
                model_buffer.seek(0)
                result_encoded = base64.b64encode(model_buffer.read()).decode('utf-8')
            else:
                result_encoded = None

            return {'result': result_encoded}
        except Exception as e:
            return {'error': str(e)}

    def run(self):
        with self.app.test_request_context():
            public_url = url_for('execute', _external=True)

        print(" * Starting Colab API server...")
        print(f" * Public URL: {public_url}")
        self.app.run()
