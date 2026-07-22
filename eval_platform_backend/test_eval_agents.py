import asyncio
import unittest

from src.agents.eval_agents import (
    accuracy_judge_agent,
    hallucination_detection_agent,
    relevance_judge_agent,
)


class EvaluationAgentTests(unittest.TestCase):
    def test_grounded_answer_is_accurate_without_hallucination(self):
        context = ["The Battle of Hastings was fought in 1066 and led to the Norman Conquest of England."]
        answer = "The Battle of Hastings was fought in 1066 and led to the Norman Conquest of England."
        accuracy = asyncio.run(accuracy_judge_agent(context, answer))
        hallucination = asyncio.run(hallucination_detection_agent(context, answer))
        self.assertEqual(accuracy.accuracy_score, 1.0)
        self.assertFalse(hallucination.is_hallucinated)
        self.assertEqual(hallucination.hallucination_score, 0.0)

    def test_unsupported_claim_is_flagged(self):
        context = ["The Roman Empire was founded in 27 BC. Rome was its capital."]
        answer = "The Roman Empire was founded in 27 BC and its capital was Constantinople."
        accuracy = asyncio.run(accuracy_judge_agent(context, answer))
        hallucination = asyncio.run(hallucination_detection_agent(context, answer))
        self.assertEqual(accuracy.accuracy_score, 0.5)
        self.assertTrue(hallucination.is_hallucinated)
        self.assertEqual(hallucination.flagged_statements, ["its capital was Constantinople."])

    def test_no_context_never_counts_as_evidence(self):
        answer = "Water boils at 100 degrees Celsius at sea level."
        accuracy = asyncio.run(accuracy_judge_agent([], answer))
        hallucination = asyncio.run(hallucination_detection_agent([], answer))
        self.assertEqual(accuracy.accuracy_score, 0.0)
        self.assertTrue(hallucination.is_hallucinated)

    def test_relevance_is_independent_of_grounding(self):
        relevance = asyncio.run(
            relevance_judge_agent("What is the capital of France?", "The capital of France is Paris.")
        )
        self.assertGreaterEqual(relevance.relevance_score, 4)


if __name__ == "__main__":
    unittest.main()
