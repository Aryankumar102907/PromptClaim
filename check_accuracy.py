import json
from utils.decision_engine import get_decision_for_document_and_query

def run_accuracy_check(test_cases_file="test_cases.json"):
    with open(test_cases_file, 'r') as f:
        test_cases = json.load(f)

    total_tests = len(test_cases)
    correct_decisions = 0
    correct_justification_keywords = 0

    print(f"Running {total_tests} accuracy tests...")

    for i, test_case in enumerate(test_cases):
        doc_name = test_case["document"]
        query = test_case["query"]
        expected_decision = test_case["expected_decision"]
        expected_keywords = test_case.get("expected_justification_keywords", [])

        print(f"\n--- Test Case {i+1}/{total_tests} ---")
        print(f"Document: {doc_name}, Query: '{query}'")

        try:
            actual_output = get_decision_for_document_and_query(doc_name, query)
            
            if "error" in actual_output:
                print(f"  Error processing test case: {actual_output['error']}")
                continue

            actual_decision = actual_output.get("decision")
            actual_justification_text = json.dumps(actual_output.get("justification", [])) # Convert list of dicts to string for keyword search

            # Check decision
            if actual_decision == expected_decision:
                correct_decisions += 1
                print(f"Decision: PASSED (Expected: {expected_decision}, Actual: {actual_decision})")
            else:
                print(f"Decision: FAILED (Expected: {expected_decision}, Actual: {actual_decision})")

            # Check justification keywords
            justification_keywords_match = True
            for keyword in expected_keywords:
                if keyword.lower() not in actual_justification_text.lower():
                    justification_keywords_match = False
                    print(f"  Justification Keyword Missing: '{keyword}'")
            
            if justification_keywords_match:
                correct_justification_keywords += 1
                print("  Justification Keywords: PASSED")
            else:
                print("  Justification Keywords: FAILED")

        except Exception as e:
            print(f"  An unexpected error occurred: {e}")

    print("\n--- Summary ---")
    print(f"Decision Accuracy: {correct_decisions}/{total_tests} ({correct_decisions/total_tests:.2%})")
    print(f"Justification Keyword Coverage: {correct_justification_keywords}/{total_tests} ({correct_justification_keywords/total_tests:.2%})")

if __name__ == "__main__":
    run_accuracy_check()
