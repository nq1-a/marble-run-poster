from lib import tdata_gen

@tdata_gen
def curly(base):
    for r in range(15):
        for c in range(10):
            if (r == 0 or r == 14) and c == 0:
                continue
            
            base["bricks"][str(r * 10 + c)] = {
                "type": "Boost",
                "rotation": r / 15 + c / 10,
                "row": r,
                "col": c
            }
