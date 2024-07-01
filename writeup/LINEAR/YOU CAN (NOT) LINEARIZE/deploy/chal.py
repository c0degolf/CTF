import signal


def timeout(signum, frame):
    print("Timeout!!!")
    signal.alarm(0)
    exit(0)


signal.signal(signal.SIGALRM, timeout)
signal.alarm(10)


import numpy as np
import random


X = np.array([[random.randrange(251) for j in range(4)] for i in range(4)])

for k in range(4):
    A = np.array([[random.randrange(251) for j in range(4)] for i in range(4)])
    B = X.T @ A @ X % 251

    for i in range(4):
        print(A[i], B[i])
    print()

assert X.flatten().tolist() == [int(_) for _ in input("X > ").split(",")]

with open("flag", "r") as f:
    print(f.read())
