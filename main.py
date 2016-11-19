###########################################################
#                  Data Mining KTH
#         Homework 1: Finding similar items 
###########################################################


import numpy as np
import copy as cp
import random
import itertools
###########################################################
#                       Class definition
###########################################################
class Shingling:

	def __init__(self, doc, size=5):
		''' Construct shingles of length size (default value 5) 
		    from the document name given
		'''
		self.k=size # shingle size
		self.file=doc 
		self.hashed_values=set()

	def shingle(self):
		fi=open(self.file, 'r')
		text=str()
		for line in fi:
			text=text+line # layout of the document taken in count
		for i in xrange(len(text)-self.k+1): # -k to avoid to create shingle under specified size, +1 because it can be <= of len(text)
			#print len(text[i:i+self.k])
			self.hashed_values.add(hash(text[i:i+self.k]))
		fi.close()


class MinHashing:
	def __init__(self, sets, n=10): 
		self.sets=sets # sets are under hashed value forms, given in a listas set
		self.nPermutations=n 
		self.key=list(set(itertools.chain.from_iterable(self.sets)))
		self.M=self.characteristic_matrix()
		self.signM=None

	def characteristic_matrix(self):
		''' Creates the characteristic matrix of sets, only returns the positions where there is 1.   M(# shnigles, # sets); we count row per row (i.e: index k means where at the k//i row and k%i column) 
		''' 
		#M2=np.zeros((len(self.key), len(self.sets))) # if we want to see the sparse matrix
		M=list()		
		for i in xrange(len(self.key)):
			for j in xrange(len(self.sets)):
				hash_list=list(self.sets[j])
				k=0
				while k <len(hash_list) and hash_list[k]!=self.key[i]:
					k+=1
				if k<len(self.sets[j]):
					M.append(i*len(self.sets)+j)
					#M2[i,j]=1	
		return M

	def permutations(self):
		''' Permute randomly the sequence of the keys of hash_value dictionary
		'''
		permute=cp.deepcopy(self.key)
		random.shuffle(permute)
		return permute

	def findShinglePositions(self, hashValue):
		for i in xrange(len(self.key)):
			if hashValue==self.key[i]:
				return i
		print 'Hash value in permutation not in the list of hash values; ERROR!!'

	def minhash(self):
		''' For one permutation, return the associated row in the signature matrix
		'''
		p=self.permutations()
		rowSign=np.zeros(len(self.sets), dtype=int)
		for j in xrange(len(self.sets)):
			for i in xrange(len(p)):
				pos=self.findShinglePositions(p[i])
				if pos*len(self.sets)+j in self.M:
					rowSign[j]=i+1 # Position in sign matrix starts to one (like in the slides)
					break # We find the first position				
		return np.transpose(rowSign) # return row of signature matrix

	def signMatrix(self):
		self.signM=np.zeros((self.nPermutations, len(self.sets)))
		for n in xrange(self.nPermutations):
			self.signM[n,:]=self.minhash()

	def compareSignatures(self, sign1, sign2):
		inter=0
		union=0
		for i in xrange(len(sign1)):
			if sign1[i]==sign2[i]:
				inter+=1
			else:
				union+=1 # perform union for each line
		return float(inter)/float(union+inter)

 
class CompareSets:
	def __init__(self, hash1, hash2):
		self.set1=hash1
		self.set2=hash2

	def jaccard(self):
		''' Return the Jaccard similarity of 2 sets of of hash values
		'''
		inter=self.set1.intersection(self.set2)
		union=self.set1.union(self.set2)
		return len(inter)/float(len(union))


###########################################################
#                   Function definition
###########################################################

 				

###########################################################
#                      MAIN
###########################################################



# Shingling of documents
shigling_size=9
doc1='Data/Part1/awards_1990/awd_1990_00/a9000255.txt'
#doc1='a.txt'
G=Shingling(doc1, shigling_size)
G.shingle()

doc2='Data/Part1/awards_1990/awd_1990_00/a9000256.txt'
#doc2='b.txt'
H=Shingling(doc2, shigling_size)
H.shingle()

doc3='Data/Part1/awards_1990/awd_1990_02/a9002020.txt'
#doc3='c.txt'
I=Shingling(doc3,shigling_size)
I.shingle()

doc4='Data/Part1/awards_1990/awd_1990_02/a9002147.txt'
#doc4='c.txt'
J=Shingling(doc4,shigling_size)
J.shingle()


# Jaccard similarity of two of them
intersec=CompareSets(G.hashed_values, H.hashed_values)
js=intersec.jaccard()
print 'Jaccard similarity:', js



# minHashing 
minH=MinHashing([G.hashed_values, H.hashed_values, I.hashed_values, J.hashed_values], 10000)
#print minH.key
#random.seed(5)
minH.signMatrix()
#print minH.signM
print 'Similarity of signatures:', minH.compareSignatures(minH.signM[:,0], minH.signM[:,1])

