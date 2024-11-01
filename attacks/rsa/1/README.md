# Common modulus attack
### required
+ two ciphertexts which encrypted with same N, plaintext
+ GCD(e1, e2) == 1

$$c_1 = m^{e_1}\ mod\ N$$
$$c_2 = m^{e_2}\ mod\ N$$

Attacker can find (u, v) that satisfy $u*e_1+v*e_2=1$ by EEA.

$$c_1^u*c_2^v=m^{u*e_1}*m^{v*e_2}=m^{u*e_1+v*e_2}=m^1\ mod\ N$$