
import pickle
loaded_model = pickle.load(open('maxent_model_whitman_vs_not.pkl', 'rb'))

import json
with open('top_words.json','r') as f:
    top_words = json.load(f)

from nltk import tokenize,ngrams

class AuthorTest:
    
    def __init__(self):
        self.goal = "whit"
        self.model = loaded_model
        self.top_words = top_words

    def isword(self,astring):
        if any(c.isalpha() for c in astring):
            return True
        return False

    def word_feats(self,words):
        words = [w.lower() for w in tokenize.word_tokenize(words)]
        words = [w for w in words if self.isword(w)]
        words_pop = [w for w in words if w in self.top_words]
        for i in range(len(words)):
            if words[i] not in words_pop:
                words[i]="<UNK>"
        words = ["<BEG>"]+ words + ["<END>"]
        bigrams = [str(i) for i in ngrams(words,2)]
        trigrams = [str(i) for i in ngrams(words,3)]
        allfeatures = words_pop+bigrams+trigrams
        allfeatures = words_pop+bigrams
        return dict([(word, True) for word in allfeatures])
       
    def author_test(self,sentence):
        features = self.word_feats(sentence)
        prediction = self.model.prob_classify(features)
        return prediction.prob('whit')

       
if __name__ == "__main__":
    at = AuthorTest()
    print(at.author_test("I am a pug."))