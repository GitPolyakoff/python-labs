def filter_objects(objects, predicate):
    return list(filter(predicate, objects))

def transform_objects(objects, operation):
    return list(map(operation, objects))

def sort_objects(objects, key_function, reverse=False):
    return sorted(objects, key=key_function, reverse=reverse)

def check_condition_any(objects, predicate):
    return any(predicate(obj) for obj in objects)