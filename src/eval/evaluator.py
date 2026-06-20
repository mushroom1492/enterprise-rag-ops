import os
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevance,
    context_precision,
    context_recall,
)
from datasets import Dataset
from src.core.rag_engine import RAGEngine

class RAGEvaluator:
    def __init__(self):
        self.engine = RAGEngine()
        self.metrics = [
            faithfulness,
            answer_relevance,
            context_precision,
            context_recall,
        ]

    def run_evaluation(self, test_dataset: list[dict]):
        """
        Run Ragas evaluation on a test dataset.
        test_dataset: list of {"question": "...", "ground_truth": "..."}
        """
        questions = [item["question"] for item in test_dataset]
        ground_truths = [[item["ground_truth"]] for item in test_dataset]
        
        answers = []
        contexts = []
        
        for q in questions:
            result = self.engine.query(q)
            answers.append(result["result"])
            contexts.append([doc.page_content for doc in result["source_documents"]])
            
        data = {
            "question": questions,
            "answer": answers,
            "contexts": contexts,
            "ground_truth": ground_truths
        }
        
        dataset = Dataset.from_dict(data)
        result = evaluate(dataset, metrics=self.metrics)
        
        return result

if __name__ == "__main__":
    # Example usage for CI/CD or local testing
    evaluator = RAGEvaluator()
    sample_data = [
        {
            "question": "What is the main topic of the project?",
            "ground_truth": "The project is about Enterprise RAG Ops demonstrating LLMOps, RAG, and DevOps."
        }
    ]
    # Note: This requires documents to be ingested first
    # print(evaluator.run_evaluation(sample_data))
