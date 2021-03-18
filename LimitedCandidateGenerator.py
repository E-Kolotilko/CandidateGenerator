
class LimitedCandidateGenerator():
    """Generate next string based on vocabulary from some_state to other_state or till all_last_chars state """

    def __init__(self, vocabulary, init_state, end_state=None, rincrement=True):
        """ Init indexes based on init_state string and vocabulary list
        
        Arguments:
        vocabulary - list of possible characters
        init_state - string with state from which to start counting
        end_state - optional stop-state string. Inclusive. Default=None -> last chars from vocabulary.  
            raises ValueError if is "less" than init_state
        rincrement - optional increment direction bool. True-> aaa, aab, aac,... False-> aaa, baa, caa,... 
        """
        self._vocabulary_=vocabulary
        self._vocab_length_ = len(vocabulary)
        self._init_state_=init_state
        self._rincrement_=rincrement
        self._indexes_=[]
        self._end_indexes_=[]
        self.set_start_state(init_state)
        if not end_state:
            end_state = ''.join([vocabulary[-1] for i in range(len(init_state))])
        if len(init_state) != len(end_state):
            raise Exception('Only same length states are supported')
        self.set_end_state(end_state)
        self._check_states_()
        #if any(map(lambda x,y : x>y, self._indexes_, self._end_indexes_)):
            #end_state = ''.join([vocabulary[-1] for i in range(len(init_state))])
            #self.set_end_state(end_state)

    def _check_states_(self):
        """ Raise ValueError exception if 'end is less than start' """
        if any(map(lambda x,y : x>y, self._indexes_, self._end_indexes_)):
            raise ValueError('init_state is "after" end')

    def set_start_state(self, new_state):
        """Reset indexes based on new_state string and existing vocabulary, check new state (can raise ValueError)"""
        self._indexes_.clear()
        for char in new_state:
            self._indexes_.append(self._vocabulary_.index(char))
        
        self._check_states_()


    def set_end_state(self, end_state):
        """Reset end indexes based on end_state string and existing vocabulary, check new state (can raise ValueError)"""
        self._end_indexes_.clear()
        for char in end_state:
            self._end_indexes_.append(self._vocabulary_.index(char))
        self._check_states_()


    def generate(self):
        """Increment and then return current state or None if end was reached (increment was impossible)"""
        if self._increment_():
            state = [self._vocabulary_[x] for x in self._indexes_]
            return ''.join(state)
        else:
            return None


    def _increment_(self):
        """Try to increment. Return True if was possible else False"""
        if self._indexes_ == self._end_indexes_:
            return False
        if (self._rincrement_):
            self._indexes_[-1]+=1
            for i in range(len(self._indexes_)-1,0,-1):
                if self._indexes_[i]>=self._vocab_length_:
                    self._indexes_[i]=0
                    self._indexes_[i-1]+=1
                else:
                    break
        else:
            self._indexes_[0]+=1
            for i in range(len(self._indexes_)-1):
                if self._indexes_[i]>=self._vocab_length_:
                    self._indexes_[i]=0
                    self._indexes_[i+1]+=1
                else:
                    break
        return True

if __name__=="__main__":
    symbols = [*range(48, 58), *range(65, 91), *range(97, 123)]
    symbols = [chr(x) for x in symbols]
    #with well-behaving defined limits, right increment
    print('Right')
    name = 'aaa'
    last_name='aad'
    generator = LimitedCandidateGenerator(symbols, name, last_name, rincrement=True)
    while (name):
        print(name)
        name=generator.generate()
    #
    #with well-behaving defined limits, left increment
    print('Left')
    name = 'aaa'
    last_name='daa'
    generator = LimitedCandidateGenerator(symbols, name, last_name, rincrement=False)
    while (name):
        print(name)
        name=generator.generate()
    #
    #end is not defined
    print('Left, no last')
    name = symbols[-3]+symbols[-1]*2
    generator = LimitedCandidateGenerator(symbols, name, rincrement=False)
    while (name):
        print(name)
        name=generator.generate()
    #end is before start
    print('end before start')
    try:
        name = symbols[-3]+symbols[-1]*2
        last_name = symbols[-3]*3
        generator = LimitedCandidateGenerator(symbols, name, last_name, rincrement=False)
        print('Expected exception, but it was not raised!')
    except ValueError as value_error:
        print('ValueError caught as expected: '+str(value_error))
    except Exception as unexpected_error:
        print('Unexpected exception caught:'+str(unexpected_error))
    print('Done')
