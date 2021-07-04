# # This is a sample Python script.
#
# # Press ⌃R to execute it or replace it with your code.
# # Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
import os
from multiprocessing import Process
from multiprocessing.pool import Pool


def info(title):
    print(title)
    print('module name:', __name__, 'parent process:', os.getppid(), 'process id:', os.getpid())

def f(x):
    info("f(" + str(x) + ")")
    return x*x

if __name__ == '__main__':
    info('main line')
    # with Pool(5) as p:
    #     print(p.map(f, [1, 2, 3]))
    p = Process(target=f, args=(1,))
    p.start()
    p.join()