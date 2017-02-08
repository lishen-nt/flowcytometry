import csv
from pylab import *
import numpy


GetNames= lambda y: ['CSV/%04d.CSV' % ((y-1)*8+i) for i in range(1,8)]
ConR= lambda y: [log10(float(y[0])),float(y[1])]+[float(i) for i in y[2:]]
ReadF= lambda y: [ConR(i) for i in [row for row in csv.reader(open(y,'rb'))][1:]]

myranges=[arange(2.01,3.01,0.1)]+[arange(0.01,1.01,0.1) for i in range(6)]
ibin=[[myranges[1],myranges[4],myranges[0],myranges[i]] for i in [2,3,5,6]]
iex=[(1,4,0,i) for i in [2,3,5,6]]
ll=len(ibin)

def doSomething(xx, hh):
	a=array(ReadF(xx))
	H=range(ll)
	edges=range(ll)
	for i in range(ll):
		H[i], edges[i] = histogramdd(a[:,iex[i]], bins=ibin[i])
	return [H[i]+hh[i] for i in range(ll)]

Tset=[row for row in csv.reader(open('DREAM6_AML_TrainingSet.csv','rb'))]

AMLTs=[int(i[0]) for i in Tset if i[1]=='AML']
NormalTs=[int(i[0]) for i in Tset if i[1]=='Normal']


rr=range(7)

H=[[zeros([len(i)-1 for i in ibin[k]]) for k in range(ll) ] for j in rr]
for j in AMLTs[:]:
	for i in rr: 
		print j
		H[i]=doSomething(GetNames(j)[i], H[i])
		for k in range(ll):
			numpy.save('hist_a_%d_%d.npy'% (i, k),H[i][k])

H=[[zeros([len(i)-1 for i in ibin[k]]) for k in range(ll) ] for j in rr]
for j in NormalTs[:]:
	for i in rr: 
		print j
		H[i]=doSomething(GetNames(j)[i], H[i])
		for k in range(ll):
			numpy.save('hist_n_%d_%d.npy'% (i, k),H[i][k])
