from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

DB_PATH = "./chroma_db"
COLLECTION_NAME = "interview_questions_v2"


# Question bank organized by domain
QUESTION_BANK = {
    "Python": [
        "What are the main features of Python?",
        "What is the difference between a list and a tuple?",
        "What is a Python dictionary, and when would you use it?",
        "What is the purpose of a function in Python?",
        "What is the difference between a for loop and a while loop?"
    ],

    "SQL": [
        "What is SQL, and what is it used for?",
        "What is the difference between a primary key and a foreign key?",
        "Explain the difference between WHERE and HAVING.",
        "What is the difference between INNER JOIN and LEFT JOIN?",
        "What is database normalization?"
    ],

    "Machine Learning": [
        "What is machine learning?",
        "Explain supervised and unsupervised learning.",
        "What are features and labels?",
        "What is overfitting?",
        "What is the purpose of training and testing data?"
    ],

    "Deep Learning": [
        "What is deep learning?",
        "What is an artificial neural network?",
        "What is an activation function?",
        "What is backpropagation?",
        "What is the difference between an epoch and a batch?"
    ],

    "Natural Language Processing": [
        "What is natural language processing?",
        "What is tokenization?",
        "What is the difference between stemming and lemmatization?",
        "What is a stop word?",
        "What is named entity recognition?"
    ],

    "Transformers": [
        "What is the Transformer architecture?",
        "What is self-attention?",
        "Why is positional encoding used in Transformers?",
        "What is the difference between an encoder and a decoder?",
        "What is multi-head attention?"
    ],

    "Generative AI": [
        "What is Generative AI?",
        "What is a large language model?",
        "What is prompt engineering?",
        "What is the difference between zero-shot and few-shot prompting?",
        "What is an AI hallucination?"
    ],

    "RAG": [
        "What is Retrieval-Augmented Generation?",
        "Why does a RAG system use a knowledge base?",
        "What are document chunks?",
        "What are embeddings?",
        "What is semantic search?"
    ],

    "LangChain": [
        "What is LangChain?",
        "What is a document loader?",
        "What is a text splitter?",
        "What is a retriever in a RAG application?",
        "What is a vector store?"
    ]
}


def build_vector_database():

    print("Preparing interview questions...")

    documents = []

    for domain, questions in QUESTION_BANK.items():

        for question in questions:

            documents.append(
                Document(
                    page_content=question,
                    metadata={"domain": domain}
                )
            )

    print("Total questions:", len(documents))

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=DB_PATH
    )

    print("New question database created successfully!")

    return vector_store


def load_rag_system():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )


def retrieve_questions(domain, query, k=3):

    vector_store = load_rag_system()

    results = vector_store.similarity_search(
        query,
        k=k,
        filter={"domain": domain}
    )

    return results


if __name__ == "__main__":
    build_vector_database()