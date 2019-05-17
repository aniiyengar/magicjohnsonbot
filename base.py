
import random

def parse_obj_path(obj, path):
	parts = path.split('.')
	if len(parts) == 0:
		return None

	ptr = obj
	for part in parts:
		if part.isdigit():
			p = int(part)
			if not isinstance(ptr, list):
				return None
			elif len(ptr) < p:
				return None
			else:
				ptr = ptr[p - 1]
		else:
			if part not in ptr:
				return None
			else:
				ptr = ptr[part]
	return ptr

class BaseScore:

	def __init__(self):
		with open('%s_templates.txt' % self.type) as f:
			self.templates = f.read().split('\n')

	def get_status(self):
		winner, loser = self.get_game()
		data = { 'winner': winner, 'loser': loser }

		temp = random.choice(self.templates)
		l = len(temp)
		final = ''

		i = 0
		while i < l:
			if temp[i] != '[':
				final = final + temp[i]
			else:
				i += 1
				s = i
				while temp[i] != ']':
					i += 1
				conv = parse_obj_path(data, temp[s:i])
				final = final + str(conv)
			i += 1

		return final

