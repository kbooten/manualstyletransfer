import gensim
import re
from nltk import tokenize


try:
    custom_vectors = "/Users/kyle/Desktop/GoogleNews-vectors-negative300.bin" ## include custom vectors (large, not for web)
    model = gensim.models.KeyedVectors.load_word2vec_format(custom_vectors, binary=True)
    try:
        model = gensim.models.KeyedVectors.load_word2vec_format('tempvectors.bin', binary=True)  ## you need some vectors for this to work
    except:
        import boto3
        s3 = boto3.resource('s3')
        KEY = "shrunkenvectors_200000.bin"  ## too big for github so on s3
        BUCKET_NAME="lang-models"
        s3.Bucket(BUCKET_NAME).download_file(KEY, 'tempvectors.bin')
        model = gensim.models.KeyedVectors.load_word2vec_format('tempvectors.bin', binary=True)
except:
    pass

    
class SimTester:
    

    def __init__(self):
        self.used_sents = []
        
    def custom_tokenize(self,astring):
        return [w.lower() for w in tokenize.casual_tokenize(astring) if w not in ",!?.-;:"]
      
    def sim_score(self,s1,s2):
        s1_tok = self.custom_tokenize(s1)
        s2_tok = self.custom_tokenize(s2)
        return model.wmdistance(s1_tok,s2_tok)


if __name__ == "__main__":
    s = SimTester()
    print(s.sim_score("I am a frog.","I will be a lizard."))
