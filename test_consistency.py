import json
from utils.decision_engine import get_decision_for_document_and_query

policy_filename = "EDLHLGA23009V012223.pdf"
user_query = "28F, 2nd trimester pregnancy, Mumbai, pre-hospitalization maternity cover, 6-month policy"
num_runs = 10

results = []
print(f"Running query '{user_query}' for document '{policy_filename}' {num_runs} times...")

for i in range(num_runs):
    print(f"Run {i+1}/{num_runs}...")
    decision_output = get_decision_for_document_and_query(policy_filename, user_query)
    results.append(decision_output.get("decision")) # Only store the 'decision' field

# Check for consistency of the 'decision' field
first_decision = results[0]
is_consistent = True
for i in range(1, num_runs):
    if results[i] != first_decision:
        is_consistent = False
        print(f"Inconsistency found at run {i+1}:")
        print(f"  Expected decision: {first_decision}")
        print(f"  Got decision: {results[i]}")
        break

if is_consistent:
    print(f"All {num_runs} runs produced the same decision: {first_decision}.")
else:
    print(f"Decisions were INCONSISTENT across {num_runs} runs.")
print("All decisions:", results)
