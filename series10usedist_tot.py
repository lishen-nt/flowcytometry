import csv
from pylab import *
import numpy

directory = '/home/hduser/FlowCAP-II/Data/AML/'

GetNames= lambda y: [directory + 'CSV/%04d.CSV' % ((y-1)*8+i) for i in range(1,8)]
ConR= lambda y: [log10(float(y[0])),float(y[1])]+[float(i) for i in y[2:]]
ReadF= lambda y: [ConR(i) for i in [row for row in csv.reader(open(y,'rb'))][1:]]

myranges=[arange(2.01,3.01,0.1)]+[arange(0.01,1.01,0.1) for i in range(6)]
ibin=[[myranges[1],myranges[4],myranges[0],myranges[i]] for i in [2,3,5,6]]
iex=[(1,4,0,i) for i in [2,3,5,6]]
ll=len(ibin)

def doSomething(xx, hh1, hh2, yn=1):
	a=array(ReadF(xx))
	H=range(ll)
	edges=range(ll)
	for i in range(ll):
		H[i], edges[i] = histogramdd(a[:,iex[i]], bins=ibin[i])
	hh1=[hh1[i]-yn*H[i] for i in range(ll)]
	epsi=[1e-10 for i in range(ll)]
	peq1=[(epsi[i]+hh1[i])/sum(epsi[i]+hh1[i]) for i in range(ll)]
	peq2=[(epsi[i]+hh2[i])/sum(epsi[i]+hh2[i]) for i in range(ll)]
	pne=[(epsi[i]+H[i])/sum(epsi[i]+H[i]) for i in range(ll)]
	slocal1=[pne[i]*log(pne[i]/peq1[i]) for i in range(ll)]
	slocal2=[pne[i]*log(pne[i]/peq2[i]) for i in range(ll)]
	return [sum(slocal1[i])-sum(slocal2[i]) for i in range(ll)]


Tset=[row for row in csv.reader(open(directory + 'DREAM6_AML_TrainingSet.csv','rb'))]

AMLTs=[int(i[0]) for i in Tset if i[1]=='AML']
NormalTs=[int(i[0]) for i in Tset if i[1]=='Normal']


rr=range(7)

Ha=[[numpy.load(directory + 'hist_a_%d_%d.npy'%(j, i)) for i in range(ll)] for j in rr]
Hn=[[numpy.load(directory + 'hist_n_%d_%d.npy'%(j, i)) for i in range(ll)] for j in rr]

for j in AMLTs[:]:
	res=zeros(ll)
	for i in rr: 
		rest=doSomething(GetNames(j)[i], Ha[i], Hn[i])
		print j, rest
		res+=rest
	print 0, sum(res), j, 9345677


for j in NormalTs[:]:
	res=zeros(ll)
	for i in rr: 
		rest=doSomething(GetNames(j)[i], Hn[i], Ha[i])
		print j, [-i for i in rest]
		res+=rest
	print 1, -sum(res), j, 9345677

f=open(directory + "./DREAM6_AML_Predictions_team21u.txt",'w')
for j in range(180,360):
	res=zeros(ll)
	for i in rr:
		rest=doSomething(GetNames(j)[i], Ha[i], Hn[i], 0)
		print j, rest
		res+=rest
	print 2, sum(res), j, 9345677
	f.write("%d\t%f\t%f\n" % (j,1/(1+exp(sum(res))), sum(res)))
	f.flush()
f.close()

#( python -O -u series10usedist_tot.py ) > salic.txt &
#cat salic.txt | grep 9345677 | sort -n -k 1 -k 2 | cut -f 1-3 -d " "
#cat DREAM6_AML_Predictions_team21u.txt |  sort -n -k 3 | cut -f 1,2 > DREAM6_AML_Predictions_team21.txt
