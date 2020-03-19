'''
class bucket:

    def __init__(size, amount):
        self.size = size
        self.amount = amount

    def get_size(self):
        return self.size

    def get_amount(self):
        return self.amount

    def add_amount(self, a):
        self.amount = min(self.amount + a, self.size)

    def get_capacity(self):
        return max(0, self.size - self.amount)
   
    # pour the contents into the bucket passed in
    def pour(self, into):
        if (into != self):
            cap = into.get_capacity()
            amt = min(cap, self.amount)
            self.amount -= amt
            into.add_amount(amt)
'''


class puzzle:

    memoize = { }
    current_states = [ ]
    next_states = [ ] 
   
    def __init__(self):
        self.bucket_sizes = [10, 6, 8]
        self.current_state = [7, 3, 5]
        self.stmap.add(self.current_state)
        self.nbuckets = self.current_state.size()
        self.target_bucket = 0
        self.target_amount = 5
        self.memoize[tuple(self.current_state)] = [ ]
        self.current_states.append(self.current_state)
        
    def add_amount(b, a):
        b[1] = min(b[1] + a, b[0])

    def get_capacity(b):
        return max(0, b[0] - b[1])
   
    # pour the contents into the bucket passed in
    def pour(b, into):
        if (into != b):
            cap = get_capacity(into)
            amt = min(cap, b[1])
            b[1] -= amt
            add_amount(into, amt)
            
    def solved(self):
        return self.current_state[self.target_bucket][1] == self.target_amount

    
    def solve(self):
        traverse(
        for b1 in range(self.nbuckets):
            for b2 in range(self.nbuckets):
                if (b1 == b2):
                    continue

                new_state = self.current_state.copy()
                pour(new_state[b1], new_state[b2])
                if new_state in self.memoize:
                    continue

                memoize.append(new_state)
        
                
