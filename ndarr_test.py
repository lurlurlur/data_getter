import numpy as np
import time

lur = np.random.rand(5, 3, 2)
print(lur)
rng = np.random.default_rng(int((time.time() * 10000) % 10000))

sample = rng.choice(range(5), 5, replace=True)
print(sample)
print(lur[sample, :, :])

arr = np.array([1, 2, 3, 4, 5, 6])
n = arr.shape[0]
s1 = np.sum(arr)
s2 = np.sum(arr ** 2)

t1 = s2 / (n - 1)
t2 = s1 ** 2 / (n * (n - 1))
print(np.sqrt(t1 - t2))

m = np.mean(arr)
d2s = np.sum((arr - m) ** 2)
print(np.sqrt(d2s / (n - 1)))
