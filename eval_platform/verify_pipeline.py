import chromadb
from uuid import uuid4
from datasets import load_dataset

client = chromadb.PersistentClient(path="./chroma_db_storage")
collection = client.get_or_create_collection(name="large_user_verification")

def live_unfiltered_test():
    print("Step 1: Fetching 1,000 raw paragraphs from SQuAD...")
    dataset = load_dataset("rajpurkar/squad", split="train")
    
    raw_contexts = []
    for item in dataset:
        context = item["context"]
        if context not in raw_contexts:
            raw_contexts.append(context)
        if len(raw_contexts) == 1000:
            break

    print("Step 2: Ingesting 1,000 paragraphs into ChromaDB...")
    ids = [str(uuid4()) for _ in raw_contexts]
    collection.add(documents=raw_contexts, ids=ids)
    print("Ingestion complete. The database now has a massive variety of topics.")
    
    print("\n==================================================")
    print("Step 3: RUN YOUR MEANING TEST")
    print("==================================================")
    user_query = input("Enter your search query: ")
    
    print(f"\nSearching database for your live query: '{user_query}'...")
    results = collection.query(query_texts=[user_query], n_results=1)
    
    print("\n=== MATCHING RETRIEVED PARAGRAPH ===")
    print(results["documents"][0][0])
    print("====================================")

if __name__ == "__main__":
    live_unfiltered_test()