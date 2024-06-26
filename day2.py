import os
import requests
import json
import chromadb
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain_core.output_parsers import JsonOutputParser

# API 키 파일에서 읽기
def load_api_key(file_path='apikey.txt'):
  with open(file_path, 'r') as file:
    return file.read().strip()

# OpenAI API 키 설정
openai_api_key = load_api_key()

# URL 목록
urls = [
  "https://lilianweng.github.io/posts/2023-06-23-agent/",
  "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
  "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

def cache_file_path(url):
  """URL을 기반으로 캐시 파일 경로 생성"""
  filename = url.split('/')[-2] + '.txt'
  return os.path.join('cache', filename)

def load_and_cache_document(url):
  """문서를 로드하고 캐시에 저장"""
  cache_path = cache_file_path(url)
  if os.path.exists(cache_path):
    with open(cache_path, 'r', encoding='utf-8') as file:
      document = file.read()
  else:
    loader = WebBaseLoader([url])
    documents = loader.load()
    document = documents[0].page_content  # 첫 번째 문서의 본문 사용
    os.makedirs('cache', exist_ok=True)
    with open(cache_path, 'w', encoding='utf-8') as file:
      file.write(document)
  return document

def load_and_split_urls(urls):
  documents = [load_and_cache_document(url) for url in urls]

  text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50, length_function=len, is_separator_regex=False)
  split_texts = [text_splitter.split_text(doc) for doc in documents]

  return split_texts

def save_to_chroma_db(documents, embedding_function):
  """임베딩된 텍스트를 Chroma DB에 저장"""
  vectordb = Chroma.from_documents(documents=documents, embedding=embedding_function)

  print("There are", vectordb._collection.count(), "documents in the collection")

  # 임베딩된 문서와 임베딩을 파일로 저장
  embeddings = [doc.page_content for doc in documents]
  metadata = [doc.metadata for doc in documents]
  data = {
    'embeddings': embeddings,
    'metadata': metadata
  }
  with open('chroma_collection.json', 'w', encoding='utf-8') as f:
    json.dump(data, f)

  return vectordb

def load_chroma_db(embedding_function):
  """파일에서 Chroma DB를 로드"""
  with open('chroma_collection.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

  documents = [Document(page_content=emb, metadata=meta) for emb, meta in zip(data['embeddings'], data['metadata'])]
  vectordb = Chroma.from_documents(documents=documents, embedding=embedding_function)
  return vectordb

def retrieve_related_chunks(query, vectordb):
  results = vectordb.similarity_search(query)  # k는 검색할 유사한 문서의 개수
  return results

def evaluate_relevance(user_query, chunks):
  system_prompt = f"""
    You are a helpful assistant. Evaluate the relevance of the following retrieved chunks to the user query.
    output only {{'relevance': 'yes'}} if the input is relevant or {{'relevance': 'no'}} if the chunk is not relevant in JSON format.
    
    User query: "{user_query}"
    Retrieved chunks: {json.dumps([chunk.page_content for chunk in chunks])}
    """
  return system_prompt

# URL 목록을 로드하고 분할된 텍스트를 얻음
split_texts = load_and_split_urls(urls)

# 모든 분할된 텍스트를 하나의 리스트로 합침
all_texts = [part for doc in split_texts for part in doc]

# 문서 형식으로 변환
documents = [Document(page_content=text) for text in all_texts]

# 임베딩 함수 생성
embedding_function = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=openai_api_key)

# Chroma DB를 저장한 파일이 있는지 확인
if os.path.exists('chroma_collection.json'):
  collection = load_chroma_db(embedding_function)
else:
  collection = save_to_chroma_db(documents, embedding_function)

# 사용자 쿼리 입력
user_query = "agent memory"

# 관련된 청크 검색
related_chunks = retrieve_related_chunks(user_query, collection)

# 검색 결과 출력
print("Related chunks for query 'agent memory':")
for i, chunk in enumerate(related_chunks):
  print(f" Chunk {i+1}: {chunk.page_content[:200]}...")  # 첫 200자만 출력

# 시스템 프롬프트 작성
system_prompt = evaluate_relevance(user_query, related_chunks)

# Llama3 API 호출
url = "http://localhost:11434/api/generate"
model = "llama3"

data = {
  "model": model,
  "prompt": system_prompt,
  "stream": False
}

response = requests.post(url, json=data)

# 응답 확인 및 출력
if response.status_code == 200:
  llama_response = response.json()["response"]
  print("Response:", llama_response)

  # JSON 파서 설정
  parser = JsonOutputParser()

  # 결과 파싱
  parsed_response = parser.parse(llama_response)

  # 관련성 평가 결과 출력
  print("Relevance evaluation:")
  for i, result in enumerate(parsed_response):
    print(f" Chunk {i+1}: {result['relevance']}")
else:
  print("Failed to get response. Status code:", response.status_code)
  print("Response:", response.text)
