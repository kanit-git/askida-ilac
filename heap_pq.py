import heapq
import time

class PriorityQueue:
    def __init__(self):
        self._heap = []

    def push(self, request):
        # priority kullanıyoruz
        heapq.heappush(self._heap, (-request["priority"], time.time(), request))

    def pop(self):
        if not self._heap:
            return None
        return heapq.heappop(self._heap)[2]

    def peek(self):
        if not self._heap:
            return None
        return self._heap[0][2]

    def __len__(self):
        return len(self._heap)

    def is_empty(self):
        return len(self._heap) == 0
