from src.parser import Parser

print('Type a request')
request = input('>> ')
print('1 -- Literature\n   1.1 -- Books\n   1.2 -- MeSH\n   '
      '1.3 -- NLM Catalog\n   1.4 -- PubMed\n   1.5 -- PubMed Central')
print('2 -- Genes\n   2.1 -- Gene\n   2.2 -- GEO DataSets\n   '
      '2.3 -- GEO Profiles\n   2.4 -- Homologene\n   2.5 -- PopSet')
print('3 -- Genomes\n   3.1 -- Assembly\n   3.2 -- Biocollections\n   '
      '3.3 -- Bioproject\n   3.4 -- Biosample\n   3.5 -- Genome\n   3.6 -- Nucleotide\n   3.7 -- SRA')
print('4 -- Proteins\n   4.1 -- Conversed Domains\n   4.2 -- Identical Protein Group\n   4.3 -- Protein'
      '4.4 -- Protein Clusters\n   4.5 -- Spaarcle\n   4.6 -- Structure\n')
catalog = input('>> ')
print('             ' * 100000)
Parser.get_request(request, catalog)