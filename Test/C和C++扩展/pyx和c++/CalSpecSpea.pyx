#%%cython
import numpy as np
cimport numpy as np
np.import_array()

# 参考http://cython.readthedocs.io/en/latest/src/userguide/wrapping_CPlusPlus.html?highlight=cdef%20extern%20from
# 参考https://www.zhihu.com/question/23003213

cdef extern from "CalSpecSpeaLib.h":
    void cal_spec_accel(double acc[], int len, double dt, double maxPeriod, double periodStep, double dampRatio, double *Period, double *Fre, double *MAcc, double *MVel, double *MDis, int numt)

def calspecaccel(np.ndarray[double, ndim=1, mode="c"] acc, int length, double dt, double maxPeriod, double periodStep, double dampRatio):
    cdef int numt = int(maxPeriod / periodStep) + 1
    # 初始化各存储数据
    cdef np.ndarray[double, ndim=1] Fre = np.zeros(numt, float)
    cdef np.ndarray[double, ndim=1] MDis = np.zeros(numt, float)
    cdef np.ndarray[double, ndim=1] MVel = np.zeros(numt, float)
    cdef np.ndarray[double, ndim=1] MAcc = np.zeros(numt, float)
    #产生501个
    cdef np.ndarray[double, ndim=1] Period = np.arange(0.0, maxPeriod + periodStep, periodStep) # 10.0 + 0.02, 0.02
    Period[0] = 0.001
    # 调用CalSpecSpeaLib.cpp定义的函数对数组进行处理
    cal_spec_accel(<double*> np.PyArray_DATA(acc), length, dt, maxPeriod, periodStep, dampRatio,
        <double*> np.PyArray_DATA(Period), <double*> np.PyArray_DATA(Fre),
        <double*> np.PyArray_DATA(MAcc), <double*> np.PyArray_DATA(MVel),
        <double*> np.PyArray_DATA(MDis), numt)
    return Period, Fre, MAcc, MVel, MDis