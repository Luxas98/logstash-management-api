from elasticsearch import Elasticsearch
import glob
import json

es = Elasticsearch(hosts=["http://localhost:9200"])
mappings = glob.glob("*.json")

# mappings = ["Patient.mapping.json"]

with open('FhirIndexTemplate.json') as fhir_template_file:
    fhir_template = json.load(fhir_template_file)
    es.indices.put_template('fhirtemplate', fhir_template)

for mapping_file in mappings:
    with open(mapping_file, 'r') as mf:
        mapping_json = json.load(mf)
        try:
            es_mapping = mapping_json['mapping']
        except KeyError:
            print(f'Faile to load: {mapping_file}')
            continue

        index_name = 'fhir' + mapping_json['resourceType']
        history_index_name = f'{index_name.lower()}_history'

        print(index_name)
        if not es.indices.exists(index_name.lower()):
            es.indices.create(index_name.lower(), {"mappings": es_mapping})

        else:
            es.indices.delete(index_name.lower())
            es.indices.create(index_name.lower(), {"mappings": es_mapping})

        if not es.indices.exists(history_index_name):
            es.indices.create(history_index_name, {"mappings": es_mapping})
        else:
            es.indices.delete(history_index_name)
            es.indices.create(history_index_name, {"mappings": es_mapping})

