import asyncio
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.agents.eval_agents import (
    AccuracySchema,
    HallucinationSchema,
    RelevanceSchema,
    accuracy_judge_agent,
    hallucination_detection_agent,
    relevance_judge_agent,
)


SCENARIOS = [
    {
        "name": "Scenario A - The Perfect Grounding Match",
        "question": "What happened in the battle of Hastings?",
        "response": "The battle of Hastings was fought in 1066 and led to the Norman Conquest of England.",
        "context": [
            "The Battle of Hastings was fought in 1066.",
            "It led to the Norman Conquest of England.",
        ],
    },
    {
        "name": "Scenario B - The Hallucination Trapping Case",
        "question": "Summarize the key facts about the Roman Empire.",
        "response": "The Roman Empire was founded in 27 BC and its capital was Constantinople.",
        "context": [
            "The Roman Empire was founded in 27 BC.",
            "Rome was the capital of the Roman Empire.",
        ],
    },
    {
        "name": "Scenario C - The Pivot/Off-Topic Case",
        "question": "Explain the significance of the Rosetta Stone.",
        "response": "The Rosetta Stone was used to unlock the secrets of baking bread in ancient Egypt.",
        "context": [
            "The Rosetta Stone is an ancient Egyptian artifact that helped scholars decipher hieroglyphs.",
        ],
    },
]


async def run_scenarios() -> None:
    print("Starting isolated evaluation benchmark run...\n")
    for scenario in SCENARIOS:
        print(f"=== {scenario['name']} ===")
        relevance = await relevance_judge_agent(scenario["question"], scenario["response"])
        accuracy = await accuracy_judge_agent(scenario["context"], scenario["response"])
        hallucination = await hallucination_detection_agent(scenario["context"], scenario["response"])

        print(json.dumps(
            {
                "relevance": relevance.model_dump(),
                "accuracy": accuracy.model_dump(),
                "hallucination": hallucination.model_dump(),
            },
            indent=2,
        ))
        print()


if __name__ == "__main__":
    asyncio.run(run_scenarios())
