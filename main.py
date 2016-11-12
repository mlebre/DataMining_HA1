import numpy as np
import copy as cp

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
		self.hashed_values=[]

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


class minHashing:
	def __init__(self, sets, n=10): 
		self.sets=sets # sets are under hashed value forms, given as a list
		self.nPermutations=n 
		self.key=(hash_dictionary.keys()) # tuple --> always work with the same list of keys
		self.M=self.characteristic_matrix()

	def characteristic_matrix(self):
		''' Creates the characteristic matrix of sets, only returns the positions where there is 1.   M(# shnigles, # sets); we count row per row (i.e: index k means where at the k//i row and k%i column) 
		''' 
		M=np.zeros((len(self.key), len(self.sets)))
		print 'len key', len(self.key)
		print hash_dictionary
		for i in xrange(len(self.key)):
			for j in xrange(len(self.sets)):
				k=0
				while k <len(self.sets[j]) and self.sets[j][k]!=self.key[i]:
					k+=1
				if k<len(self.sets[j]):
					M[i,j]=1
		return M

#	def permutations(self):
#		permute=cp.deepcopy()






###########################################################
#                   Function definition
###########################################################

def compareSets(hash1, hash2):
	''' Return the Jaccard similarity of 2 sets of of hash values
	'''
	inter=np.intersect1d(hash1, hash2)
	union=set(hash1+hash2)
	#print union
	return len(inter)/float(len(union))


 				

###########################################################
#                           MAIN
###########################################################

# Global dictionaries used to stock shingles and hash values, 
shingle_dictionary={} # key = shingle, value = hash value; one unical value for one key
hash_dictionary={} # key = hash value, value = shingle; one unical value for one key


shigling_size=1
#doc1='Data/Part1/awards_1990/awd_1990_00/a9000006.txt'
doc1='a.txt'
G=Shingling(doc1, shigling_size)
G.shingle()

#doc2='Data/Part1/awards_1990/awd_1990_00/a9000031.txt'
doc2='b.txt'
H=Shingling(doc2, shigling_size)
H.shingle()

doc3='c.txt'
I=Shingling(doc3,shigling_size)
I.shingle()


intersec=compareSets(I.hashed_values, H.hashed_values)
print 'Jaccard similarity:', intersec

# minHashing class test
minH=minHashing([G.hashed_values, I.hashed_values, H.hashed_values], 10)
print minH.M[:0]==minH.M[:1]
print minH.M



