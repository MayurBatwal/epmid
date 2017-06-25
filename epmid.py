import pandas as pd
import math

class Node:
	value = ''
	children = []


def epmid(d, attr_val, df, Class, Class_label):
	y = list(df[Class_label])
	p = y.count(Class[0]) * 1.0
	n = y.count(Class[1]) * 1.0

	PC = []
	NC = []
	PCprob = []
	NCprob =[]

	for i in range(len(d)):
		cy = 0
		cn = 0
		for j in d[i]:
			if(y[j] == Class[0]):
				cy = cy + 1
			else:
				cn = cn + 1
		if(cy > 0 or cn > 0):
			if((cy / p) >= (cn / n)):
				PC.append(attr_val[i])
			else:
				NC.append(attr_val[i])

	prob = []


	b = 1.0 / len(d)
	c = p / (p + n)
	for i in PC:
		k = attr_val.index(i)
		cy = 0.0
		cn = 0.0
		for j in d[k]:
			if(y[j] == Class[0]):
				cy = cy + 1
			else:
				cn = cn + 1
		a = cy / (cy + cn)

		prob.append((a * b) / c)


	l = [[i] for i in range(len(prob))]

	while(1):
		l2 = list(l)
		l1 = [list(set(l[i] + l[j])) for i in range(len(l)) for j in range(i + 1, len(l))
			if all(abs(prob[m] - prob[n]) <= 0.1 for m in l[i] for n in l[j]) ]

		for i in l1:
			l.append(i)

		l1 = []
		for i in l:
			if(i not in l1):
				l1.append(i)

		l = list(l1)

		if(l == l2):
			break

	l1 = l[::-1]

	l = []
	for i in range(len(l1)):
		subs = False
		for j in range(i):
			if(set(l1[i]) < set(l1[j])):
				subs = True
				break
		if(subs == False):
			l.append(l1[i])


	lpos = list(l)




	#negative
	prob = []

	b = 1.0 / len(d)
	c = n / (p + n)
	for i in NC:
		k = attr_val.index(i)
		cy = 0.0
		cn = 0.0
		for j in d[k]:
			if(y[j] == Class[0]):
				cy = cy + 1
			else:
				cn = cn + 1
		a = cn / (cy + cn)

		prob.append((a * b) / c)


	l = [[i] for i in range(len(prob))]

	while(1):
		l2 = list(l)
		l1 = [list(set(l[i] + l[j])) for i in range(len(l)) for j in range(i + 1, len(l))
			if all(abs(prob[m] - prob[n]) <= 0.1 for m in l[i] for n in l[j]) ]

		for i in l1:
			l.append(i)

		l1 = []
		for i in l:
			if(i not in l1):
				l1.append(i)

		l = list(l1)

		if(l == l2):
			break

	l1 = l[::-1]

	l = []
	for i in range(len(l1)):
		subs = False
		for j in range(i):
			if(set(l1[i]) < set(l1[j])):
				subs = True
				break
		if(subs == False):
			l.append(l1[i])


	lneg = list(l)


	d2 = []
	a2 = []

	for i in lpos:
		m = []
		s = ""
		for j in i:
			m = m + d[attr_val.index(PC[j])]
			s = s + PC[j] + " "
		d2.append(m)
		a2.append(s)

	for i in lneg:
		m = []
		s = ""
		for j in i:
			m = m + d[attr_val.index(NC[j])]
			s = s + NC[j] + " "
		d2.append(m)
		a2.append(s)

	
	return d2, a2

	



	

def attr_selection(df, attributes, attr_values, Class, Class_label):
	y = list(df[Class_label])

	p = list(y).count(Class[0]) * 1.0
	n = list(y).count(Class[1]) * 1.0
	t = len(y)

	E = -((p / t) * math.log((p / t), 2)) - ((n / t) * math.log((n / t), 2)) 

	gain = [0] * len(attributes)

	for i in range(len(attributes)):	
		attr_val = attr_values[i]

		l = list(df[attributes[i]])
		d = [[] for j in range(len(attr_val))]
		for j in range(len(y)):
			d[attr_val.index(l[j])].append(y[j])

		Ei = 0
		for j in range(len(attr_val)):
			p = list(d[j]).count(Class[0]) * 1.0
			n = list(d[j]).count(Class[1]) * 1.0
			t = p + n
			if(p == 0 or n == 0):
				w = 0
			else:
				w = (p * math.log((p / t), 2)) + (n * math.log((n / t), 2))
			Ei = Ei - (w)

		Ei = Ei / len(y)
		gain[i] = E - Ei

			
	return gain.index(max(gain))



def decisionTree(df, attributes, attr_values, level, Class, Class_label, prnt):
	N = Node()
	N.children = []

	y = list(df[Class_label])
	if(y.count(Class[0]) == len(y)):
		N.value = Class[0]
		if(prnt):
			print " " * level * 5, "class : ", N.value
		return N
	if(y.count(Class[1]) == len(y)):
		N.value = Class[1]
		if(prnt):
			print " " * level * 5, "class : ", N.value
		return N

	if(len(attributes) == 0):
		if(y.count(Class[0]) >= y.count(Class[1])):
			N.value = Class[0]
		else:
			N.value = Class[1]
		if(prnt):
			print " " * level * 5, "class : ", N.value
		return N

	best_attr = attr_selection(df, attributes, attr_values, Class, Class_label)
	if(prnt):
		print " " * level * 5, "Node : ", attributes[best_attr]
	N.value = attributes[best_attr]

	attr_val = attr_values[best_attr]   
	l = list(df[attributes[best_attr]]) 

	del attributes[best_attr]
	del attr_values[best_attr]


	d = [[] for j in range(len(attr_val))]
	for j in range(len(l)):
		d[attr_val.index(l[j])].append(j)

	
	d, attr_val = epmid(d, attr_val, df, Class, Class_label)		#####EPMID


	for i in range(len(attr_val)):
		if(prnt):
			print " " * level * 5, "branch : ", attr_val[i]
		k = 0
		dfi = pd.DataFrame(columns = df.columns)
		for j in d[i]:
			dfi.loc[k] = df.loc[j]
			k = k + 1

		if(len(dfi) == 0):
			if(y.count(Class[0]) >= y.count(Class[1])):
				N.value = Class[0]
			else:
				N.value = Class[1]
			print " " * level * 5, "class : ", N.value
		else:
			N.children.append(decisionTree(dfi, list(attributes), list(attr_values), level + 1, Class, Class_label, prnt))

	return N



def DecisionTreeEPMID(file, Class_label, prnt=False):
	df = pd.read_csv(file)

	attributes = list(df.columns)
	attributes.remove(Class_label)

	attr_values = []
	for i in attributes:
		attr_values.append(list(set(df[i])))

	Class = list(set(df[Class_label]))


	a = decisionTree(df, attributes, attr_values, 0, Class, Class_label, prnt)
	return a
