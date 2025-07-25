#!/usr/bin/env python
"""Generates the ldraw.library.parts namespace."""
import codecs
import os

import pystache
from attridict import AttriDict
from progress.bar import Bar

from ldraw.parts import PartError
from ldraw.resources import _get_resource_content
from ldraw.utils import camel, clean, ensure_exists

SECTION_SEP = "#|#"


def gen_parts(parts, library_path):
    """Generate the ldraw.library.parts namespace modules."""
    print("generate ldraw.library.parts, this might take a long time...")
    parts_dir = ensure_exists(os.path.join(library_path, "parts"))

    recursive_gen_parts(parts.parts, parts_dir)


def recursive_gen_parts(parts_parts, directory):
    """Recursively generate parts modules for nested part categories."""
    for name, value in list(parts_parts.items()):
        if isinstance(value, AttriDict):
            recurse = False
            for v in value.values():
                if len(v) > 0:
                    recurse = True

            if recurse:
                subdir = os.path.join(directory, name)
                ensure_exists(subdir)
                recursive_gen_parts(value, subdir)

    sections = {
        name: value
        for name, value in parts_parts.items()
        if not isinstance(value, AttriDict)
    }

    module_parts = {}
    for section_name, section_parts in sections.items():
        if section_name == "":
            continue
        for desc, code in section_parts.items():
            module_parts[desc] = code  # noqa: PERF403

        parts_py = os.path.join(directory, f"{section_name}.py")
        part_str = section_content(section_parts, section_name)
        with codecs.open(parts_py, "w", encoding="utf-8") as generated_file:
            generated_file.write(part_str)

    generate_parts__init__(directory=directory, sections=sections)


def generate_parts__init__(directory, sections):
    """Generate __init__.py to make submodules in ldraw.library.parts."""
    parts__init__str = parts__init__content(sections)

    parts__init__ = os.path.join(directory, "__init__.py")
    ensure_exists(os.path.dirname(parts__init__))

    with codecs.open(parts__init__, "w", encoding="utf-8") as parts__init__file:
        parts__init__file.write(parts__init__str)


def parts__init__content(sections):
    """Generate the content for __init__.py files in parts modules."""
    sections = [
        {"module_name": module_name} for module_name in sections if module_name != ""
    ]
    return pystache.render(PARTS__INIT__TEMPLATE, context={"sections": sections})


def section_content(section_parts, section_key):
    """Generate the content for a section of parts."""
    parts_list = []
    progress_bar = Bar("section %s ..." % str(section_key), max=len(section_parts))
    for description in section_parts:
        parts_list.append(get_part_dict(section_parts, description))
        progress_bar.next()
    progress_bar.finish()
    parts_list = [x for x in parts_list if x != {}]
    parts_list.sort(key=lambda o: o["description"])
    return pystache.render(PARTS_TEMPLATE, context={"parts": parts_list})


PARTS__INIT__TEMPLATE = pystache.parse(
    _get_resource_content(os.path.join("templates", "parts__init__.mustache")),
)
PARTS_TEMPLATE = pystache.parse(
    _get_resource_content(os.path.join("templates", "parts.mustache")),
)


def get_part_dict(parts_parts, description):
    """Get a dict context for a part."""
    try:
        code = parts_parts[description]
        return {
            "description": description,
            "class_name": clean(camel(description)),
            "code": code,
        }
    except (PartError, KeyError):
        return {}
