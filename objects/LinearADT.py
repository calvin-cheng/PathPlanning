class PriorityQueue:
    # Children = 2 * n, (2 * n) + 1
    # Parent = n // 2
    def __init__(self, items, priorities):
        self.items = [0] + items
        self.priorities = [0] + priorities
        self.len = len(items)
        
        self.heapify()

    def enqueue(self, item, priority):
        self.items.append(item)
        self.priorities.append(priority)
        self.len += 1
        self.percUp(self.len)

    def dequeue(self):
        if self.len > 1:
            res = self.items[1]
            self.len -= 1
            self.items[1] = self.items.pop()
            self.priorities[1] = self.priorities.pop()
            self.percDown(1)
            return res
        elif self.len == 1:
            self.len -= 1
            self.priorities.pop()
            return self.items.pop() 
        else:
            print('Priority Queue already empty!')
            return None

    def percUp(self, i):
        while i//2 > 0:
            if self.priorities[i//2] > self.priorities[i]:
                self.swap(i, i//2)
            i //= 2

    def percDown(self, i):
        while 2*i <= self.len:
            if 2*i+1 > self.len:
                # No sibling exists
                maxChildIdx = 2*i
            else:
                # Compare siblings
                if self.priorities[2*i] < self.priorities[2*i+1]:
                    maxChildIdx = 2*i
                else:
                    maxChildIdx = 2*i+1
            if self.priorities[maxChildIdx] < self.priorities[i]:
                self.swap(maxChildIdx, i)
            i = maxChildIdx
    
    def setPriority(self, item, priority):
        i = self.items.index(item)
        self.priorities[i] = priority
        self.heapify()
    
    def heapify(self):
        for i in range(self.len, 0, -1):
            self.percDown(i)

    def swap(self, i, j):
        self.priorities[i], self.priorities[j] = self.priorities[j], self.priorities[i]
        self.items[i], self.items[j] = self.items[j], self.items[i]

    def isEmpty(self):
        return self.len == 0

