import gensim
import re


try:
    model = gensim.models.KeyedVectors.load_word2vec_format('tempvectors.bin', binary=True)  ## you need some vectors for this to work
except:
    import boto3
    s3 = boto3.resource('s3')
    KEY = "shrunkenvectors_200000.bin"  ## too big for github so on s3
    BUCKET_NAME="lang-models"
    s3.Bucket(BUCKET_NAME).download_file(KEY, 'tempvectors.bin')
    model = gensim.models.KeyedVectors.load_word2vec_format('tempvectors.bin', binary=True)

    
class SimTester:
    

    def __init__(self):
        self.used_sents = []
        self.threshold = .8
        
    def custom_tokenize(self,astring):
        ## periods
        period_regex = re.compile(r'(?<![!Mr|Mrs|St|Ma|])\.')
        astring = re.sub(period_regex," .",astring)
        
        ## others
        for i in ',!?':
            astring = astring.replace(i," "+i)
            
        return astring
      
    def sim_score(self,s1,s2):
        s1_tok = self.custom_tokenize(s1)
        s2_tok = self.custom_tokenize(s2)
        return model.wmdistance(s1_tok,s2_tok)


if __name__ == "__main__":
    s = SimTester()
    print(s.sim_score("I am a frog.","I will be a lizard."))