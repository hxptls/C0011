#
# c.11.py
# Created by Hexapetalous on Feb 6, 2016.
#
# This is a part of C0011.
# Copyright (c) 2016 Hexapetalous. All rights reserved.
#


def printl(my_str):
    """
    Print the left part of the whole line.
    :param my_str: Output string.
    :return:
    """
    print(my_str, flush=True, end='')


printl('Initializing...')
from P0009 import btbb as p9b
from P0009 import btbbc as p9c

# API #
ROOT_URL = 'http://tieba.baidu.com/p/4260990232'
IGNORE_FLOOR = []
STORE_FILE_NAME = '/home/wan/N_E_I_H version1.0/C0011/233.txt'
print('[OK]')

# FETCH DATA #
data = dict()

printl('Fetching title of url: \'%s\'...' % ROOT_URL)
data['title'] = p9b.get_title_from_url(ROOT_URL)
print('[OK]')
print('TITLE %s' % data['title'])

printl('Fetching data of url: \'%s\'...' % ROOT_URL)
root_post = p9c.Post(ROOT_URL)
print('[OK]')

printl('Process step #1...')
root_post.match()
root_post.migration()
print('[OK]')

print('Process step #2...')
root_info = root_post.get_real_floors()
child_list = list()
test_count = 0
for floor in root_info:
    found = False
    if test_count % 16 == 0:
        print('Analyzed %d floors...' % test_count)
    test_count += 1
    if floor['floor'].floor_index in IGNORE_FLOOR:
        continue
    if floor['comments'] is None:  # No comments, play egg...
        continue
    if floor['floor'].floor_index < 3:
        continue
    for comment in floor['comments']:
        content = comment.content
        if content.find('专项') != -1:
            href = p9b.get_a(content)
            if href == '':
                print('ERROR There is a comment which contains \'专项\' but no '
                      'link.')
                print('\tROOT_URL %s' % ROOT_URL)
                print('\tFLOOR %d' % floor['floor'].floor_index)
                print('\tRAW COMMENT %s' % content)
                print('\tERROR END')
                continue
            floor_content = floor['floor'].content
            floor_content_list = floor_content.splitlines()
            for string in floor_content_list:
                start_from = -1
                if string.find('作品全称：') != -1:
                    start_from = string.find('作品全称：')
                elif string.find('作品全称:') != -1:  # I'm so clever!
                    start_from = string.find('作品全称:')
                elif string.find('作品名称：') != -1:  # I'm so clever! * 2
                    start_from = string.find('作品名称：')
                elif string.find('作品名称:') != -1:  # I'm so clever! * 3
                    start_from = string.find('作品名称:')

                if start_from != -1:  # Everything is done.
                    name = string[start_from + 5:]  # `5` is the length of
                    # '作品全称：'
                    child = {'name': name, 'href': href}
                    child_list.append(child)
                    found = True
                    break
            if not found:
                print('ERROR There is a good comment but there is no name of '
                      'the works.')
                print('\tROOT_URL %s' % ROOT_URL)
                print('\tFLOOR %d' % floor['floor'].floor_index)
                print('\tRAW FLOOR (follow lines)')
                print(floor_content)
                print('\tERROR END')
                print('\tINFO This may be caused by a wrong prefix. If it is '
                      'so, add it to the control flow started from line #72.')
            break
        if found:
            break

print('[OK]')
# TEST
# print('This is test...TEST START')
# for child in child_list:
#     print('NAME %s' % child['name'], 'HREF %s' % (child['href']), sep='\n')
# print('TEST END')

# PRINT OUT #
DATA_VERSION = 0
printl('Writing file...')
file = open(STORE_FILE_NAME, mode='w')
print('# This is c.11, a part if C0011 by Hexapetalous.', file=file)
print('# Data version = %d' % DATA_VERSION, file=file)
print('# Copyright 2016 Hexapetalous. All rights reserved.', file=file)
for child in child_list:
    print('NAME %s' % child['name'], 'HREF %s' % (child['href']), sep='\n',
          file=file)
print('END', file=file)
print('[OK]')
