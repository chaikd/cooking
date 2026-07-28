def snake_to_camel(name: str):
    parts = name.split("_")
    return parts[0] + "".join(i.title() for i in parts[1:])


def camelize(list):
    old_props = list[0].keys()
    props = [snake_to_camel(p) for p in old_props]
    return [dict(zip(props, row.values())) for row in list]