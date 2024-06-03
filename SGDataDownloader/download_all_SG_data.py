import json
from download_dataseries import return_data_series_json
from utils import element_to_csv_convertor, find_metadata
import re
from typing import *
from get_metadata import get_metadata

def main():
    file_path = "list_of_aggregations.json"
    with open(file_path, 'r') as file:
        data_aggregation_list = json.load(file)
    # process each aggregation 
    for aggregation in data_aggregation_list:
        # this is the actual data of the series
        data_agg_dict = return_data_series_json(aggregation['dataseries_id'])

        # this is the metadata for each series
        metadata:Dict = get_metadata(aggregation['dataseries_id'])

        # make mappings for index to series, and vice versa
        index_to_element: Dict[str, str] = {}
        element_to_index: Dict[str, str] = {}
        for series_name in (metadata['Data']['records']['row']):
            index_to_element[series_name['seriesNo']] = series_name['rowText']
            element_to_index[series_name['rowText']] = series_name['seriesNo']

        # list of subseries in each series
        new_element_list = list(data_agg_dict.keys())

        # store mappings of series name to CSV for metadata processing later
        element_name_to_csv:Dict = {}
        for i in range(len(new_element_list)):
            # for each subseries in new_element_list, write it to a csv
            aggregation_name = aggregation['internal_name']
            csv_name = aggregation_name.replace(' ', '_') + '_'+ re.sub(r'_+', '_', new_element_list[i].replace(' ', '_').replace('-', '')) 
            element_name_to_csv[new_element_list[i]] = csv_name + '.csv'
            element_to_csv_convertor(csv_name, data_agg_dict[new_element_list[i]])
        
        elements_list = list(element_name_to_csv.keys())
        # map CSV to metadata
        for i in range(len(elements_list)):
            meta_data = find_metadata(elements_list[i], index_to_element, element_to_index, element_name_to_csv, aggregation['internal_name'])
            print(meta_data)



    return

main()
