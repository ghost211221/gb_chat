"""Лаунчер"""

import subprocess
import sys

PROCESS = []

NUMOFCLIENTS = 3

if len(sys.argv) > 1:
    NUMOFCLIENTS = int(sys.argv[1])

while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESS.append(subprocess.Popen('python server/src/serverMain.py',
                                        creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(NUMOFCLIENTS):
            PROCESS.append(subprocess.Popen(f'python client/src/clientMain.py',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()
