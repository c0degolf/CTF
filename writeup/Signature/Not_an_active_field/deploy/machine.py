import numpy as np

def theta(a, b):
    return 1 if a == b else 0

class TreeParityMachine:
    def __init__(self, k = 3, n = 4, l = 6, rule = "hebian"):
        '''
        k - number of hidden neurons
        n - number of input neurons
        l - range of each weight [-l, l]
        '''
        self.k = k
        self.n = n
        self.l = l
        self.W = np.random.randint(-l, l+1, (k, n))
        self.rule = rule
        
    def forward(self, x):
        '''
        x - input vector
        '''
        self.x = x.reshape(self.W.shape)
        self.roe = np.sign(np.sum(self.W * self.x, axis = 1))
        self.tau = np.prod(self.roe)
        return self.tau
    
    def hebian(self, tau):
        for (i, j), _ in np.ndenumerate(self.W):
            self.W[i, j] +=  self.x[i, j] * self.roe[i] * theta(self.tau, tau) * theta(self.roe[i], self.tau)
            self.W[i, j] = np.clip(self.W[i, j], -self.l, self.l)
            
    def anti_hebian(self, tau):
        for (i, j), _ in np.ndenumerate(self.W):
            self.W[i, j] -=  self.x[i, j] * self.roe[i] * theta(self.tau, tau) * theta(self.roe[i], self.tau)
            self.W[i, j] = np.clip(self.W[i, j], -self.l, self.l)
    
    def random_walk(self, tau):
        for (i, j), _ in np.ndenumerate(self.W):
            self.W[i, j] +=  self.x[i, j] * theta(self.tau, tau) * theta(self.roe[i], self.tau)
            self.W[i, j] = np.clip(self.W[i, j], -self.l, self.l)
    
    
    def backward(self, tau):
        if self.rule == "hebian":
            self.hebian(tau)
        elif self.rule == "anti_hebian":
            self.anti_hebian(tau)
        elif self.rule == "random_walk":
            self.random_walk(tau)
    
if __name__ == "__main__":
    tpm = TreeParityMachine()
    print(tpm.forward(np.random.randint(-10, 10, tpm.n * tpm.k)))
    tpm.backward(1)