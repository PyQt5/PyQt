import sys

sys.path.insert(0, './Release')

import pydext

print(pydext)
print(dir(pydext))

print(pydext.__author__)
print(pydext.__mail__)

print(pydext.hello())

print(pydext.hello2('Irony'))

print(pydext.sum(1, 5))

# 结果变负数
print(pydext.sum(1, 5, minus=True))
