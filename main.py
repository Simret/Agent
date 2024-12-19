from flask import Flask, request, jsonify
from llama_index.llms.ollama import Ollama
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, PromptTemplate
from llama_index.core.embeddings import resolve_embed_model
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from pydantic import BaseModel
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.query_pipeline import QueryPipeline
from prompts import context, code_parser_template
from code_reader import code_reader
from dotenv import load_dotenv
import os
import ast

load_dotenv()

app = Flask(__name__)

llm = Ollama(model="mistral", request_timeout=30.0)

parser = LlamaParse(result_type="markdown")

file_extractor = {".pdf": parser}
documents = SimpleDirectoryReader("./data", file_extractor=file_extractor).load_data()

embed_model = resolve_embed_model("local:BAAI/bge-m3")
vector_index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
query_engine = vector_index.as_query_engine(llm=llm)

tools = [
    QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name="api_documentation",
            description="this gives documentation about code for an API. Use this for reading docs for the API",
        ),
    ),
    code_reader,
]

code_llm = Ollama(model="codellama", 
                    temperature=0.3,    # Control randomness of the output
                    top_p=0.9,          # Nucleus sampling
                    max_length=100      # Maximum output length (characters or tokens)
                    )   
agent = ReActAgent.from_tools(tools, llm=code_llm, verbose=True, context=context)


class CodeOutput(BaseModel):
    code: str
    description: str
    filename: str


parser = PydanticOutputParser(CodeOutput)
json_prompt_str = parser.format(code_parser_template)
json_prompt_tmpl = PromptTemplate(json_prompt_str)
output_pipeline = QueryPipeline(chain=[json_prompt_tmpl, llm])

@app.route("/run_flow", methods=["POST"])
def run_flow():
    data = request.json
    prompt = data.get('input_value')
# while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    
    if not prompt:
        return jsonify({"error": "No input value provided"}), 400
    retries = 0
    while retries < 3:
        try:
            result = agent.query(prompt)
            next_result = output_pipeline.run(response=result)
            cleaned_json = ast.literal_eval(str(next_result).replace("assistant:", ""))
            return jsonify(cleaned_json), 200
        except Exception as e:
            retries += 1
            print(f"Error occured, retry #{retries}:", e)
    return jsonify({"error": "Unable to process request, please try again later"}), 500
    # if retries >= 3:
    #     print("Unable to process request, try again...")
    #     continue

    # print("Code generated")
    # print(cleaned_json["code"])
    # print("\n\nDesciption:", cleaned_json["description"])

    # filename = cleaned_json["filename"]

    # try:
    #     with open(os.path.join("output", filename), "w") as f:
    #         f.write(cleaned_json["code"])
    #     print("Saved file", filename)
    # except:
    #     print("Error saving file...")

if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Flask API running on port 5000
