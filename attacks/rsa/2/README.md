# Cube attack
### required
+ small e
+ $m < \sqrt[e]{N}$

$$c=m^e\ mod\ N$$
$$m=\sqrt[3]{c+kN}$$

We can use sage's `ZZ(c).nth_root(e)`method.