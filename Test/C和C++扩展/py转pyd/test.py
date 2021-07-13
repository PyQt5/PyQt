import sys

sys.path.insert(0,
                './build/lib.{0}-{1}.{2}'.format(sys.platform, sys.version_info.major,
                                                 sys.version_info.minor))

import pydmod

print(pydmod)
print(pydmod.sum(1, 5))
