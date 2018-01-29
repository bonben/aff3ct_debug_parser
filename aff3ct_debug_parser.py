#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("path", type=str, help="path to the file to be parsed")
parser.add_argument("--mod", type=str, required=True, help="module to be extracted, ex : Source_random_fast")
parser.add_argument("--sck", type=str, required=True, help="socket to be extracted, ex : generate")
parser.add_argument("-o", "--output", type=str, help="path to the output folder", default="./")

parser.parse_args()
