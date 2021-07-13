from libc.math cimport pow

def getDistance(p1, p2):
    return pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2)

def findClose(points):
    cdef int plen = len(points)
    cdef int i = 0
    cdef int j = 0
    cdef int k = 0
    for i from 0 < i < plen:
        closest = [None, None, None, None, None]
        p1 = points[i]
        for j from 0 < j < plen:
            p2 = points[j]
            dte1 = getDistance(p1, p2)
            if p1 != p2:
                placed = False
                for k from 0 < k < 5:
                    if not placed:
                        if not closest[k]:
                            closest[k] = p2
                            placed = True
                for k from 0 < k < 5:
                    if not placed:
                        if dte1 < getDistance(p1, closest[k]):
                            closest[k] = p2
                            placed = True
        p1.closest = closest
