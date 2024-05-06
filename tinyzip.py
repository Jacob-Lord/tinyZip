from heapq import heappush, heappop, heapify
from collections import defaultdict
from bitarray import bitarray, decodetree
import math
import os

#https://www.codespeedy.com/how-to-encode-a-string-in-huffman-coding-using-python/
def huffmanCode(aDict): #with a given dictionary
    """Huffman encode the given dict mapping symbols to weights"""
    heap = [[freq, [aChar, ""]] for aChar, freq in aDict.items()] # build a minheap
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap) # pop least frequent, then heapify
        hi = heappop(heap) # next least frequent , then heapify
        for pair in lo[1:]:
            pair[1] = '0' + pair[1] #pair[1] is the current codeword for pair[0] char
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:]) #push then heapify
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

def zip(text, fileName, huffman):
    '''
    Desc: Compresses data information by shortening sequence of bits used to store chars based on frequency
    Paramters: text - text to compress
           fileName - the file name to store the compressed txt
            huffman - Huffman code dictionary
    Returns: a dictionary containing the fileName and compressed data in the form of a bitarray()
    '''
    ba = bitarray() #create bitarray object
    ba.encode(huffman, text) # encode each character of text to code table mapping according to Huffman code

    fileName = format_name_to_zip(fileName)
    file = open(fileName, "w")
    file.write(ba.to01())
    #store bit array with file name
    info = {fileName: ba} #{'King.zip': bitarray('...')} is the format of this dictionary 
    return info, fileName

def format_name_to_zip(fileName):
    if str(fileName).__contains__('.txt'):
        fileName = fileName[0:-4] #cut off file format from string
        fileName += '.zip' #replace with proper file format
    return fileName

def format_name_to_txt(fileName):
    fileName = fileName[0:-4] #cut off file format from string
    fileName += '.zip' #replace with proper file format
    return fileName


def build_freq_table(file,text):
    '''
    Desc: Build a freq Table (Dictionary ADT) of characters from a file object
    Parameter: file - A file object
    '''
    freq_dict = {}
    for s in file: 
        text += s
        for w in s: 
            if freq_dict.__contains__(w):
                freq_dict[w] += 1
            else:
                freq_dict.update({w: 1})
    return freq_dict, text

def build_code_table(huffman_tree):
    '''
    Desc: Create a huffman code table based on the huffman tree and 
        returns a dictionary of the mapping of the characters
    Parameter: huffman_tree - A double nested list representing the huffman tree's mapping of values
    '''
    code_table = {} #initialize
    for i in range(0, len(huffman_tree)): #iterate through huffman_tree
        #map values from huffman_tree to a code table (dictionary)
        code_table.update({huffman_tree[i][0]: bitarray(huffman_tree[i][1])}) #{key, bitarray('010')} is the correct format for .encode in bitarry

    return code_table
        
def display_encode_info(freq_table, code_table):
    print('Character \t Weight \t\t Huffman Code')

    for key, value in code_table.items():
        huff_val = value.to01()
        print(key, "\t", freq_table[key], "\t\t", huff_val) #newline character makes print loop go to a newline for it, so it is a blank symbol enxt to 58 and its huffman code


def unzip(zipFileName, huffman, zipSize):
    t = decodetree(huffman)
    file = open(zipFileName)
    data = ''
    for x in file:
        x.rstrip('\n') #take newline char off
        data += x
    file.close() #close file object
    a = bitarray(data)
    a.decode(t) #decode compressed data using huffman dict
    text = ''.join(a.iterdecode(t)) #iterate through the bitarray and 
    fileSize = text.__len__()
    fileName = format_name_to_txt(zipFileName)
    file = open('King(1).txt', 'w')
    file.write(text)
    file.close()
    return fileSize


def huffman_driver():
    #fileName = input('Enter the name of the file to zip (and then unzip)') #example : file.txt
    fileName = 'King.txt'
    file = open(fileName) #make file object from text file
    text = '' #store text as a string
    freq_table, text = build_freq_table(file,text) #build a freq table (Dictionary ADT) of characters from the file object
    print(len(text)) #text length is 2 char longer than Mr. Sung's version, why? semicolon maybe
    file.close() #close file after reading
    huffman_tree = huffmanCode(freq_table) # build a huffman tree using the frequency table
    code_table = build_code_table(huffman_tree) #create code table (dictionary) from huffman tree
    display_encode_info(freq_table, code_table)
    zip_info, zip_name = zip(text, fileName, code_table)
    print('Size of King.txt: ' + str(text.__len__()))
    print('Size of ' + zip_name + ': ' + str(zip_info['King.zip'].nbytes))
    file_size = unzip(zip_name, code_table, '101')
    print('Size of unzipped ' + fileName + ': ' + str(file_size))


huffman_driver()
