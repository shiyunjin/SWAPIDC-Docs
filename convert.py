#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys, getopt
import os
import re

def usage():
    print('convert.py -i <inputdir>');

def file_extension(path): 
    return os.path.splitext(path)[1];

def dirlist(path, allfile):
    filelist =  os.listdir(path);

    for filename in filelist:
        filepath = os.path.join(path, filename);
        if os.path.isdir(filepath):
            dirlist(filepath, allfile);
        else:
            if file_extension(filepath) == '.tpl':
                allfile.append(filepath);
    return allfile;

line = '';

def replacetpl(file_path):
    global line;
    pattern = re.compile(b'\$lang\[[^\{\}\s]+\]');

    # try:
    f = open(file_path,'rb+');
    all_lines = f.readlines();
    f.seek(0);
    f.truncate();
    for line in all_lines:
        line.decode('utf-8');
        result = re.findall(pattern,line);
        for text in result:
            new_str = text.replace(b'$lang[',b'__(');
            new_str = new_str[:-1] + b')';
            new_str = new_str.replace(b')]}',b'])}'); #修复常见语法转换错误
            line = line.replace(text, new_str);
        f.write(line);
    f.close();

    # except Exception as e:
        # print(e);


def main(argv):
    inputdir = '';
    try:
        opts, args = getopt.getopt(argv,"hi:",["idir="]);
    except getopt.GetoptError:
        usage();
        sys.exit(1);
    for opt, arg in opts:
        if opt == '-h':
            usage();
            sys.exit();
        elif opt in ("-i", "--idir"):
            inputdir = arg
    if inputdir == '':
        usage();
        sys.exit(1);

    files = dirlist(inputdir, []);
    print(files);


    for file in files:
        replacetpl(file);


if __name__ == "__main__":
        main(sys.argv[1:]);


