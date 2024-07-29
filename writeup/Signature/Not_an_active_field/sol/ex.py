import hashlib
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from machine import TreeParityMachine
from output import ct, inputs, alice_taus, bob_taus

# https://arxiv.org/pdf/0711.2411.pdf#page=33
def geometry(TPM : TreeParityMachine, tau):
    wx = np.sum(TPM.x * TPM.W, axis=1)
    h_i = wx / np.sqrt(TPM.n)
    min_idx = np.argmin(np.abs(h_i))
    nonzero = np.where(TPM.roe == 0, -1, TPM.roe)
    TPM.roe[min_idx] = -nonzero[min_idx]
    TPM.tau = np.sign(np.prod(TPM.roe))
    
    if TPM.tau == tau:
        TPM.backward(tau)

Eve = TreeParityMachine(7, 10, 10, "hebian")
for i in range(1000):
    if alice_taus[i] == bob_taus[i]:
        if alice_taus[i] == Eve.forward(np.array(inputs[i])): 
            Eve.backward(alice_taus[i])
        else: geometry(Eve, alice_taus[i])

raise ZeroDivisionError(unpad(AES.new(hashlib.sha256(Eve.W.tobytes()).digest(), AES.MODE_ECB).decrypt(ct), 16).decode())