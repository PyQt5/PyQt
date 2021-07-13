import sys
import time

sys.path.append(
    './build/lib.{0}-{1}.{2}'.format(sys.platform, sys.version_info.major, sys.version_info.minor))

from CalSpecSpea import calspecaccel
import matplotlib.pyplot as plt
import numpy as np

t1 = time.time()
acc = np.loadtxt('hf_acc.txt')
dt = 0.005
maxPeriod = 10.0
periodStep = 0.02
dampRatio = 0.05

Period, Fre, MAcc, MVel, MDis = calspecaccel(
    acc, acc.shape[0], dt, maxPeriod, periodStep, dampRatio)

print('Period[0]', Period[0])
print('Fre[0]', Fre[0])
print('MAcc[0]', MAcc[0])
print('MVel[0]', MVel[0])
print('MDis[0]', MDis[0])

t2 = time.time() - t1
print(t2)

plt.plot(Period, MAcc)
plt.show()
