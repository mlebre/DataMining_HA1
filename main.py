import numpy as np

###########################################################
#                       Class definition
###########################################################
class Shingling:

	def __init__(self, doc, size=5):
		''' Construct shingles of length size (default value 5) 
		    from the document name given
		'''
		self.k=size
		self.file=doc 
		self.hashed_values=[]

	def shingle(self):
		global shingle_dictionary
		global hash_dictionary
		fi=open(self.file, 'r')
		text=str()
		for line in fi:
			text=text+line
		for i in xrange(len(text)):
			if i+self.k>len(text):
				break # avoid to create shingle under secified size
			if text[i:i+self.k] not in shingle_dictionary.keys():
				shingle_dictionary[text[i:i+self.k]]=len(shingle_dictionary)+1
				hash_dictionary[shingle_dictionary[text[i:i+self.k]]]=text[i:i+self.k]
			if shingle_dictionary[text[i:i+self.k]] not in self.hashed_values:
				# Don't care about repetition of a shingle? 
				self.hashed_values.append(shingle_dictionary[text[i:i+self.k]])
		fi.close()

def compareSets(hash1, hash2):
	''' Return the Jaccard similarity of 2 sets of of hash values
	'''
	inter=np.intersect1d(hash1, hash2)
	union=set(hash1 +hash2)
	return len(inter)/float(len(union))


 				

###########################################################
#                           MAIN
###########################################################

# Global dictionaries used to stock shingles and hash values, 
shingle_dictionary={} # key = shingle, value = hash value; one unical value for one key
hash_dictionary={} # key = hash value, value = shingle; one unical value for one key


shigling_size=9
doc1='Data/Part1/awards_1990/awd_1990_00/a9000006.txt'
#doc1='a.txt'
G=Shingling(doc1, shigling_size)
G.shingle()
doc2='Data/Part1/awards_1990/awd_1990_00/a9000031.txt'
#doc2='b.txt'
H=Shingling(doc2, shigling_size)
H.shingle()
print len(hash_dictionary)
#print len(hash_dictionary[1])
#print shingle_dictionary['Title    ']

intersec=compareSets(G.hashed_values, H.hashed_values)
print intersec


