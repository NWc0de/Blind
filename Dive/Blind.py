"""
   Spencer Little (spencer@soursecurity.com)
"""

from Logger import LOGGER, LogLevel

import re

# limitations:
# line continuation characters (x = \
#                               5)
#
# variable declarations with type hints (x : int)
#
# parameters... which can (commonly) vary accross lines
r_class_definition = r"^\s*class\s+([A-Za-z0-9_-]+)(?:\(.*\))?"
r_func_definition = r"^\s*def\s+([A-Za-z0-9_-]+)\s*\(.*\)\s*:"
r_var_assignment = r"^\s*([A-Za-z0-9_-]+)\s*=.*"

def exists_in_dict(d, k):
    # I'm not sure if the "in" operator just does a linear search through
    # the keys of the hash table. I'm only using a hash table to avoid this
    # linear search, so I'm infering that raising a KeyError is a result
    # of actually doing the lookup in the hash table and not finding the
    # element.
    try:
        d[k]
        return True
    except KeyError:
        return False
    except Exception as e:
        LOGGER.log_event(f"Something strange happened will checking for {k} in {d}: {e.args[0]}", LogLevel.STOPPED_EXECUTING, do_assert=True)


def randomize_variables(source_as_string):
    stripped = strip_comments(source_as_string)
    randomized = stripped
    c_kwords = {}
    f_kwords = {}
    v_kwords = {}

    # FIXME:
    # deal with nested scope by check for multiple instances
    # with the same user defined nomenclature in different
    # scope. Optimally these would be randomized into unique
    # random names and made unique per scope since a user might
    # be able to incorrectly infer intuitive / semantic meaning
    # by observing the use of the variable, function or class
    # in one of the other scope(s)

    for line in stripped.split("\n"):
        class_m = re.match(r_class_definition, line)
        if not class_m is None and not exists_in_dict(c_kwords, class_m.group(1)):
            c_kwords[class_m.group(1)] = 0  # dummy value, exploiting the dict to use as a hashset
        
        func_m = re.match(r_func_definition, line)
        if not func_m is None and not exists_in_dict(f_kwords, func_m.group(1)):
            f_kwords[func_m.group(1)] = 0
        
        var_m = re.match(r_var_assignment, line)
        if not var_m is None and not exists_in_dict(v_kwords, var_m.group(1)):
            v_kwords[var_m.group(1)] = 0


    class_names = list(c_kwords.keys())
    for i in range(len(class_names)):
        randomized = randomized.replace(f" {class_names[i]}", f" RandClass{i}")
    func_names = list(f_kwords.keys())
    for i in range(len(func_names)):
        if func_names[i][:1] == '__':  # ignore special functions
            continue
        randomized = randomized.replace(f" {func_names[i]}", f" rand_func{i}")
    var_names = list(v_kwords.keys())
    for i in range(len(var_names)):
        # since upper case typically implies non-lexically enforced global semantics,
        # and these carry some meaning endemic to the source file itself and not based
        # on abstractions of underlying semantics, let's preserve case
        repl_name = f"RAND_VAR{i}" if var_names[i].isupper() else f"rand_var{i}"

        def repl_var(m):
            if m.group(0)[-1] == "=":
                return f"{repl_name}="
            elif m.group(0)[-1] == ".":
                return f"{repl_name}."
            else:
                return f"{repl_name} "
 
        randomized = re.sub(rf"{var_names[i]}(?:\s|=|\.)", repl_var, randomized)

    return randomized


def strip_comments(source_as_string):
    stripped = ""
    in_doc_string = False
    for line in source_as_string.split("\n"):
        if not re.match(r"^\s*\"{3}.*\"{3}", line) is None:
            continue

        if not in_doc_string and not re.match(r".*\"{3}$", line) is None:
            in_doc_string = True
            continue
        elif not re.match(r".*\"{3}$", line) is None:
            in_doc_string = False
            continue
        elif in_doc_string:
            continue


        seen_one_non_ws = False
        include = True
        stripped_line = ""
        for char in line:
            if char != " ":
                seen_one_non_ws = True
            if char == "#" and not seen_one_non_ws:
                include = False
                break
            elif char == "#":
                break
            stripped_line += char

        if include:
            stripped += stripped_line + "\n"

    return stripped