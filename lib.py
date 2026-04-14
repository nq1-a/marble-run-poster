from copy import deepcopy
from json import dumps

base_tdata = {
    "bricks": {
        "0": {
            "type": "Ball",
            "rotation": 0,
            "row": 0,
            "col": 0
        },
        "140": {
            "type": "Exit",
            "rotation": 0,
            "row": 14,
            "col": 0
        }
    },
    "pairs": []
}

def tdata_gen(gen):
    with open("tracks/" + gen.__name__ + ".json", "w") as f:
        tdata = deepcopy(base_tdata)
        gen(tdata)
        f.write(dumps(tdata))
    
    return gen
