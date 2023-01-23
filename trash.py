for i in range(10):

    print(f"translate([0,0,{i}*3])  cylinder(0.5*{10-i}, {10-i}*0.5, {10-i}*0.2);")
