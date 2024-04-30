from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers, HuggingFacePipeline
from langchain.chains import RetrievalQA

from src.prompt import *
from transformers import AutoTokenizer, AutoModel, BitsAndBytesConfig, pipeline
from store_index import vectordb

from dotenv import load_dotenv

# import pinecone
# from langchain.vectorstores import Pinecone

import torch
import os


app = Flask(__name__)

# load_dotenv()

# PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
# PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')


embeddings = download_hugging_face_embeddings()

# pinecone.init(api_key=PINECONE_API_KEY,
#               environment=PINECONE_API_ENV)

# index_name="ai-customer-service"
# docsearch=Pinecone.from_existing_index(index_name, embeddings)

PROMPT=PromptTemplate(template=prompt_template, input_variables=["context", "question"])

chain_type_kwargs={"prompt": PROMPT}



model_path = "THUDM/chatglm-6b"
tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False, trust_remote_code=True)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)


llm = AutoModel.from_pretrained(
    model_path,
    low_cpu_mem_usage=True,
    quantization_config=bnb_config,
    trust_remote_code=True,
    # device_map='auto',
    # from_tf = True,
)

pipe = pipeline(
    "text-generation",
    model=llm,
    tokenizer=tokenizer,
    max_length=4096,
    temperature=1.0,
    do_sample=True,
    top_p=0.95,
    repetition_penalty=1.15
)

local_llm = HuggingFacePipeline(pipeline=pipe)
retriever = vectordb.as_retriever(search_kwargs={"k": 3})


qa_chain = RetrievalQA.from_chain_type(llm=local_llm,
                                  chain_type="stuff",
                                  retriever = retriever,
                                  chain_type_kwargs=chain_type_kwargs,
                                #   return_source_documents=True
)



@app.route("/")
def index():
    return render_template('chat.html')



@app.route("/get", methods=["GET", "POST"])
# def chat():
#     msg = request.form["msg"]
#     input = msg
#     test = qa_chain.run(input)
#     result=qa_chain({"query": input})
#     print("Result : ", result)
#     arr = str(test).split("回答uiop1234：")
#     print("ARR:", arr)
#     print("Response:", arr[1])

#     return str(arr[1])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    result=qa_chain({"query": input})
    print("Response : ", result["result"])
    return str(result["result"])



if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)


