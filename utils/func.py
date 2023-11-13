import psycopg2


def get_nested_value(json, keys, default=None):
    """
    Helper function to safely access nested keys in the JSON data.

    Args:
        keys (list): List of keys to traverse the nested structure.
        default: Default value to return if the key is not found or an error occurs.

    Returns:
        The value associated with the nested key or the default value.
    """
    try:
        value = json
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return default
