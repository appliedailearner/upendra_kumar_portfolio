import csv
f = open(r'data/rto_rpo_decision_matrix_expanded_cleaned.csv', encoding='utf-8')
rows = list(csv.DictReader(f))
f.close()
print('RTO Band:', sorted(set(r['RTO Band'] for r in rows if r.get('RTO Band'))))
print('RPO Band:', sorted(set(r['RPO Band'] for r in rows if r.get('RPO Band'))))
print('Region:', sorted(set(r['Region Preference'] for r in rows if r.get('Region Preference'))))
print('Criticality:', sorted(set(r['Criticality'] for r in rows if r.get('Criticality'))))
print('Topology:', sorted(set(r['Topology Preference'] for r in rows if r.get('Topology Preference'))))
