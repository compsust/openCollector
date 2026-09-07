from typing import Any


def get_attribute(
    config: dict[str, Any], attribute: str, config_name: str, required: bool = True
) -> Any:
    """
    Retrieves the attribute from the config, or
    raises an error if it does not exist and the attribute is required.

    Args:
        config: The config to retrieve from.
        attribute: The name of the attribute.
        config_name: The name of the config.
        required: If true, an exception will be raised
            if the attribute doesn't exist.

    Raises:
        ValueError: Raised if the attribute does not
            exist within the config and is required.

    Returns:
        The config attribute, or None if it does not exist and is not required.
    """
    try:
        value = config[attribute]
    except KeyError:
        if required:
            raise ValueError(
                f"Config '{config_name}' missing required parameter '{attribute}'."
            )
        else:
            return None

    if value is None and required:
        raise ValueError(
            f"Config '{config_name}' missing required parameter '{attribute}'."
        )

    return value
