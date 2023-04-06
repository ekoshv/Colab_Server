# Colab API Server

Colab API Server is a Python library that helps set up a REST API server on a Google Colab instance. It allows users to execute code remotely from their local machines using the `colab_remote` library.

## Installation

pip install git+https://github.com/ekoshv/Colab_Server.git

## Usage

To set up the Colab API server, follow these steps:

1. Import the ColabAPIServer class.

from colab_api_server import ColabAPIServer

2. Initialize the ColabAPIServer object.

colab_api_server = ColabAPIServer()

3. Run the API server.

colab_api_server.run()

The server will start and provide you with a public URL. Use this URL to interact with the API from your local machine using the colab_remote library.