from utils.decision_engine import get_decision_for_document_and_query
import json

policy_filename = 'EDLHLGA23009V012223.pdf'
user_query = '28F, 2nd trimester pregnancy, Mumbai, pre-hospitalization maternity cover, 6-month policy'

decision = get_decision_for_document_and_query(policy_filename, user_query)
print(json.dumps(decision, indent=2))