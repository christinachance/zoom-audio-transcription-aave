import numpy as np
import pandas as pd
import re
import argparse
import os.path
import webvtt
from num2words import num2words
import pylangacq
import jiwer
import os

def fileProcessing(filepath):
    text = ""
    if (filepath.endswith('vtt')):
        for caption in webvtt.read(filepath):
            text = text + caption.text + "\n"
    elif (filepath.endswith('txt')):
        file = open(filepath,"r")
        data = file.readlines()
        text = ""
        for sample in data[1:]:
            text = text + sample.split('\t')[3] + "\n"
        file.close()
        text = re.sub('\(pause.*\)', '', text) # removing pauses
        text = re.sub('\/RD.*\/', '', text) # removing redacted personal information
        text = re.sub('\[\<.*\>\]', '', text) # removing overlapping non-linguistic sound markers
        text = re.sub('\<.*\>', '', text) # removing non- overlapping non-linguistic sound markers
    elif (filepath.endswith('cha')):
        data = pylangacq.read_chat(filepath)
        text = ""
        for sample in data.words():
            if sample in ['!', '?', '.']:
                text = text + " " + sample + "\n"
            else:
                text = text + " " + sample
        text = re.sub(r'(\d+)', '', text)
        text = re.sub('X', '', text) # removing redacted
        text = re.sub('\-', ' ', text)
    else:
        print("error: unaccepted file format [" + filepath + "]")
        return
    text = re.sub(r"(\d+)", lambda x: num2words(int(x.group(0))), text)
    text = text.lower()
    text = re.sub('\-', ' ', text) # adding spaces between stutters
    text = jiwer.ExpandCommonEnglishContractions()(text) # expand contractions
    # cleaning text for excess spaces and tabs
    text = re.sub(r'[^\w\s]', '', text) # removing punctation
    text = jiwer.RemoveWhiteSpace(replace_by_space=True)(text)
    text = jiwer.RemoveMultipleSpaces()(text)
    # writing cleaned text to new file
    new_file_path = filepath.rpartition('_')[0] + "_processed/" + filepath.rpartition('/')[2][:-4] + "_cleaned.txt"
    if not os.path.exists(new_file_path):
        new_file = open(new_file_path, "x")
    new_file = open(new_file_path, "w")
    new_file.write(text)
    new_file.close()


# def txtProcessing(filename):
#     file = open(filename,"r")
#     data = file.readlines()
#     text = ""
#     for sample in data[1:]:
#         text = text + sample.split('\t')[3] + "\n"
#     file.close()
#     text = re.sub('\(pause.*\)', '', text) # removing pauses
#     text = re.sub('\/RD.*\/', '', text) # removing redacted personal information
#     text = re.sub('\[\<.*\>\]', '', text) # removing overlapping non-linguistic sound markers
#     text = re.sub('\<.*\>', '', text) # removing non- overlapping non-linguistic sound markers
#     text = re.sub(r"(\d+)", lambda x: num2words(int(x.group(0))), text)
#     text = text.lower()
#     text = jiwer.RemoveSpecificWords(lingustic_sounds)(text)
#     text = re.sub('\-', ' ', text) # adding spaces between stutters
#     text = jiwer.ExpandCommonEnglishContractions()(text) # expand contractions
#     # cleaning text for excess spaces and tabs
#     text = jiwer.RemoveMultipleSpaces()(text)
#     text = jiwer.RemoveWhiteSpace(replace_by_space=True)(text)
#     # text = text.replace('.', '\n') # removing punctation
#     text = re.sub(r'[^\w\s]', '', text) # removing punctation
#     # writing cleaned text to new file
#     new_file_name = filename.rpartition('_')[0] + "_processed/" + filename.rpartition('/')[2][:-4] + "_cleaned.txt"
#     print(new_file_name)
#     # if not os.path.exists(new_file_name):
#     #     new_file = open(new_file_name, "x")
#     # new_file = open(new_file_name, "w")
#     # new_file.write(text)
#     # new_file.close()
#
# def vvtProcessing(filename):
#     text = ""
#     for caption in webvtt.read(filename):
#         text = text + caption.text + "\n"
#     text = re.sub(r"(\d+)", lambda x: num2words(int(x.group(0))), text)
#     text = text.lower()
#     text = jiwer.RemoveSpecificWords(lingustic_sounds)(text)
#     text = re.sub('\-', ' ', text)
#     text = jiwer.ExpandCommonEnglishContractions()(text) # expand contractions
#     # cleaning text for excess spaces and tabs
#     text = jiwer.RemoveMultipleSpaces()(text)
#     text = jiwer.RemoveWhiteSpace(replace_by_space=True)(text)
#     # text = text.replace('.', '\n') # removing punctation
#     text = re.sub(r'[^\w\s]', '', text) # removing punctation
#     # writing cleaned text to new file
#     new_file_name = filename.rpartition('_')[0] + "_processed/" + filename.rpartition('/')[2][:-4] + "_cleaned.txt"
#     print(new_file_name)
#     # if not os.path.exists(new_file_name):
#     #     new_file = open(new_file_name, "x")
#     # new_file = open(new_file_name, "w")
#     # new_file.write(text)
#     # new_file.close()
#
#
# def chaProcessing(filename):
#     data = pylangacq.read_chat(filename)
#     text = ""
#     for sample in data.words():
#         if sample in ['!', '?', '.']:
#             text = text + " " + sample + "\n"
#         else:
#             text = text + " " + sample
#     text = re.sub(r'(\d+)', '', text)
#     text = re.sub('X', '', text) # removing redacted
#     text = re.sub('\-', ' ', text)
#     text = text.lower()
#     text = jiwer.RemoveSpecificWords(lingustic_sounds)(text)
#     text = re.sub('ʔ', '', text)
#     text = jiwer.ExpandCommonEnglishContractions()(text) # expand contractions
#     # cleaning text for excess spaces and tabs
#     text = jiwer.RemoveMultipleSpaces()(text)
#     text = jiwer.RemoveWhiteSpace(replace_by_space=True)(text)
#     # text = text.replace('.', '\n') # removing punctation
#     text = re.sub(r'[^\w\s]', '', text) # removing punctation
#     # writing cleaned text to new file
#     new_file_name = filename.rpartition('_')[0] + "_processed/" + filename.rpartition('/')[2][:-4] + "_cleaned.txt"
#     print(new_file_name)
#     # if not os.path.exists(new_file_name):
#     #     new_file = open(new_file_name, "x")
#     # new_file = open(new_file_name, "w")
#     # new_file.write(text)
#     # new_file.close()


def main():
    """
    Main file to run from the command line.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("directory_name",
                        help="directory of raw files")
    args = parser.parse_args()


    for filename in os.listdir(args.directory_name):
        filepath = os.path.join(args.directory_name, filename)
        # checking if it is a file
        if os.path.isfile(filepath):
            fileProcessing(filepath)




if __name__ == "__main__":
    main()
