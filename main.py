###########################################################
#                  Data Mining KTH
#         Homework 1: Finding similar items 
###########################################################


import numpy as np
import copy as cp
import random
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
		self.hashed_values=list()

	def shingle(self):
		global shingle_dictionary
		global hash_dictionary
		fi=open(self.file, 'r')
		text=str()
		for line in fi:
			text=text+line # layout of the document taken in count
		for i in xrange(len(text)):
			if i+self.k>len(text):
				break # avoid to create shingle under secified size
			if text[i:i+self.k] not in shingle_dictionary.keys():
				# Creates an entry in dictionnaries for new shingle
				shingle_dictionary[text[i:i+self.k]]=len(shingle_dictionary)+1
				hash_dictionary[shingle_dictionary[text[i:i+self.k]]]=text[i:i+self.k]
			self.hashed_values.append(shingle_dictionary[text[i:i+self.k]]) # at the ith case of self.hashed_value there is the hash value associated to the ith shingle
		fi.close()


class MinHashing:
	def __init__(self, sets, n=10): 
		self.sets=sets # sets are under hashed value forms, given as a list
		self.nPermutations=n 
		self.key=(hash_dictionary.keys()) # tuple --> always work with the same list of keys
		self.M=self.characteristic_matrix()
		self.signM=None

	def characteristic_matrix(self):
		''' Creates the characteristic matrix of sets, only returns the positions where there is 1.   M(# shnigles, # sets); we count row per row (i.e: index k means where at the k//i row and k%i column) 
		''' 
		#M2=np.zeros((len(self.key), len(self.sets))) # if we want to see the sparse matrix
		M=list()		
		for i in xrange(len(self.key)):
			for j in xrange(len(self.sets)):
				k=0
				while k <len(self.sets[j]) and self.sets[j][k]!=self.key[i]:
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

	def minhash(self):
		''' For one permutation, return the associated row in the signature matrix
		'''
		p=self.permutations()
		rowSign=np.zeros(len(self.sets), dtype=int)
		for j in xrange(len(self.sets)):
			for i in xrange(len(p)):
				if (p[i]-1)*len(self.sets)+j in self.M: # -1 because index in M and keys are not synchronized
					rowSign[j]=i+1 # Position in sign matrix starts to one (like in the slides)
					break					
		return np.transpose(rowSign) # returns row of signature matrix

	def signMatrix(self):
		self.signM=np.zeros((self.nPermutations, len(self.sets)))
		for n in xrange(self.nPermutations):
			self.signM[n,:]=self.minhash()

	def compareSignatures(self, sign1, sign2):
		inter=0
		for i in xrange(len(sign1)):
			if sign1[i]==sign2[i]:
				inter+=1
		return inter/float(len(sign1))

 
class CompareSets:
	def __init__(self, hash1, hash2):
		self.set1=hash1
		self.set2=hash2

	def jaccard(self):
		''' Return the Jaccard similarity of 2 sets of of hash values
		'''
		inter=np.intersect1d(self.set1, self.set2)
		union=set(self.set1+self.set2)
		return len(inter)/float(len(union))


###########################################################
#                   Function definition
###########################################################

 				

###########################################################
#                      MAIN
###########################################################

# Global dictionaries used to stock shingles and hash values, 
shingle_dictionary={} # key = shingle, value = hash value; one unical value for one key
hash_dictionary={} # key = hash value, value = shingle; one unical value for one key


# Shingling of documents
shigling_size=9
doc1='Data/Part1/awards_1990/awd_1990_00/a9000006.txt'
#doc1='a.txt'
G=Shingling(doc1, shigling_size)
G.shingle()

doc2='Data/Part1/awards_1990/awd_1990_00/a9000031.txt'
#doc2='b.txt'
H=Shingling(doc2, shigling_size)
H.shingle()
doc3='Data/Part1/awards_1990/awd_1990_02/a9002020.txt'
#doc3='c.txt'
I=Shingling(doc3,shigling_size)
I.shingle()

doc4='Data/Part1/awards_1990/awd_1990_02/a9002147.txt'
#doc3='c.txt'
J=Shingling(doc4,shigling_size)
J.shingle()


# Jaccard similarity of two of them
intersec=CompareSets(G.hashed_values, H.hashed_values)
js=intersec.jaccard()
print 'Jaccard similarity:', js



# minHashing 
minH=MinHashing([G.hashed_values, H.hashed_values, I.hashed_values, J.hashed_values], 100)
#random.seed(5)
minH.signMatrix()
#print '\n', minH.signM
print minH.compareSignatures(minH.signM[:,1], minH.signM[:,2])

