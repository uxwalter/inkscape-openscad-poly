"""
Contributors:
Copyright (c) 2016 Benedict Endemann
Copyright (c) 2011 Marty McGuire
"""
import inkex

class OSCADPolyContext:
    def __init__(self, svg_file):
        self.file = svg_file
        self.polygons = []
        inkex.debug(f"Writing to {svg_file}")

    def generate(self):
        # generate list of all modules at top for easy control
        for polygon in self.polygons:
            if polygon['color']:
                print("color([{:0.4f}, {:0.4f}, {:0.4f}, {:0.4f}]) {}();".format(
                    polygon['color'][0],
                    polygon['color'][1],
                    polygon['color'][2],
                    polygon['color'][3],
                    polygon['id']))
            else:
                print("{}();".format(polygon['id']))

        # generate actual modules from polygons
        for polygon in self.polygons:
            # align
            pmin=[ 1e6, 1e6]
            pmax=[-1e6,-1e6]
            for p in polygon['points']:
                pmin[0]=min(p[0],pmin[0])
                pmin[1]=min(p[1],pmin[1])
                pmax[0]=max(p[0],pmax[0])
                pmax[1]=max(p[1],pmax[1])

            xdiff=pmax[0]-pmin[0]
            ydiff=pmax[1]-pmin[1]
            points=[ [p[0]-pmin[0]-xdiff/2,(pmax[1]-p[1])-ydiff/2] for p in polygon['points']]

            print(f"module {polygon['id']}() {{")

            print("  segs=[")
            for seg in polygon['paths']:
                print("            {}".format(seg),end=",")

            print("];")
            print(" mask=[")
            print(",".join([str(len(x)) for x in polygon['paths']]))
            print("];")

            print("    polygon(")
            print("        points=[")
            for p in points:
                print(f"[{p[0]:.3f},{p[1]:.3f}]", end=",")
            print("],")

            #print("            {},".format(points))
            print("        paths=[ for (i=[0:len(mask)]) if (mask[i]) segs[i]  ]")
            print("    );")
            print("}")

    def add_poly(self, poly_id, points, paths, color = None):
        shortened_points = [[round(x, 3),round(y, 3)] for x, y in points]
        self.polygons.append({ 'id': poly_id, 'points':shortened_points, 'paths':paths, 'color':color})
