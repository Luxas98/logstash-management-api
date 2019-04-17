import json


def process_property(property_name, property_info):
    fields_list = []
    if 'properties' in property_info:
        for inner_property_name, inner_property_info in property_info[
            'properties'].items():
            nested_fields = process_property(inner_property_name,
                                             inner_property_info)
            for nested_field in nested_fields:
                fields_list.append(f'[{property_name}]{nested_field}')
    else:
        fields_list.append(f'[{property_name}]')

    return fields_list


def process_resource(resource_name):
    output_fields = []
    with open(
            f'fhir/elasticsearch/mappings/STU3/{resource_name}.mapping.json') as mapping_file:

        mappings = json.load(mapping_file)['mapping']['properties']

        for property_name, property_info in mappings.items():
            fields = process_property(property_name, property_info)
            output_fields.extend(fields)

    return output_fields
