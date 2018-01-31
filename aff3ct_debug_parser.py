#!/usr/bin/python3

import argparse


class OutputStructure:
    index = 0
    n_frames = 0
    frame_length = 0
    data_format = ""
    name = ""
    frames = []

    def __init__(self):
        self.frames = []

    def get_frames(self, lines, key, inter_frame):
        # list line numbers with specified keys
        key_lns = []
        for i in range(0, len(lines)):
            if key in lines[i]:
                key_lns.append(i)

        for key_ln in key_lns:
            first_frame_ln = key_ln + 1 + inter_frame * self.index
            for i in range(0, inter_frame):
                frame = lines[first_frame_ln + i]
                if inter_frame > 1:
                    frame = frame[frame.find("(") + 1: frame.find(")")]
                else:
                    frame = frame[frame.find("[") + 1: frame.find("]")]
                frame = frame.replace(" ", "")
                frame = frame.replace(",", " ")
                frame = frame.split(" ")
                self.frames.append(frame)

    def export_as_text(self, path):
        # write output information into file
        with open(path, "w") as fout:
            fout.write(str(len(self.frames)) + "\n")
            fout.write(self.data_format + "\n")
            fout.write(str(self.frame_length) + "\n")

            for frame in self.frames:
                for i, value in enumerate(frame):
                    if i:
                        fout.write(" ")
                    fout.write(value)
                fout.write("\n")


def adp_parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("path", type=str, help="path to the file to be parsed")
    parser.add_argument("--mod", type=str, required=True, help="module to be extracted, ex : Source_random_fast")
    parser.add_argument("--tsk", type=str, required=True, help="task to be extracted, ex : generate")
    parser.add_argument("-o", "--output", type=str, help="path to the output folder", default="./")

    args = parser.parse_args()
    return args


def get_task_ios(lines, key):
    for i in range(0, len(lines)):
        if key in lines[i]:
            line = lines[i]
            line = line.replace("const ", "")
            line = line[line.find("(") + 1: line.find(")")]
            tsk_ios = line.split(', ')
            return tsk_ios
    return []


def get_output_structures(lines, key):
    tsk_ios = get_task_ios(lines, key)
    if not tsk_ios:
        print(key + " not found")
        exit(1)
    out_structures = []
    for i in range(0, len(tsk_ios)):
        out_structures.append(OutputStructure())
        out_structures[i].index = i
        tsk_arg = tsk_ios[i]
        tsk_arg = tsk_arg.split(" ")
        out_structures[i].data_format = tsk_arg[0]
        tsk_arg = tsk_arg[1].replace("]", "")
        tsk_arg = tsk_arg.split("[")
        out_structures[i].name = tsk_arg[0]
        if "x" in tsk_arg[1]:
            tsk_arg = tsk_arg[1].split("x")
            inter_frame = int(tsk_arg[0])
            out_structures[i].frame_length = int(tsk_arg[1])
        else:
            inter_frame = 1
            out_structures[i].frame_length = tsk_arg[1]
    return out_structures, inter_frame


# TODO deal with path with path library

def main():
    format_list = {"int8, int16, int32, int64, float32, float64"}

    args = adp_parse_args()

    # open files and store contents
    with open(args.path, "r") as debug_file:
        lines = debug_file.readlines()

    # build id key mod::tsk
    key = args.mod + "::" + args.tsk

    # fill output structures
    out_structures, inter_frame = get_output_structures(lines, key)

    # get frames
    for out_sct in out_structures:
        out_sct.get_frames(lines, key, inter_frame)

    # export frames
    for out_sct in out_structures:
        out_sct.export_as_text(args.output + out_sct.name + ".txt")

    print("# End of program.")


if __name__ == "__main__":
    main()
