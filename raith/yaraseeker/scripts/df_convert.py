# YaraSeeker
# Author: Steven Folek | @Pir00t
# Description: Convert seeker output into a dataframe
# Version: 1.0

import pandas as pd

def convert(data):
	file_data = []
	current_file = None
	current_rule = None
	current_identifier = None
	current_string = None
	current_offset = None

	for item in data:
		if item.startswith('File:'):
			current_file = item.split(':', 1)[1].strip()
		elif item.startswith('Rule:'):
			current_rule = item.split(':', 1)[1].strip()
		elif item.startswith('Identifier:'):
			current_identifier = item.split(':', 1)[1].strip()
		elif item.startswith('String:'):
			current_string = item.split(':', 1)[1].strip()
		elif item.startswith('Offset:'):
			current_offset = item.split(':', 1)[1].strip()
			file_data.append({
				'File': current_file,
				'Rule': current_rule,
				'Identifier': current_identifier,
				'String': current_string,
				'Offset': current_offset
			})

	return pd.DataFrame(file_data)