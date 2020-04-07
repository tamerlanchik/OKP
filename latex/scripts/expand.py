#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import load as json_load
from sys import argv as sys_argv


def get_var(file, end_delimiter, max_var_len=100):
    char = file.read(1)
    name = ''
    i = 0
    while char:
        i+=1
        if i > max_var_len:
            print("Error: too long variable: ", name)
            return None
        if char == end_delimiter:
            return name
        name += char
        char = file.read(1)

def expand(input_file, output_file, values, start_delimiter, end_delimiter):
    with open(input_file, 'r', encoding="utf-8") as src, open(output_file, 'w') as dest:
        while True:
            char = src.read(1)
            if not char:
                print("File end reached")
                break
            if char != start_delimiter:
                dest.write(char)
                continue

            var_name = get_var(src, end_delimiter)
            if not var_name:
                exit(1)
            val = values.get(var_name)
            if not isinstance(val, str):
                val = str(val)
            if not val:
                print(var_name, ': cannot find value in dict')
                continue
            print('Replace %s to %s' % (var_name, val))
            dest.write(val)


if len(sys_argv) > 4:
    print("Too many args (max 3)")
    exit(1)

_, input_file, output_file, values_file = sys_argv

values_dict = {}
with open(values_file, 'r') as values:
    values_dict = json_load(values)

expand(input_file, output_file, values_dict,
       start_delimiter='¿', end_delimiter='¡')


