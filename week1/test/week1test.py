
hits=[
      { 
        '_index': 'searchml_ltr', 
        '_id': 'doc_e', 
        '_score': 0.0, 
        '_source': {
          'id': 'doc_e', 
          'title': 'Pigs in a Blanket and Other Recipes',
          'price': '27.50',
          'in_stock': True,
          'body': "Pigs in a blanket aren't as cute as you would think given it's a food and not actual pigs wrapped in blankets.",
          'category': 'instructional'
        }, 
        'fields': {
          '_ltrlog': [
            {
              'log_entry': [
                {'name': 'title_query', 'value': 1.1272218}, 
                {'name': 'body_query', 'value': 2.2908108}, 
                {'name': 'price_func', 'value': 27.5}
                ]
              
            }
          ]
        }, 
        'matched_queries': ['logged_featureset']
      }
    ]

log_entries = hits[0]['fields']['_ltrlog'][0]['log_entry']

print(log_entries)

for entry in log_entries:
    if entry['name'] == "title_query" :
        print(entry['value'])
