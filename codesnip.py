#!/usr/bin/env python3
#written in python3.2.3
#author: Micah Page / metublurr
__version__ = 0.03 #added color difference, added arguments, changed direcory paths to one file

import webbrowser
import os
import sys
import pickle
import fileinput

default_color = '\x1b[0m' #white fg, black bg
key_color =  '\x1b[33m' #yellow
text_color = '\x1b[32m' #green


if os.name =='nt':
    os.environ['HOME'] = os.path.join(os.environ['HOMEDRIVE'], 
                                      os.environ['HOMEPATH'])

instruction = 'Paste code snippet, save file (Ctrl + S), then close (Ctrl + Q), see terminal'
dir_path = os.environ['HOME'] + os.sep + '.snippets'
pkl_path = dir_path + os.sep + 'snippets.pkl'
full_path = dir_path + os.sep + 'snippets.py'
temp_path = dir_path + os.sep + instruction + '.py'
readme = dir_path + os.sep + 'README.txt'

def readmetext(readme):
    readme_file = open(readme, 'w')
    print('Do not delete code snippet from file as keys for it will still exist',file=readme_file)
    print('To delete all created by program:', file=readme_file)
    print('\tsudo rm -rf /home/<USER>/.Snippets', file=readme_file)
    readme_file.close()

def makesep():
    pass
    #mysep = '-' * 60
    #if type(mysep) == 'str':
        #print('-' * 60)

    
def keylist(key):
    return '#KEYLIST=' + str(key)

def start_stamp(key):
    return '#STARTCODE=' + str(key)
    
def end_stamp(key):
    return '#ENDCODE=' + str(key)
    
def create_new_path(full_path):
    filed = open(full_path, 'w')
    filed.close()
    
def create_pkl(pkl_path, obj):
    files = open(pkl_path, 'wb')
    pickle.dump(obj, files)
    files.close()
    
def load_pkl(pkl_path):
    files = open(pkl_path, 'rb')
    obj = pickle.load(files)
    return obj

def write_snippet(full_path, temp_path, pkl_path):

    temp = open(temp_path, 'w')
    webbrowser.open(temp_path)
    while True:
        keyword = input('\n{}\nq to quit\nInput Keyword for Snippet: '.format(instruction))
        
        if keyword == '':
            print('Incorrect keyword')
            #os.remove(temp_path)
            continue 
        elif keyword == 'q':
            os.remove(temp_path)
            print()
            return False 
        elif os.stat(temp_path).st_size == 0:
            print('No data to write!')
            #os.remove(temp_path)
            webbrowser.open(temp_path)
            continue
        keylist = load_pkl(pkl_path)
        for key in keylist:
            if key == keyword or keyword == 'q': #if keyword already exists or quit (q)
                print('keyword already exists!')
                #os.remove(temp_path)
                continue
        else:
            break
    temp.close()
    keylist.append(keyword)
    create_pkl(pkl_path, keylist)

    files = open(full_path, 'a')
    temp = open(temp_path)
    
    startcode = start_stamp(keyword)
    endcode = end_stamp(keyword)
    
    files.write(startcode + '\n') #write to files
    for line in temp:
        files.write(line)
    files.write(endcode + '\n')
    files.close()
    
    os.remove(temp_path)
    
def view_keys(pkl_path):
    keylist = load_pkl(pkl_path)
    makesep()
    if len(keylist) == 0:
        print('No keys yet!')
    else:
        print('# of keys: {}'.format(len(keylist)))
        print('keys are: ')
        print(key_color, end='')
        for key in sorted(keylist):
            print('\t' + key)
    print(default_color, end='')

def change_key_name(full_path, pkl_path, old_key, new_key):#added full_path
    keylist = load_pkl(pkl_path)
    makesep()
    for key in keylist:
        if old_key == key:
            keylist.remove(key)
    keylist.append(new_key)
    create_pkl(pkl_path, keylist)
    edit_snippet_file(full_path, old_key, new_key)

    
def edit_snippet_file(full_path, old_key, new_key):
    
    old_startcode = start_stamp(old_key)
    old_endcode = end_stamp(old_key)
    new_startcode = start_stamp(new_key)
    new_endcode = end_stamp(new_key)
    
    files = fileinput.input(full_path, inplace=True)
    for line in files:
        if old_startcode in line or old_endcode in line:
            line = line.replace(old_startcode, new_startcode)
            line = line.replace(old_endcode, new_endcode)
        sys.stdout.write(line)

def delete_snippet(full_path, del_key):
    files = open(full_path)
    lines = files.readlines()
    
    startcode = start_stamp(del_key)
    endcode = end_stamp(del_key)
    
    numline = 0
    for line in lines:
        numline = numline + 1
        if startcode in line:
            startcode_num = numline
        if endcode in line:
            endcode_num = numline
    
    files = fileinput.input(full_path, inplace=True)
    for numline, line in enumerate(files):
        if numline >= startcode_num and numline < (endcode_num - 1):
            line = line.replace(line, '')
        if startcode in line or endcode in line:
            line = line.replace(line, '')
            #line = line.replace(line, '')######
        sys.stdout.write(line)
    keylist = load_pkl(pkl_path)
    for key in keylist:
        if del_key == key:
            keylist.remove(key)
    create_pkl(pkl_path, keylist)
    return
    
def get_snippet(full_path, key):
    files = open(full_path)
    lines = files.readlines()
    
    startcode = start_stamp(key)
    endcode = end_stamp(key)
    
    numline = 0
    for line in lines:
        numline = numline + 1
        if startcode in line:
            startcode_num = numline
        if endcode in line:
            endcode_num = numline

    total_file_line = numline
    total_snippet_line = ((endcode_num - 1) - startcode_num)
    print('total lines: {}'.format(total_file_line))
    print('total snippet lines: {}'.format(total_snippet_line))
    print('snippet on lines: {0}-{1}'.format((startcode_num + 1), (endcode_num - 1)))
    makesep()
    
    numline = 0
    print(text_color, end='') #print green if in terminal
    for numline, line in enumerate(lines):
        
        if numline >= startcode_num and numline < (endcode_num - 1):
            print(line, end='')
    print(default_color, end='') #reset color
    files.close()
    
def search_keys(pkl_path, keyword=''):
    keylist = load_pkl(pkl_path)
    if keyword == '' or keyword == ' ':
        search = input('Search for key: ')
    else:
        search = keyword
    print(key_color, end='')
    for key in sorted(keylist):
        if search in key:
            print('\t',key)
    print(default_color, end='')
    
def menu(full_path, temp_path, pkl_path):
    while True:
        makesep()
        print('1) View keys')
        print('2) Write Code Snippet')
        print('3) Read Code Snippet')
        print('4) Change key name')
        print('5) Delete key and snippet')
        print('6) Search keys')
        print('E) Exit')
        
        user_choice = input('Choose option: ')
        if user_choice == '1':
            view_keys(pkl_path)
        elif user_choice == '2':
            write_snippet(full_path, temp_path, pkl_path)
        elif user_choice == '3':
            keyword = input('\nkeyword: ')
            if keyword == 'q':
                print()
                continue
            keylist = load_pkl(pkl_path)
            if keyword not in keylist:
                print('No such key!')
            else:
                get_snippet(full_path, keyword)
        elif user_choice == '4':
            old_key = input('\nOld keyword: ')
            if old_key == 'q':
                print()
                continue
            keylist = load_pkl(pkl_path)
            if old_key not in keylist:
                print('No such key!')
            else:
                new_key = input('New keyword: ')
                if new_key == 'q':
                    print()
                    continue
                if new_key == '':
                    print('Invalid keyword!')
                    continue
                if new_key in keylist:
                    print('keyword already exists')
                    print()
                    continue
                else:
                    change_key_name(full_path, pkl_path, old_key, new_key)
        elif user_choice == '5':
            keyword = input('\nkeyword: ')
            if keyword == 'q':
                print()
                continue
            keylist = load_pkl(pkl_path)
            if keyword not in keylist:
                print('No such key!')
            else:
                delete_snippet(full_path, keyword)
        elif user_choice == '6':
            search_keys(pkl_path)
        elif user_choice.capitalize() == 'E':
            sys.exit()
            
def menu_term(full_path, temp_path, pkl_path, flag, keywordarg=None, new_keywordarg=None):
    #print('keywordarg is: ', keywordarg)
    #print('new_keywordarg is: ', new_keywordarg)
    if flag == '-v':
        view_keys(pkl_path)
    elif flag == '-w':
        write_snippet(full_path, temp_path, pkl_path)
    elif flag == '-r':
        if keywordarg == None:
            keyword = input('\nkeyword: ')
        else:
            keyword = keywordarg
        if keyword == 'q':
            print()
            return
        keylist = load_pkl(pkl_path)
        if keyword not in keylist:
            print('No such key!')
        else:
            get_snippet(full_path, keyword)
    elif flag == '-c':
        if keywordarg == None:
            old_key = input('\nOld keyword: ')
        else:
            old_key = keywordarg
            
        if old_key == 'q':
            print()
            return
        keylist = load_pkl(pkl_path)
        if old_key not in keylist:
            print('No such key!')
        else:
            if new_keywordarg == None:
                new_key = input('New keyword: ')
            else:
                new_key = new_keywordarg
            if new_key == 'q':
                print()
                return
            if new_key == '':
                print('Invalid keyword!')
                return
            if new_key in keylist:
                print('keyword already exists')
                print()
                return
            else:
                change_key_name(full_path, pkl_path, old_key, new_key)
    elif flag == '-d':
        if keywordarg == None:
            keyword = input('\nkeyword: ')
        else:
            keyword = keywordarg
        if keyword == 'q':
            print()
            return
        keylist = load_pkl(pkl_path)
        if keyword not in keylist:
            print('No such key!')
        else:
            delete_snippet(full_path, keyword)
    elif flag == '-s':
        if keywordarg == None:
            keywordarg = ''
        search_keys(pkl_path, keywordarg)
        
def menu_help(filename):
    print('\n{} [FLAG] [KEY] [NEW KEY]'.format(filename))
    print('{} with no flag is menu'.format(filename))
    print('{} with flag only will allow chars not allowed in Bash'.format(filename))
    print('flags: ')
    print('\t-h\t--help')
    print('\t-v\t--view keys')
    print('\t-s\t--search keys')
    print('\t-w\t--write code snippet')
    print('\t-r\t--read code snippet')
    print('\t-c\t--change key name')
    print('\t\t\t{} -c [OLD KEY] [NEW KEY]'.format(filename))
    print('\t-d\t--delete key and code snippet')
if not os.path.isdir(dir_path):
    os.mkdir(dir_path)
    print('Creating dir', dir_path)
if not os.path.exists(full_path): #if full_path does not exist
    create_new_path(full_path)
    print('Creating path', full_path)
if not os.path.exists(pkl_path): 
    create_list = []
    create_pkl(pkl_path, create_list)
    print('Creating path', pkl_path)
if not os.path.exists(readme):
    readmetext(readme)

arg_len = len(sys.argv)
all_flag = ['-v', '-s', '-w', '-r', '-c', '-d']
filename = sys.argv[0]
def showhelp(filename):
    print('"{} -h" for help'.format(filename))

if arg_len == 1:
    showhelp(filename)
    menu(full_path, temp_path, pkl_path)
    sys.exit()
elif arg_len == 2:
    filename, flag = sys.argv
    if flag == '-h':
        menu_help(filename)
        sys.exit()
    else:
        pass
elif arg_len == 3:
    filename, flag, keyword = sys.argv
    if flag == '-w' or flag == '-v':
        print('flag "{}" does not take a key'.format(flag))
        sys.exit()
    if flag == '-c':
        print('flag -c cannot take only 1 arg')
        showhelp(filename)
        sys.exit()
elif arg_len > 3 and sys.argv[1] != '-c':
    filename = sys.argv[0]
    print('Too many arguments!')
    showhelp(filename)
    sys.exit()
elif sys.argv[1] == '-c':
    filename, flag, keyword, new_keyword= sys.argv

for index in all_flag:
    if flag == index:
        if arg_len == 2:
            menu_term(full_path, temp_path, pkl_path, flag)
            sys.exit()
        keylist = load_pkl(pkl_path)
        for key in keylist:
            if keyword == key or flag == '-s':
                try:
                    if keyword == key and new_keyword not in keylist:
                        #print('test', new_keyword)
                        menu_term(full_path, temp_path, pkl_path, flag, keyword, new_keyword)
                    else:
                        print('"{}" is already a key!'.format(new_keyword))
                    sys.exit()
                except NameError:
                    #tried to pass new_keyword but there is none
                    pass
                menu_term(full_path, temp_path, pkl_path, flag, keyword)
                sys.exit()

        print('Keyword "{}" does not exist!'.format(keyword))
        print('"{} -v" for current keywords'.format(filename))
        sys.exit()
#print('got flag: ', flag, 'and index of', index)
print('Unkown flag "{}"'.format(flag))
showhelp(filename)
sys.exit()


    

