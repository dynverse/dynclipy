import rpy2.robjects as ro
import rpy2.rinterface as rinterface

import sys

from scipy.sparse import csr_matrix
import numpy as np

@ro.conversion.rpy2py.register(rinterface.SexpS4)
def convert_sparse(obj):
    if "dgCMatrix" in obj.rclass[0]:
        x = obj.do_slot("x")
        p = obj.do_slot("p")
        i = obj.do_slot("i")
        
        return csr_matrix((x, i, p))

@ro.conversion.rpy2py.register(rinterface.ListSexpVector)
def convert_list(obj):
    # check if a non-empty list
    if not isinstance(obj, rinterface.NULLType) and len(obj) > 0:
        # check if named list
        if not isinstance(obj.names, rinterface.NULLType) and len(obj) == len(obj.names):
                return {
                        name:ro.conversion.rpy2py(obj[i]) for i, name in enumerate(obj.names)
                }
        else:
                return [
                        ro.conversion.rpy2py(obj[i]) for i in range(len(obj))
                ]
    else:
        return {}


@ro.conversion.rpy2py.register(rinterface.StrSexpVector)
def convert_character(obj):
    if len(obj) == 1:
        return str(obj[0])
    else:
        return [str(x) for x in obj]


@ro.conversion.rpy2py.register(rinterface.IntSexpVector)
def convert_integer(obj):
    if len(obj) == 1:
        return int(obj[0])
    else:
        return [int(x) for x in obj]


@ro.conversion.rpy2py.register(rinterface.FloatSexpVector)
def convert_double(obj):
    if len(obj) == 1:
        return float(obj[0])
    else:
        return [float(x) for x in obj]


@ro.conversion.rpy2py.register(rinterface.BoolSexpVector)
def convert_logical(obj):
    if len(obj) == 1:
        return bool(obj[0])
    else:
        return [bool(x) for x in obj]


# recursively check inside lists and dicts for items that were not converted into python objects
def check_conversion_rpy2py(obj, position = "/", verbose = False):
    if verbose:
            print("✔ " + position)
    if isinstance(obj, dict):
        for name, obj2 in obj.items():
            check_conversion_rpy2py(obj2, position + name + "/")
    elif isinstance(obj, list):
        for i, obj2 in enumerate(obj):
            check_conversion_rpy2py(obj2, position + str(i) + "/")
    else:
        assert not isinstance(obj, rinterface.SexpVector), position + " could not be converted!"

    return True


def main(
    args = sys.argv[1:],
    definition_location = "/code/definition.yml"
):
    ro.globalenv["args"] = ro.StrVector(args)
    ro.globalenv["definition_location"] = ro.StrVector([definition_location])

    task = ro.r("""
    dyncli::main(
            args = args,
            definition_location = definition_location
    )
    """)

    if "seed" in task:
        np.random.seed(np.abs(task["seed"]))

    return task