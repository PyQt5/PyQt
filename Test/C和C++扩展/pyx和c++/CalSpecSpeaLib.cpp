#include "CalSpecSpeaLib.h"

#include <stdio.h>
#include <iostream>
#include <math.h>
using namespace std;


double maxabs(double num[], int len)
{
    //略
    return abs(num[0]);

}
bool isALLvaluezero(double num[], int len)
{
    //略
    return false;

}
void cal_spec_accel(double acc[], int len, double dt, double maxPeriod, double periodStep, double dampRatio, double *Period, double *Fre, double *MAcc, double *MVel, double *MDis, int numt)
{
    //略
    Period[0] = 99.95;
    Fre[0] = 99.96;
    MAcc[0] = 99.97;
    MVel[0] = 99.98;
    MDis[0] = 99.99;
}

int main()
{
    double acc[20] = { 0.0038,0.0049,0.0061,0.0075,0.0088,0.01,0.0112,0.0123,0.0133,0.0140,0.0146,0.0152,0.0157,0.0162,0.0167,0.0172,0.0175,0.0178,0.0179,0.0179 };
    int len = 20;
    double dt = 0.005;
    double maxPeriod = 10.0;
    double periodStep = 0.02;
    double dampRatio = 0.05;
    int numt = int(maxPeriod / periodStep) + 1;
    double *Fre = new double[numt];
    double *MDis = new double[numt];
    double *MVel = new double[numt];
    double *MAcc = new double[numt];
    double *Period = new double[numt];
    for (int i = 0; i<numt; i++) {
        Period[i] = periodStep*i;
        Fre[i] = 0;
        MDis[i] = 0;
        MVel[i] = 0;
        MAcc[i] = 0;
    }
    Period[0] = 0.001;
    //cal_spec_accel(double acc[], int len,double dt,double maxPeriod,double periodStep,double dampRatio,double *Period,double *Fre,double *MAcc,double *MVel,double *MDis)
    cal_spec_accel(acc, len, dt, maxPeriod, periodStep, dampRatio, Period, Fre, MAcc, MVel, MDis, numt);
    
    for (int i = 0; i<numt; i++)
    {
        cout << MAcc[i] << endl;
    }
    
    delete[] Fre;
    return 0;
}