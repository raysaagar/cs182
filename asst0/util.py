##### Filename: util.py
##### Author: Saagar Deshpande
##### Date: 9/8/2013
##### Email: sdeshpande@college.harvard.edu

import copy
from collections import deque

## Problem 1

def matrix_multiply(x, y):

    if (len(x) != len(y)):
        return None
    if (len(x) != len(x[0])):
        return None

    # set up the answer matrix
    ans = [[ ], [ ]]
    
    for i in range(0,2):
        for j in range(0,2):
            sum = 0;
            # do the matrix multiply for each element in the answer
            for k in range(0,2):
                sum = sum + (x[i][k]*y[k][j])
            # push the sum we found. push 2 sums to each list.
            ans[i].append(sum)
    return ans


## Problem 2, 3

class MyQueue:
    def __init__(self):
        # create a new deque object
        self.data = deque('')
    def push(self, val):
        # append to the right
        self.data.append(val)
    def pop(self):
        # since we push data to the right, we pop from the left
        try: 
            x = self.data.popleft()
            return x
        except IndexError:
            # return None if we can't pop any more items
            return None
    def __eq__(self, other):

        # check if both objects are queues
        if isinstance(self, MyQueue) != isinstance(other, MyQueue):
            return False

        # convert to lists so we can do an item by item comparison
        a = list(self.data)
        b = list(other.data)

        # if the lengths are not equal, not equal
        if (len(a) != len(b)):
            return False

        # compare items, return false if two aren't equal
        for itemA, itemB in zip(a, b):
            if itemA != itemB:
                return False

        return True

    def __ne__(self, other):
        # the same as __eq__, but return the opposite boolean value for each case

        if isinstance(self, MyQueue) != isinstance(other, MyQueue):
            return True

        a = list(self.data)
        b = list(other.data)

        if (len(a) != len(b)):
            return True

        for itemA, itemB in zip(a, b):
            if itemA != itemB:
                return True

        return False

    def __str__(self):
        # print each item to string form one by one
        a = list(self.data)
        
        if len(a) == 0:
            return "<empty queue>"

        s = "top | "

        for itemA in a:
            s = s + str(itemA) + " "

        return s + "| bottom"

class MyStack:
    def __init__(self):
        # new deque object
        self.data = deque('')
    def push(self, val):
        # append to right
        self.data.append(val)
    def pop(self):
        # pop off right because we appended to the right
        try: 
            x = self.data.pop()
            return x
        except IndexError:
            return None
    def __eq__(self, other):
        # same as queue version

        if isinstance(self, MyStack) != isinstance(other, MyStack):
            return False

        a = list(self.data)
        b = list(other.data)

        if (len(a) != len(b)):
            return False

        for itemA, itemB in zip(a, b):
            if itemA != itemB:
                return False

        return True
    def __ne__(self, other):
        # same as queue version

        if isinstance(self, MyStack) != isinstance(other, MyStack):
            return True

        a = list(self.data)
        b = list(other.data)

        if (len(a) != len(b)):
            return True

        for itemA, itemB in zip(a, b):
            if itemA != itemB:
                return True

        return False

    def __str__(self):
        # reverse the list so we can have some notion of top->bottom as left->right
        a = list(reversed(self.data))
        
        if len(a) == 0:
            return "<empty stack>"

        s = "top | "

        for itemA in a:
            s = s + str(itemA) + " "

        return s + "| bottom"

## Problem 4

def add_position_iter(lst, number_from=0):
    # lists are mutable, so need a separate copy
    new_lst = list(lst)
    # simple add of position and number_from
    for i in range(0, len(new_lst)):
        new_lst[i] += i + number_from
    return new_lst

def add_position_recur(lst, number_from=0):
    # lists are mutable, so need a separate copy
    new_lst = list(lst)
    # call a helper function
    return add_position_recur_helper(new_lst, number_from, 0)

def add_position_recur_helper(lst, number_from, pos):
    # if position hits end of list, return the list
    if (pos >= len(lst)):
        return lst
    else:
        # update the sum
        lst[pos] = lst[pos] + pos + number_from
        # call recursive helper, add 1 to position because we are moving down the list
        add_position_recur_helper(lst, number_from, pos+1)
    return lst

def add_position_map(lst, number_from=0):
    new_lst = list(lst)

    # create a list of number_from values for the map
    nf_lst = [number_from]*len(lst)

    # lambda does the sum, pass in the list, a range, and the nf_list for mapping
    new_lst = map(lambda x, p, nf: x + p + nf, new_lst, range(0, len(lst)), nf_lst)
    return new_lst

## Problem 5

def remove_course(roster, student, course):
    # find the set in the dict, use set.remove function
    roster[student].remove(course)
    return roster

def deep_copy(roster):
    # deep copy the roster
    # create a new dict
    new_roster = {}
    # for each item in the old dict, copy the set into the new dict.
    for student in roster:
        new_roster[student] = roster[student].copy()
    # set was copied with shallow copy, which is reasonable because the set is simple
    return new_roster

def copy_remove_course(roster, student, course):
    #tmp_roster = deep_copy(roster)
    # could use the copy library instead...
    tmp_roster = copy.deepcopy(roster)
    return remove_course(tmp_roster,student,course)

def main():
    #  tests for matrix mulitply
    print matrix_multiply([[1, 2], [3, 4]], [[4, 3], [2, 1]])
    print matrix_multiply([[4, 5], [6, 7]], [[1, 3], [9, 7]])

    # tests for Queue
    q = MyQueue()
    q2 = MyQueue()
    q.push(1); q.push(2); q.push(3);
    
    q2.push(1)

    print q.__eq__(q2) # FALSE
    print q.__eq__(q)  # TRUE
    
    print q.__ne__(q2) # TRUE
    print q.__ne__(q)  # FALSE

    print q.__str__()

    # should return 1, 2, 3 
    for i in range(0,3):
        print q.pop()

    print q.__str__() # nothing left in queue

    # tests for Stack 
    s = MyStack()
    s2 = MyStack()
    
    s.push(1); s.push(2); s.push(3);
    
    s2.push(1)
    
    print s.__eq__(s2) # FALSE
    print s.__eq__(s)  # TRUE
    
    print s.__ne__(s2) # TRUE
    print s.__ne__(s)  # FALSE
    
    print s.__str__()

    # should return 3, 2, 1
    for i in range(0,3):
        print s.pop()

    print s.__str__() # nothing left in stack

    print q2.__eq__(s2) # FALSE
    print s2.__ne__(q2) # TRUE

    # test the add_position_iter
    a = [7,5,1,4]
    b = [0,0,3,1]
    print a
    print b

    print add_position_iter(a)
    print add_position_recur(a)
    print add_position_map(a)

    print add_position_iter(b, 3)
    print add_position_recur(b, 3)
    print add_position_map(b, 3)

    # should be the same as above!
    print a
    print b

    # testing remove_course
    roster = {'kyu': set(['cs182']), 'david': set(['cs182'])}
    print roster
    print remove_course(roster, 'kyu','cs182')
    print roster # the remove was destructive

    roster2 = {'kyu': set(['cs182']), 'david': set(['cs182'])}
    print roster2
    roster2_changed = copy_remove_course(roster2, 'kyu','cs182')
    print roster2 # the remove was not destructive because of the copy
    print roster2_changed

if __name__ == "__main__":
    main()