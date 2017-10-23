import json
import functools

def to_json(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        result = json.dumps(*args, **kwargs)
        return result
    return wrapped


@to_json
def get_data(num_list):
    return sum(num_list)
