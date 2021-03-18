
class CandidateGenerator():
    """Generate string based on vocabulary from some_state to all_last_chars state """
    
    def __init__(self, vocabulary, init_state):
        """ Init indexes based on init_state string and vocabulary list"""
        self._vocabulary_=vocabulary
        self._vocab_length_ = len(vocabulary)
        self._init_state_=init_state
        self._indexes_=[]
        self.set_state(init_state)

    def set_state(self, new_state):
        """Reset indexes based on new_state string and existing vocabulary"""
        self._indexes_.clear()
        for char in new_state:
            self._indexes_.append(self._vocabulary_.index(char))

    def get_state(self):
        state = [self._vocabulary_[x] for x in self._indexes_]
        return ''.join(state)

    def generate(self):
        """Increment and then return current state or None if end was reached"""
        if self._increment_():
            state = [self._vocabulary_[x] for x in self._indexes_]
            return ''.join(state)
        else:
            return None
        
    def _increment_(self):
        """Try to increment. Return True if possible else False"""
        if self._indexes_[-1]>=self._vocab_length_:
            return False
        self._indexes_[0]+=1
        for i in range(len(self._indexes_)-1):
            if self._indexes_[i]>=self._vocab_length_:
                self._indexes_[i]=0
                self._indexes_[i+1]+=1
            else:
                break
        return self._indexes_[-1]<self._vocab_length_


if __name__=="__main__":
    symbols = [*range(48, 58), *range(65, 91), *range(97, 123)]
    symbols = [chr(x) for x in symbols]
    name = symbols[-3]+symbols[-1]*4
    #name = symbols[-3]*3
    generator = CandidateGenerator(symbols,name)
    while (name):
        print(name)
        name=generator.generate()
    print('Done')
