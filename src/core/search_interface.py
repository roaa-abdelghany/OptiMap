from .result_schema import validate_result

def run_search(search_function, graph, start, goal):
    result = search_function(graph, start, goal)
    return validate_result(result)
