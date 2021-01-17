import csv
import inspect
import click
import pygraphviz as pgv
import tempfile
from shutil import copyfile

@click.command()
@click.option('--input',  help='call stack file')
@click.option('--output', help='call stack graph photo')
def analyze(input, output):
    """generate call stack photo"""
    click.echo('Hello %s!' % input)


## 建立调用栈
def build_callstack() -> list:
    callstack = []
    frame = inspect.currentframe()
    depth = 0
    # get frame depth
    while frame:
        frame = frame.f_back
        depth += 1
    frame = inspect.currentframe()
    # build call stack
    while frame:
        code = frame.f_code
        file = code.co_filename
        method = code.co_name
        line = code.co_firstlineno
        call_info = CallInfo(depth, file, method, line)
        callstack.append(call_info)
        depth -= 1
        frame = frame.f_back
    return callstack


## 生成调用栈关系图
def output_callstack_photo(callstack, path):
    G = pgv.AGraph(strict=False, directed=True)
    subgraph_set = {}
    for call_info in callstack:
        node = '{0}:{1}:{2}'.format(call_info.file, call_info.line, call_info.method)
        if call_info.file not in subgraph_set:
            subgraph_set[call_info.file] = G.add_subgraph(
                name='cluster' + call_info.file,
                label=call_info
            )
        subgraph = subgraph_set[call_info.file]
        subgraph.add_node(
            node,
            label='{0}:{1}'.format(call_info.line, call_info.method)
        )

    for index, start in enumerate(callstack):
        if index + 1 < len(callstack):
            start_filename = start.file
            start_line = start.line
            start_function = start.method
            start_subgraph = subgraph_set[start_filename]
            end = callstack[index + 1]
            end_filename = end.file
            end_line = end.line
            end_function = end.method
            end_subgraph = subgraph_set[end_filename]

            if index == 0:
                color = 'green'
            elif index == len(callstack) - 2:
                color = 'red'
            else:
                color = 'black'

            G.add_edge(
                '{0}:{1}:{2}'.format(start_filename,
                                     start_line,
                                     start_function),
                '{0}:{1}:{2}'.format(end_filename,
                                     end_line,
                                     end_function),
                color=color,
                ltail=start_subgraph.name,
                lhead=end_subgraph.name,
                label='#{0} at {1}'.format(index + 1, start_line)
            )

        fd, temp = tempfile.mkstemp('.png')
        G.draw(temp, prog='dot')
        G.close()
        copyfile(temp, path)


def get_call_stacks(path):
    file = open(path, "w")
    csv_reader = csv.reader(file)
    calls = []
    for call_info in csv_reader:
        num = int(call_info[0])
        file = call_info[1]
        method = call_info[2]
        line = call_info[3]
        call = CallInfo(num, file, method, line)
        calls.append(call)
    return calls


class CallInfo:

    def __init__(self, num, file, method, line):
        self.num = num
        self.file = file
        self.method = method
        self.line = line

    def __cmp__(self, other) -> int:
        if self.num > other.num:
            return 1
        elif self.num == other.num:
            return 0
        else:
            return -1

if __name__ == "__main__":
    analyze()

