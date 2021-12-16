from pprint import pprint
from os import walk


def check_UE(lines):
    vulnerable = False
    vulnerable_lines = []
    for line_num in range(len(lines)):
        line = lines[line_num].lstrip()

        # get rid of comments and brackets
        if line[:2] == '/*' or line[:2] == '* ' or line[:2] == '//' or line[:2] == '*/' \
                or line[:1] == '{' or line[:1] == '}':
            continue

        # for each of the interested functions [call(), callcode(), deleagtecall(), send()], check if their return value
        # is being handled:
        #   either by an if statement, or by using the require() function;
        #
        #   edge case: saving the return value as a local variable and check using if in the next line
        #       edge case of the edge case: using a short notation of IF ELSE condition (using ? and :)
        if '.call.' in line or '.call(' in line:
            if 'if ' in line[:line.find('.call')] or 'require(' in line[:line.find('.call')]:
                continue
            else:
                # print('unhandled call()')
                vulnerable = True
                vulnerable_lines.append(line_num + 1)

        elif '.callcode' in line:
            if 'if ' in line[:line.find('.callcode')] or 'require(' in line[:line.find('.callcode')]:
                continue
            else:
                # print('unhandled callcode()')
                vulnerable = True
                vulnerable_lines.append(line_num + 1)

        elif '.delegatecall' in line:
            if 'if ' in line[:line.find('.delegatecall')] or 'require(' in line[:line.find('.delegatecall')]:
                continue
            else:
                # print('unhandled delegatecall()')
                vulnerable = True
                vulnerable_lines.append(line_num + 1)

        elif '.send(' in line:
            if 'if ' in line[:line.find('.send(')] or 'require(' in line[:line.find('.send(')]:
                continue
            else:
                # print('unhandled send()')
                vulnerable = True
                vulnerable_lines.append(line_num + 1)

        # edge case
        if '=' in line and ('.call.' in line or '.call(' in line
                            or '.callcode' in line or '.delegatecall' in line or '.send(' in line):
            variable_name = line[:line.find('=')].split()[-1]
            next_line = lines[line_num + 1].lstrip()
            if next_line.split()[0] == 'if' and variable_name in next_line.split()[1]:
                continue
            elif '?' in next_line and ':' in next_line:
                if variable_name in next_line[next_line.find('?'): next_line.find(':')]:
                    continue
            else:
                if not line_num + 1 in vulnerable_lines:
                    vulnerable = True
                    vulnerable_lines.append(line_num + 1)

    return vulnerable, vulnerable_lines


if __name__ == '__main__':

    # get a list of Solidity files (with .sol extension) under a given directory
    f = []
    vulnerable_files = []
    for (dirpath, dirnames, filenames) in walk('./unchecked_low_level_calls'):
        for file in filenames:
            if file[-4:] == '.sol':
                f.append(file)
                file_obj = open(dirpath + '/' + file, 'r')
                vulnerable, vulnerable_lines = check_UE(file_obj.readlines())
                if vulnerable:
                    vulnerable_files.append((file, vulnerable_lines))
        break
    pprint(vulnerable_files)
    print(len(f))
    print(len(vulnerable_files))
