# torch compile
import time
import numpy as np
import torch
import torch.nn as nn


class Timer:
    """Record multiple running times."""
    def __init__(self):
        self.times = []
        self.start()

    def start(self):
        """Start the timer."""
        self.tik = time.time()

    def stop(self):
        """Stop the timer and record the time in a list."""
        self.times.append(time.time() - self.tik)
        return self.times[-1]

    def avg(self):
        """Return the average time."""
        return sum(self.times) / len(self.times)

    def sum(self):
        """Return the sum of time."""
        return sum(self.times)

    def cumsum(self):
        """Return the accumulated time."""
        return np.array(self.times).cumsum().tolist()

class benchmark:
    def __init__(self, desciption='Done'):
        self.description = desciption

    def __enter__(self):
        self.timer = Timer()
        return self
    
    def __exit__(self, *args):
        print(f'{self.description}: {self.timer.stop():.4f} sec')


# script
# toy network

# sequential
def get_sequentialNet():
    net = nn.Sequential(nn.Linear(512, 256),
                        nn.ReLU(),
                        nn.Linear(256, 128),
                        nn.ReLU(),
                        nn.Linear(128, 2))
    return net
device = torch.device("cuda")
x = torch.randn(size=(1, 1, 512), device=device)


net = get_sequentialNet()
net.to(device)

net.eval()
print( net(x) )


# eager mode
with benchmark('eager: warm up'):
    for i in range(5):
        net(x)

with benchmark('eager: 1000 loop'):
    for i in range(1000):
        net(x)












# compile
with benchmark('compile:'):
    compile_net = torch.compile(get_sequentialNet().to(device))

compile_net.eval()

print( compile_net(x) )



with benchmark('compile: warm up'):
    for i in range(5):
        compile_net(x)

with benchmark('compile: 1000 loop'):
    for i in range(1000):
        compile_net(x)


