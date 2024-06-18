import os
import openai
import chromadb
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document

# API 키 파일에서 읽기
def load_api_key(file_path='apikey.txt'):
  with open(file_path, 'r') as file:
    return file.read().strip()

# OpenAI API 키 설정
openai.api_key = load_api_key()

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

  return vectordb

# URL 목록을 로드하고 분할된 텍스트를 얻음
split_texts = load_and_split_urls(urls)

# 모든 분할된 텍스트를 하나의 리스트로 합침
all_texts = [part for doc in split_texts for part in doc]

# 문서 형식으로 변환
documents = [Document(page_content=text) for text in all_texts]

# 임베딩 함수 생성
embedding_function = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=openai.api_key)

# 임베딩을 Chroma DB에 저장
collection = save_to_chroma_db(documents, embedding_function)

# 결과 출력 (예시로 첫 번째 문서의 첫 번째 분할 텍스트를 출력)
for i, doc_splits in enumerate(split_texts):
  print(f"Document {i+1} split parts:")
  for j, split_part in enumerate(doc_splits):
    print(f" Part {j+1}: {split_part[:200]}...")  # 첫 200자만 출력