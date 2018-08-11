#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys, getopt
import os
import re

def usage():
    print('gettext.py -i <inputdir> -o zh-CN.po');

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
lists = [];

def readtpl(file_path):
    global line,lists;
    pattern = re.compile(b'__\([\'\"]{1}[^\$\{\}\s]+[\'\"]{1}\)');

    # try:
    f = open(file_path,'rb+');
    all_lines = f.readlines();
    for line in all_lines:
        line.decode('utf-8');
        result = re.findall(pattern,line);
        for text in result:
            lists.append(text[4:-2]);
    f.close();

    # except Exception as e:
        # print(e);

def writepo(file_name):
    global lists;
    f = open(file_name,'wb');
    f.seek(0);
    f.truncate();
    doc = '''msgid ""
msgstr ""
"Project-Id-Version: 模版\\n"
"POT-Creation-Date: 2018-08-11 14:16+0800\\n"
"PO-Revision-Date: 2018-08-11 14:16+0800\\n"
"Last-Translator: getttext <system@swapteam.cn>\\n"
"Language-Team: \\n"
"Language: zh_CN\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"X-Generator: SWAP GetText 1.0\\n"
"X-Poedit-Basepath: .\\n"
"Plural-Forms: nplurals=1; plural=0;\\n"
"X-Poedit-KeywordsList: __\\n"
"X-Poedit-SearchPath-0: .\\n"
"X-Poedit-SearchPathExcluded-0: *.js\\n"

''';
    
    f.write(doc.encode());
    for item in lists:
        f.write(b"#:\n");
        f.write(b'msgid "' + item + b"\"\n");
        f.write(b'msgstr ""' + b"\n\n");
    f.close();

def main(argv):
    global lists;
    
    inputdir = '';
    outfile = '';
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["idir=","ofile="]);
    except getopt.GetoptError:
        usage();
        sys.exit(1);
    for opt, arg in opts:
        if opt == '-h':
            usage();
            sys.exit();
        elif opt in ("-i", "--idir"):
            inputdir = arg
        elif opt in ("-o", "--ofile"):
            outfile = arg
    if inputdir == '' or outfile == '':
        usage();
        sys.exit(1);

    files = dirlist(inputdir, []);
    print(files);


    for file in files:
        readtpl(file);
    
    lists = list(set(lists));
    writepo(outfile);
    print('输出的文件为：', outfile);

if __name__ == "__main__":
        main(sys.argv[1:]);

