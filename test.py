#!/usr/bin/env python3

""" Tests the program """

import sys
import os
import subprocess

tests = {
    "#examples/conditions.fd": ['4', '"1 + 3 برابر است با؟"\n"آفرین درسته!"'],
    "examples/conditions.fd": ['7', '"1 + 3 برابر است با؟"\n"نادرسته."'],
    "examples/helloworld.fd": '"سلام، دنیا!"',
    "examples/function.fd": '"ناموفق"',
    "examples/name.fd": ['hello', '"نام خود را وارد کنید"\n"سلام ""hello"'],
    "examples/tests/semi_space.fd": ['hello', '"hello"'],
    "examples/loop.fd": '''"شماره "1
"شماره "2
"شماره "3
"شماره "4
"شماره "5
"شماره "6
"شماره "7
"شماره "8
"شماره "9
"شماره "10
0
0
0
0
0
0
0
0
0
0
'''
}
"""This variable is a list to declaring tests
Structure:
[
    ["test-script-file-name", "Output to assert"]
    ["test-script-file-name2", "Output to assert2..."]
    ["test-script-file-name2", ["stdin input", "Output to assert2..."]]
]
"""

if os.name == 'nt':
    # is windows
    interpreter_cmd = ['python', 'ferdowsi.py']
else:
    interpreter_cmd = ['python3', 'ferdowsi.py']

print('Running tests...')

# running tests
for test in tests:
    print('testing ' + test + '...', end=' ')
    filename = test.replace('#', '')
    if os.name == 'nt':
        filename = filename.replace('/', '\\')
    stdin = ''
    tmp = tests[test]
    if type(tmp) == list:
        stdin = tmp[0]
        expected_output = tmp[1].strip()
    else:
        expected_output = tmp.strip()
    
    # run the script
    output = subprocess.check_output([*interpreter_cmd, filename], input=stdin.encode(), stderr=open(os.devnull, 'w')).decode().strip()
    # check output
    try:
        assert output == expected_output
        print('\033[32mPASS\033[0m')
    except AssertionError:
        print('\033[31mAssertion error for ' + filename + ': output "' + output + '" is not equals expected output "' + expected_output + '"')
        raise
        sys.exit(1)

print('\033[32mAll of ' + str(len(tests)) + ' tests passed successfully\033[0m')
