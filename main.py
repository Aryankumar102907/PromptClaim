import os
import json
from pathlib import Path
from dotenv import load_dotenv

from utils.decision_engine import get_decision_for_document_and_query
from core.config import DOCUMENTS_DIR

load_dotenv()

def main():
    while True:
        policy_filename = input(f"Enter the policy document name (e.g., BAJHLIP23020V012223.pdf) or 'exit' to quit: ").strip()

        if policy_filename.lower() == 'exit':
            break

        print(f"Successfully loaded document: {policy_filename}")

        while True:
            user_query = input(f"\nEnter your query for '{policy_filename}' (or 'back' to choose another document): ").strip().strip('"').strip("' ")

            if user_query.lower() == 'back':
                break
            if not user_query:
                continue

            decision_output = get_decision_for_document_and_query(policy_filename, user_query)
            
            print("\n=== Decision Output ===\n")
            if "error" in decision_output:
                print(f"Error: {decision_output['error']}")
                if "raw_output" in decision_output:
                    print("Raw output:")
                    print(decision_output["raw_output"])
            else:
                print(json.dumps(decision_output, indent=2))
            print("\n" + "="*40 + "\n")

if __name__ == "__main__":
    main()


def main():
    while True:
        policy_filename = input(f"Enter the policy document name (e.g., BAJHLIP23020V012223.pdf) or 'exit' to quit: ").strip()

        if policy_filename.lower() == 'exit':
            break

        print(f"Successfully loaded document: {policy_filename}")

        while True:
            user_query = input(f"\nEnter your query for '{policy_filename}' (or 'back' to choose another document): ").strip().strip('"').strip("'")

            if user_query.lower() == 'back':
                break
            if not user_query:
                continue

            decision_output = get_decision_for_document_and_query(policy_filename, user_query)
            
            print("\n=== Decision Output ===\n")
            if "error" in decision_output:
                print(f"Error: {decision_output['error']}")
                if "raw_output" in decision_output:
                    print("Raw output:")
                    print(decision_output["raw_output"])
            else:
                print(json.dumps(decision_output, indent=2))
            print("\n" + "="*40 + "\n")

if __name__ == "__main__":
    main()
