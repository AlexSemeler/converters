import os
from glob import glob
import lxml.etree as xml_tree

def write_item(item, file):
    """
    Write a single item to the file. If the item is 0, write 'No Data'.
    """
    if item != 0:
        file.write(f'{item}\t')
    else:
        file.write('No Data\t')

def write_list(items, file):
    """
    Write a list of items to the file. Items are comma-separated.
    If the list is empty, write 'No Data'.
    """
    if items:
        for i, item in enumerate(items):
            if i != len(items) - 1:
                file.write(f'{item}, ')
            else:
                file.write(f'{item}\t')
    else:
        file.write('No Data\t')

# Path to the folder containing XML files
xml_folder = ''
# Output CSV file path
output_file_path = 'output_tuples_pangea.csv'

# Header fields for the output CSV
aux_header_list = ['date', 'title', 'language', 'publisher', 'format',
                   'identifier', 'rights', 'source', 'type', 'creator', 'subject','setspec']

# Dictionary to keep track of record counts per XML file
xml_record_counters = {}

# Open the output file for writing
with open(output_file_path, 'w', encoding='utf-8-sig') as output_file:
    # Write the header row to the output file
    output_file.write('\t'.join(aux_header_list) + '\n')

    # Iterate over all XML files in the specified folder
    for filename in glob(os.path.join(xml_folder, '*.xml')):
        short_name = os.path.splitext(os.path.basename(filename))[0]
        xml_record_counters[short_name] = 0
        print('Parsing:', short_name)

        try:
            # Parse the XML file
            context = xml_tree.iterparse(filename, events=("start", "end"))
            _, root = next(context)  # Get the root element
            for event, element in context:
                if event == "end" and element.tag == "record":
                    # Initialize a tuple to store the record data
                    writing_tuple = [0, 0, 0, 0, 0, 0, 0, 0, 0, [], []]

                    # Iterate over elements within the record
                    for item in element.iter():
                        if 'date' in item.tag:
                            if len(str(item.text).split('-')[0]) == 4:
                                writing_tuple[0] = str(item.text).split('-')[0]
                            continue
                        if 'creator' in item.tag:
                            writing_tuple[9].append(item.text)
                            continue
                        if 'subject' in item.tag:
                            writing_tuple[10].append(item.text)
                            continue
                        for index, header in enumerate(aux_header_list[1:8], start=1):
                            if header in item.tag:
                                writing_tuple[index] = item.text
                                break

                    # Write the collected data to the output file
                    for i in range(8):
                        write_item(writing_tuple[i], output_file)

                    write_list(writing_tuple[9], output_file)
                    write_list(writing_tuple[10], output_file)
                    output_file.write('\n')
                    xml_record_counters[short_name] += 1
                    root.clear()  # Clear the element and its children to free memory

            print('XML file parsed successfully:', short_name)
        except xml_tree.XMLSyntaxError:
            print(f'File "{short_name}" corrupted: Parsing aborted')

print(f'Approximately {sum(xml_record_counters.values())} rows written to {output_file_path}')
