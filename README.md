# algofun
Fun with algorithms!

Projects in this repo:

1. bloku
   BlockuDoku game initial implementation
   
2. bucket
   You are given a number of buckets of various capacity, with initial amount of water in them. 
   You are asked to measure a certain amount of water, by transfering water among these buckets.
   recket.py i

3. fastbloku
   BlockuDoku solver. There are several players implemented:
    - Human player: uses console input to get the moves
    - Random player: uses random nubmer generator to pick moves
    - Rule player: uses simple rule based system
    - Brute player: exhaustive search of possible moves
    - Smart player: uses a configurable sample size to randomly pick a subset of moves at each level from all possible moves
    - LR player: Logistic regression player. Uses ML model trained using many calculated board state values.
    - Smart LR player: Uses LR, but limits the searches at each level.
    
4. poker
   Poker hand rank computation.
