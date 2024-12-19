# AI Code Assistant

This is an AI agent that can assist code generation.

## Installation

### 1. Clone the repository
First, clone the repository and navigate to the project folder:

```bash
git clone https://github.com/simret/assistant.git
cd codeassistant
```

### 2. Activate the virtual environment
Activate the virtual environment:

```bash
python3 -m venv envname
source envname/bin/activate
```

### 3. Install dependencies in requirements.txt
Install the required dependencies for the project:

```bash
pip install -r requirements.txt
```

## 4. Configuration
The application uses environment variables to set up its parameters.

**Environment Variables**
The `.env` file contains sensitive information like API keys.

## Usage

Once your environment is configured, you can run the Flask server and streamlit

```bash
python3 main.py
streamlit run app.py
```
This will start the server at http://localhost:5000
 http://localhost:8501

Ensure that the environment variables are set correctly in `.env` before running the application

* **LLM Model Configuration:**
  * ollama should be installed and cloud api key is required
Download Ollama: https://github.com/ollama/ollama
curl -fsSL https://ollama.com/install.sh | sh

* **LLM parameters used:**  
  * temperature: 0.3 used to ensure code follows predictable patterns and avoids error.
  * top_p: 0.9 used to allow a bit more creativity while keeping the structure intact (e.g., exploring different sorting algorithms).
  * max_length: 100 used to limit the output to a concise function that’s not too long but provides enough detail.
The parameters can be fine-tune to generate code that is either precise and conventional or creative and experimental, depending on the use case.

* **API Keys:**
Create a LlamaCloud Account to Use LLama Parse: https://cloud.llamaindex.ai
  * `LAMA_CLOUD_API_KEY`: Your Cloud API key.
