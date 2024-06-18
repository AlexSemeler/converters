# coding: utf-8
# Description of the RIS format: https://en.wikipedia.org/wiki/RIS_(file_format)
from codecs import open

# Open the output RIS file for writing
output_file = open('geophysics-Rede.ris', 'w', 'utf-8-sig')

# Open the input TSV file for reading
table = open('pangea-dc-xml-geophysics.tsv', 'r', 'utf-8-sig')
data_list = table.readlines()  # Read all lines from the TSV file
table.close()  # Close the input TSV file

# Process each line of the TSV file
for line in data_list:
    try:
        # Start a new RIS record
        output_file.write('TY  - Research data Metadata in PANGEA\n')

        # Split the line by tabs to get individual fields
        fields = line.split('\t')

        # Write the keyword field (assuming it is at index 10)
        output_file.write(f'KW  - {fields[10]}\n')

        # Write the label field (assuming it is at index 16)
        output_file.write(f'LB  - {fields[16]}\n')

        # Write additional keywords (assuming they are in the field at index -10, separated by semicolons)
        for keyword in fields[-10].split(';'):
            output_file.write(f'KW - {keyword}\n')

        # Write additional labels (assuming they are in the same field as additional keywords)
        for label in fields[-10].split(';'):
            output_file.write(f'LB - {label}\n')

        # Write DOI values (assuming they are in the field at index 3, separated by semicolons)
        for doi in fields[3].split(';'):
            output_file.write(f'DOI  - {doi}\n')

        # End the RIS record
        output_file.write('ER  - \n')
    except IndexError:
        # Skip the line if there are not enough fields
        continue

# Close the output RIS file
output_file.close()
