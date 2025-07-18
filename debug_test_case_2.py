from utils.decision_engine import get_decision_for_document_and_query
import json

document = "CHOTGDP23004V012223.pdf"
query = "What is the waiting period for pre-existing diseases?"

decision_output = get_decision_for_document_and_query(document, query)

print(json.dumps(decision_output, indent=2))