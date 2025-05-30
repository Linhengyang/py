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

x = torch.randn(size=(512, 10, 512))

net = get_sequentialNet()


print( net(x) )

compile_net = torch.compile(net)

print( compile_net(x) )

with benchmark('without torchcompile'):
    for i in range(10000):
        net(x)


with benchmark('with torchcompile'):
    for i in range(10000):
        compile_net(x)


