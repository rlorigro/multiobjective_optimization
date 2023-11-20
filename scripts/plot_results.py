import matplotlib
from matplotlib import pyplot
import argparse
import random


def main(nodes_path, edges_path):
    color_key = [
        [175,108,173],
        [91,138,201],
        [165,80,77],
        [119,89,223],
        [221,82,37],
        [195,112,66],
        [143,119,192],
        [93,115,217],
        [222,123,130],
        [148,166,50],
        [218,62,75],
        [75,168,60],
        [214,67,114],
        [72,155,108],
        [157,124,59],
        [60,171,194],
        [115,133,60],
        [207,144,42],
        [190,68,208],
        [188,101,203]
    ]

    coords = dict()

    child_to_parent = dict()
    parent_to_cluster = dict()

    # id_a,x_a,y_a,id_b,x_b,y_b
    with open(edges_path, 'r') as file:
        for l,line in enumerate(file):
            if l==0:
                continue

            tokens = line.strip().split(',')

            id_a = int(tokens[0])
            id_b = int(tokens[3])

            child_to_parent[id_b] = id_a

    # id,x,y,is_parent,true_label
    with open(nodes_path, 'r') as file:
        for l,line in enumerate(file):
            if l==0:
                continue

            tokens = line.strip().split(',')

            i = int(tokens[0])
            x = float(tokens[1])
            y = float(tokens[2])
            is_parent = bool(int(tokens[3]))

            coords[i] = [x,y]

            if is_parent:
                parent_to_cluster[i] = len(parent_to_cluster)
                print(len(parent_to_cluster))

    for a,b in child_to_parent.items():
        x1,y1 = coords[a]
        x2,y2 = coords[b]

        pyplot.plot([x1,x2],[y1,y2], color="gray", linewidth=0.2)

    for i,coord in coords.items():
        x,y = coord

        parent_id = i
        if i in child_to_parent:
            parent_id = child_to_parent[i]

        cluster_id = parent_to_cluster[parent_id]

        color = [float(x)/255.0 for x in color_key[cluster_id]]

        size = 2
        if parent_id == i:
            size = 4

        pyplot.plot(x,y,color=color,markersize=size,marker='o')

    pyplot.gca().set_xlim([0,10])
    pyplot.gca().set_ylim([0,10])
    pyplot.gca().set_aspect('equal')

    pyplot.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-n",
        required=True,
        type=str,
        help="Path to nodes_[name].csv file"
    )

    parser.add_argument(
        "-e",
        required=True,
        type=str,
        help="Path to edges_[name].csv file"
    )

    args = parser.parse_args()

    main(nodes_path=args.n, edges_path=args.e)
