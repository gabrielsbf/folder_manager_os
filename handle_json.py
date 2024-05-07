import json
import env

def read_file(file_name, folder=env.PROJECT_PATH) -> dict | list:
	with open(folder + file_name, 'r') as fd:
		json_obj = json.load(fd)
	return json_obj

def write_file(json_obj: list[dict] | dict, file_name: str, folder=env.PROJECT_PATH) -> None:
	with open(folder + file_name, 'w') as fd:
		json.dump(json_obj, fd)

def update_file(json_obj: list[dict] | dict, file_name: str, folder=env.PROJECT_PATH):
	to_concat = read_file(file_name, folder)

	if type(to_concat) == dict and type(json_obj) == dict:
		for key, value in json_obj.items():
			to_concat.update({key:value})
	elif type(to_concat) == list and type(json_obj) == list:
		for arr in json_obj:
			to_concat.append(arr)
	else:
		raise TypeError("the json object given as argument is neither a dict neither a list")
	write_file(to_concat, file_name, folder)

# test_program = [{'blabla': 'bla'}, {'e': 'tudo mais'}]


# update_file(test_program, 'client_alias.json')
		