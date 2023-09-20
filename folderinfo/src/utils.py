def reduce_tokens(data):
    """
    The `reduce_tokens` function takes in a dictionary of data and returns a reduced version of the data
    with specific keys and values.

    :param data: The `data` parameter is a dictionary that contains information about a code file. It
    can have the following keys:
    :return: The function `reduce_tokens` returns a new dictionary `new_data` that contains reduced
    information from the input `data`. The reduced information includes the header, functions, classes,
    and imports from the input `data`.
    """
    new_data = {}

    # Handle header
    if data.get("header"):
        new_data["h"] = data["header"].split("\n")[0]

    # Handle functions
    if data.get("functions"):
        new_data["f"] = [
            {
                "n": func["name"],
                "l": func["line"],
                **({"d": func["docstring"]} if func.get("docstring") else {}),
                **({"a": func["calls"]} if func.get("calls") else {}),
            }
            for func in data["functions"]
        ]

    # Handle classes
    if data.get("classes"):
        new_data["c"] = [
            {
                "n": cls["name"],
                "l": cls["line"],
                **({"d": cls["docstring"]} if cls.get("docstring") else {}),
                **({"m": cls["methods"]} if cls.get("methods") else {}),
            }
            for cls in data["classes"]
        ]

    # Handle imports
    if data.get("imports"):
        new_data["i"] = [
            {"n": imp["name"], **({"m": imp["module"]} if "module" in imp else {})}
            if isinstance(imp, dict)
            else imp["name"]
            for imp in data["imports"]
        ]

    return new_data
