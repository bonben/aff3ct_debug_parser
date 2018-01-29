#!/usr/bin/python3

import argparse


class OutputStructure:
    n_frames = 0
    inter_frame = 0
    frame_length = 0
    data_format = ""
    path = ""

    def __init__(self, n_frames = 0, frame_length = 0, data_format = "", path = ""):
        self.n_frames = n_frames
        self.frame_length = frame_length
        self.data_format = data_format
        self.path = path


# parse arguments
parser = argparse.ArgumentParser()

parser.add_argument("path", type=str, help="path to the file to be parsed")
parser.add_argument("--mod", type=str, required=True, help="module to be extracted, ex : Source_random_fast")
parser.add_argument("--tsk", type=str, required=True, help="task to be extracted, ex : generate")
parser.add_argument("-o", "--output", type=str, help="path to the output folder", default="./")

args = parser.parse_args()

# open files and store contents
with open(args.path, "r") as debug_file:
    lines = debug_file.readlines()


# build id key mod::tsk
key = args.mod + "::" + args.tsk

# boolean to trace if the key has been found
key_found = False

# extract tsk args
for i in range(0, len(lines)):
    if key in lines[i]:
        key_found = True
        line = lines[i]
        line = line.replace("const ", "")
        line = line[line.find("(") + 1: line.find(")")]
        tsk_args = line.split(', ')
        break

if not key_found:
    print(key + " not found")
    exit(1)

out_structures = []

# fill output structures
n_tsk_args = len(tsk_args)
for i in range(0, len(tsk_args)):
    out_structures.append(OutputStructure())
    tsk_arg = tsk_args[i]
    tsk_arg = tsk_arg.split(" ")
    out_structures[i].data_format = tsk_arg[0]
    tsk_arg = tsk_arg[1].replace("]", "")
    tsk_arg = tsk_arg.split("[")
    # TODO deal with path with path library
    out_structures[i].path = args.output + tsk_arg[0] + ".txt"
    if "x" in tsk_arg[1]:
        tsk_arg = tsk_arg[1].split("x")
        # TODO interframe independant of output => "global" variable
        out_structures[i].inter_frame = int(tsk_arg[0])
        out_structures[i].frame_length = int(tsk_arg[1])
    else:
        out_structures[i].inter_frame = 1
        out_structures[i].frame_length = tsk_arg[1]

# list line numbers with specified keys
key_lns = []
for i in range(0, len(lines)):
    if key in lines[i]:
        key_lns.append(i)

# write output information into file
for output in out_structures:
    with open(output.path, "w") as fout:
        fout.write(str(len(key_lns) * output.inter_frame) + "\n")
        fout.write(output.data_format + "\n")
        fout.write(str(output.frame_length) + "\n")
        fout.close()


for out_idx in range(0, len(out_structures)):
    output = out_structures[out_idx]
    with open(output.path, "a") as fout:
        for key_ln in key_lns:
            first_frame_ln = key_ln + 1 + output.inter_frame * out_idx
            for i in range(0, output.inter_frame):
                frame = lines[first_frame_ln + i]
                if output.inter_frame > 1:
                    frame = frame[frame.find("(") + 1: frame.find(")")]
                else:
                    frame = frame[frame.find("[") + 1: frame.find("]")]
                frame = frame.replace(" ", "")
                frame = frame.replace(",", " ")
                fout.write(frame)
                fout.write("\n")


print("# End of program.")
