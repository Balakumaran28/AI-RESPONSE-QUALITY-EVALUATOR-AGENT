import chromadb
from uuid import uuid4
from datasets import load_dataset

client = chromadb.PersistentClient(path="./chroma_db_storage")
collection = client.get_or_create_collection(name="reference_knowledge_base")

def add_reference_chunks(chunks: list[str], dataset_name: str):
    generated_ids = [str(uuid4()) for _ in chunks]
    metadata_list = [{"source_dataset": dataset_name, "chunk_index": idx} for idx, _ in enumerate(chunks)]
    
    collection.add(
        documents=chunks,
        metadatas=metadata_list,
        ids=generated_ids
    )
    print(f"Successfully ingested {len(chunks)} chunks from '{dataset_name}' into ChromaDB.")

def query_reference_knowledge(query_text: str, top_k: int = 2):
    results = collection.query(
        query_texts=[query_text],
        n_results=top_k
    )
    return results

if __name__ == "__main__":
    print("Fetching dataset from Hugging Face...")
    hf_dataset = load_dataset("rajpurkar/squad", split="train")
    
    raw_paragraphs = list(set(hf_dataset["context"]))
    target_chunks = raw_paragraphs[:100]
    
    print("Starting ingestion pipeline...")
    add_reference_chunks(chunks=target_chunks, dataset_name="squad_huggingface")
    
    search_query = "What architectural styles or structures are mentioned in the historical records?"
    print(f"\nTesting live query: '{search_query}'")
    search_results = query_reference_knowledge(query_text=search_query, top_k=1)
    
    print(f"Retrieved Context: {search_results['documents'][0][0]}")