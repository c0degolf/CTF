# LLL

$m_{(2)}=m_{n-1}...\ m_{0};\ m_n=0,1$\
$C=\sum\limits_{k=0}^{n-1} pub_km_k$

$$
M = 
\begin{bmatrix}
I_{n\times n} & pub_{n\times 1} \\
-\frac{1}{2}_{1\times n} & -C
\end{bmatrix}
$$

Applying LLL to M, we find a vector that contains a FLAG.