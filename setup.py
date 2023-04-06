from setuptools import setup, find_packages

setup(
    name="colab_api_server",
    version="0.1.0",
    author='Ehsan KhademOlama',
    author_email='ekoshv.igt@gmail.com',
    description='A Python library for setting up a remote Google Colab API server',
    packages=find_packages(),
    install_requires=[
        "Flask>=2.1.1",
        "flask-ngrok>=0.0.25",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
)





