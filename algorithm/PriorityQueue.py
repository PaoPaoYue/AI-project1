"""
A development class to improve efficiency in A* searching or maybe in the future
"""
class IndexQueue:
    def __init__(self):
        self.pq = [None]
        self.qp = {}
        self.vals = {}
        self.n = 0

    def empty(self):
        return self.n == 0

    def contain(self, key):
        return key in self.vals

    def get(self, key):
        return self.vals[key]

    def push(self, key, value):
        if (not key in self.vals):
            self.n += 1
            self.vals[key] = value
            self.qp[key] = self.n
            self.pq.append(key)
            self.__swim(self.n)
        

    def pop(self):
        res = None
        if self.pq:
            key = self.pq[1]
            res = self.vals[key]
            self.__swap(1, self.n)
            self.pq.pop()
            self.qp.pop(key)
            self.vals.pop(key)
            self.n -= 1
            self.__sink(1)
        return res

    def change(self, key, value):
        if key in self.vals:
            self.vals[key] = value
            self.__swim(self.qp[key])
            self.__sink(self.qp[key])

    def delete(self, key):
        if key in self.vals:
            tmp = self.qp[key]
            self.__swap(tmp, self.n)
            self.pq.pop()
            self.qp.pop(key)
            self.vals.pop(key)
            self.n -= 1
            self.__swim(self.qp[key])
            self.__sink(self.qp[key])

    def __swim(self, index):
        while index > 1 and self.__gt(index//2, index):
            self.__swap(index//2, index)
            index = index//2

    def __sink(self, index):
        while (2*index <= self.n):
            child = 2*index
            if child < self.n and self.__gt(child, child+1):
                child += 1
            if not self.__gt(index, child):
                break
            self.__swap(index, child)
            index = child

    def __swap(self, a, b):
        a_tmp = self.pq[a]
        b_tmp = self.pq[b]
        self.pq[b] = a_tmp
        self.pq[a] = b_tmp
        self.qp[a_tmp] = b
        self.qp[b_tmp] = a

    def __gt(self, a, b):
        return self.vals[self.pq[a]] > self.vals[self.pq[b]]
        

