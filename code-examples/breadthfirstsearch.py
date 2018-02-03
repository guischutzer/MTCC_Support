 1 def breadthFirstSearch(self, startState):
 2     q = queue.Queue()
 3     q.put(startState)
 4     maxReward = -200
 5     actionPath = []

 6     while not q.empty():
 7         state = q.get()
 
 8         if state.isTerminal():
 9             reward = state.getReward()
10             if reward >= maxReward:
11                 maxReward = reward
12                 actionPath = state.getPath()

13         else:
14             for s in self.getChildren(state):
15             q.put(s)

16     return actionPath
