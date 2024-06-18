import os
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# URL 목록
urls = [
  "https://lilianweng.github.io/posts/2023-06-23-agent/",
  "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
  "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

def cache_file_path(url):
  """ URL을 기반으로 캐시 파일 경로 생성 """
  filename = url.split('/')[-2] + '.txt'
  return os.path.join('cache', filename)

def load_and_cache_document(url):
  """ 문서를 로드하고 캐시에 저장 """
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

# URL 목록을 로드하고 분할된 텍스트를 얻음
split_texts = load_and_split_urls(urls)

# 결과 출력 (예시로 첫 번째 문서의 첫 번째 분할 텍스트를 출력)
for i, doc_splits in enumerate(split_texts):
  print(f"Document {i+1} split parts:")
  for j, split_part in enumerate(doc_splits):
    print(f" Part {j+1}: {split_part[:200]}...")  # 첫 200자만 출력
