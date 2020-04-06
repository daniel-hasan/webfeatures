

def get_class_by_name(name):
	components = name.split('.')
	module_name = ".".join(components[0:len(components)-1])
	mod = __import__(module_name)

	for comp in components[1:]:
		mod = getattr(mod, comp)
	return mod
