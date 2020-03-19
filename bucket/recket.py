
def add_amount(cs, b, a):
    b[1] = min(b[1] + a, b[0])


def get_capacity(cs, b):
    return max(0, bucket_sizes[b] - cs[b])


# pour the contents into the bucket passed in
def pour(cs, b_from, b_into):
    if (b_into != b_from):
        cap = get_capacity(cs, b_into)
        amt = min(cap, cs[b_from])
        cs[b_from] -= amt
        cs[b_into] += amt

        
def transition(cs, move):
    ns = cs.copy()
    pour(ns, move[0], move[1])
    return ns

        
def solved(s):
    return s[target_bucket] == target_amount


def solve(cs, nmoves):
    
    if (len(cs)==0):
        # print("EMPTY LIST OF STATES, NO SOLUTION FOUND!")
        return []
    
    nslist = []
    
    for st in cs:
        path = memoize[tuple(st)] # shortest path so far to this
        
        for b1 in range(nbuckets):
            for b2 in range(nbuckets):
                if (b1 == b2):
                    continue

                move = [b1, b2]
                ns = transition(st, move)

                if tuple(ns) in memoize:
                    # print("Already been here: %s\nprev path=%s" % (ns, memoize[tuple(ns)]))
                    continue

                #found new state
                # print("New state: %s" % ns)
                # print("Path=%s  move=%s"%(path, move))
                np = path.copy()
                np.append(move)
                memoize[tuple(ns)] = np
                # print("Memoized state=%s path=%s new path=%s"%(tuple(ns), path, np))
                nslist.append(ns)

                if solved(ns):
                    # print("SOLVED! In %s steps" % (nmoves+1))
                    return np
                    
    return solve(nslist, nmoves+1)


def question_generator():

    global bucket_sizes 
    global current_state
    global nbuckets
    global target_bucket
    global target_amount
    global memoize


    bucket_sizes = [25, 18, 9, 31, 17]
    current_state = [11, 16, 8, 20, 13]
    nbuckets = len(bucket_sizes)

    for tb in range(nbuckets):
        for ta in range(bucket_sizes[tb]+1):
            target_bucket = tb
            target_amount = ta
            memoize = { }
            next_states = [ ]
            
            memoize[tuple(current_state)] = [ ]
            solution = solve([current_state], 0)

            cs = current_state

            if len(solution) > 3:           
                print("[%s] ==> Target: In bucket %s leave %s units of water"%(len(solution),\
                            target_bucket, target_amount))


def solver(tb, ta):
    global bucket_sizes 
    global current_state
    global nbuckets
    global memoize
    global target_bucket
    global target_amount
    
    bucket_sizes = [25, 18, 9, 31, 17]
    current_state = [11, 16, 8, 20, 13]
    nbuckets = len(bucket_sizes)
    target_bucket = tb
    target_amount = ta
    memoize = {}
    
    print("Bucket sizes:%s"%bucket_sizes)
    print("Initial amount of water in each bucket:%s"%current_state)
    print("Target: In bucket %s leave %s units of water"%(target_bucket, target_amount))
    print("-------------------")

    memoize[tuple(current_state)] = [ ]
    solution = solve([current_state], 0)

    cs = current_state

    if len(solution) == 0:
        print("No solution found! :(")
    else:
        print("Solution found. Moves:")
        for m in solution:
            ns = transition(cs, m)
            print("%s ==> %s ==> %s"%(cs, m, ns))
            cs = ns

def main():
    # question_generator()
    solver(0, 3)
    solver(2, 1)
    solver(3, 8)


bucket_sizes = []
current_state = []
nbuckets = 0
target_bucket = 0
target_amount = 0
memoize = {}
main()    
