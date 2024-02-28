import inspect


def get_object_entry_names(obj):
    names = []
    for name in dir(obj):
        if not name.startswith('__'):
            names.append(name)
    return names


def get_object_props(obj):
    dict = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith('__') and not inspect.ismethod(value):
            dict[name] = value
    return dict


def get_object_methods(obj):
    dict = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith('__') and inspect.ismethod(value):
            dict[name] = value
    return dict
