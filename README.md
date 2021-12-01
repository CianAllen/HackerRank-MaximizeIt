# HackerRank-MaximizeIt
My submission to HackerRank's "MaximizeThis!" practice problem. Evolutionary algorithm implemented in order to find most optimal solution.

Problem description:

You are given a function F(X) = square(X). You are also given k lists. The i list consists of N elements.

You have to pick one element from each list so that the value from the equation below is maximized:
S = (f(X) + f(x2).... + f(xi)) % M

M is described in the first line of the input file and
K is the number of lists in the file

% denotes the modulo operator.

Note that you need to take exactly one element from each list, not necessarily the largest element. You add the squares of the chosen elements and perform the modulo operation. The maximum value that you can obtain, will be the answer to the problem.

Output Format
Output a single integer denoting the value

Ex:
3 1000\n
2 5 4\n
3 7 8 9\n
5 5 7 8 9 10\n

First line: 3 = number of lists in K, 1000 = M
second line to final line: first elem = number of elements in list, rest of line = list for that line

Output for ex: 206 = (F(5) + F(9) + F(10)) % 1000
