#!/usr/bin/env python3

import os
import signal

class SmolPRNG:
    # Wow, so small, faster than Python random (probably)!

    def __init__(self, seed: bytes=None):
        if seed is None:
            seed = os.urandom(64)
        assert len(seed) == 64

        self.state = [ int.from_bytes(seed[i:i+4], 'little') for i in range(0, 64, 4) ]
        self.counter = 0
        
        for _ in range(1000):
            self._step()

    def _step(self):
        consts = [
            [0, 0xa0e37a42],
            [0, 0xa57f1a93],
            [0, 0x83bb9b44]
        ]

        for i in range(16):
            i1, i2 = [(i + j + 1) % 16 for j in range(2)]
            self.state[i] = (
                (self.state[i] >> 1) ^ consts[0][self.state[i] & 1]
                ^ (self.state[i1] >> 1) ^ consts[1][self.state[i1] & 1]
                ^ (self.state[i2] >> 1) ^ consts[2][self.state[i2] & 1]
            )

        self.counter = 0

    def gen(self) -> int:
        if self.counter == 16:
            self._step()
        
        y = self.state[self.counter]
        y ^= (y >> 7)
        y ^= (y << 11) & 0xb5547000
        y ^= (y << 13) & 0xf5230000
        y ^= (y >> 17)
        
        self.counter += 1
        return y


if __name__ == "__main__":
    prng = SmolPRNG()

    print("Here are some random values:")
    for i in range(50):
        print(prng.gen() & 0xffff)
    signal.alarm(10)

    print("Can you guess the next values?")
    for i in range(16):
        user_input = int(input("> "))
        value = prng.gen()

        if value == user_input:
            print("Correct!")
        else:
            print("Wrong.")
            exit(0)
    
    flag = os.environ.get('CHALLENGE_FLAG', 'DH{test_flag}')
    print(f"Congratz! Here's the flag: {flag}")
