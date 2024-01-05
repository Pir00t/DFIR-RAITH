# YaraSeeker
# Author: Steven Folek | @Pir00t
# Description: Yara scanner for testing a rule file (or rule files) against a dir of files or single file with interactive output
# Version: 1.0

import ipywidgets as widgets
import magic
import os
import yara
from common.validate import validate_path
from IPython.display import display
from scripts.df_convert import convert


def init_Yara():
	# Textbox for file or directory path
	path_textbox = widgets.Text(value='', placeholder='Enter file or directory path', description='Path:',disabled=False)

	# Textbox for Yara rules file path
	rules_textbox = widgets.Text(value='', placeholder='Enter Yara rule(s) path', description='Rule(s):', disabled=False)

	# Display widgets
	display(path_textbox, rules_textbox)

	output = widgets.Output()
	yara_vars = {'path': '', 'rules_file': '', 'path_type': '', 'rules_file_type': ''}

	def on_button_click(b):
		nonlocal yara_vars

		yara_vars['path'] = path_textbox.value
		yara_vars['rules_file'] = rules_textbox.value
		output.clear_output()
		with output:
			# Get values from widgets
			path = path_textbox.value
			rules_file = rules_textbox.value
	
			# Validate paths
			yara_vars['path_type'] = validate_path(path)
			yara_vars['rules_file_type'] = validate_path(rules_file)

			if yara_vars['path_type'] == 'invalid':
				print(f'\n[!] Invalid path: {path}')
			elif yara_vars['rules_file_type'] == 'invalid':
				print(f'\n[!] Invalid rules file path: {rules_file}')
			else:
				print('\n[*] Variables initialized')

	# Create a button to trigger the action
	button = widgets.Button(description="Initialize Yara")
	button.on_click(on_button_click)
	
	display(button)
	display(output)

	return yara_vars

def is_binary_file(file_path):
	try:
		mime = magic.Magic()
		file_type = mime.from_file(file_path)
		return 'executable' in file_type.lower()
	except IOError:
		return False

def rule_compiler(rule_path, rules_file_type):
	try:
		if rules_file_type == 'directory':
			rule_files = []
			yara_filenames = []
			for rf in os.listdir(rule_path):
				if rf.endswith('.yar') or rf.endswith('.yara'):
					rule_files.append(f'{rule_path}{rf}')

			if rule_files:
				print(f'[+] Found {len(rule_files)} YARA rule files')
				for f in rule_files:
					splitname = os.path.split(f)[1]
					yara_filenames.append(os.path.splitext(splitname)[0])
					
				rules = yara.compile(filepaths=dict(zip(yara_filenames, iter(rule_files))))
				print('[*] Compiled successfully')
				return rules
			else:
				print('[!] No YARA rule files found in the given directory')
				return None
		else:
			rules = yara.compile(filepath=rule_path)
			print('[*] Compiled successfully')
			return rules

	except Exception as e:
		print(f'[!] Error compiling rule file: {e}')
		return None

def scan_dir(dir_path, rules):
	yara_matches = []

	for root, dirs, files in os.walk(dir_path):
		for filename in files:
			file_path = os.path.join(root, filename)

			if is_binary_file(file_path):
				file_matches = scan_file(file_path, rules)
				if file_matches:
					yara_matches.extend(file_matches)

	return yara_matches

def scan_file(file_path, rules):
	yara_matches = []
	
	matches = rules.match(file_path)
	
	if matches:
		for i in range(len(matches)):
			data = f'File:{file_path}\n'
			for x in range(len(matches[i].strings)):
				data += f'Rule:{matches[i].rule}\n'
				data += f'Identifier:{matches[i].strings[x].identifier}\n'
				for y in range(len(matches[i].strings[x].instances)):
					data += f'String:{matches[i].strings[x].instances[y]}\n'
					data += f'Offset:{matches[i].strings[x].instances[y].offset}\n'
				
				yara_matches.append(data)

	return yara_matches

def match_split(matches):
	data = []
	for entry in matches:
		data.extend(entry.splitlines())

	return convert(data)
 