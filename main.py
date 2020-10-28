from src.parser import Parser

print('Type a request')
request = input('>> ')
print('1 -- Literature\n   1.1 -- Books\n   1.2 -- MeSH\n   '
      '1.3 -- NLM Catalog\n   1.4 -- PubMed\n   1.5 -- PubMed Central')
catalog = input('>> ')
Parser.get_request(request, catalog)