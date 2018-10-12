# Search.py coded by Sean Murren, February 2015

import sys
from collections import deque


class Node(object):
	# Node class contains id and weight info (total cost to reach node).
	# It also stores who it's parent node is when it is added to frontier
	# Contains a list of Link Objects which contain information on child nodes

	def __init__(self, id):
		self.id = id  # string character
		self.links = []  # list of link objects (info on nodes this node is linked to)
		self.parent = None  # parent node 
		self.weight = None  # path cost to reach this node
		
	def addLink(self, nodeObj, weight):  # add link object
		self.links.append(Link(nodeObj, weight))
		self.links.sort(key=Link.getNodeId)   # sort the links alphabetically, will be added to frontier in that order
		
	def getId(self):
		return self.id
		
	def getLinks(self):
		return self.links
		
	def getWeight(self):
		return self.weight
		
	def setWeight(self, num):
		self.weight = num
		
	def setParentNode(self, nodeObj):
		self.parent = nodeObj
		
	def getParentNode(self):
		return self.parent
	
	def printInfo(self):
		print("Node: " + self.id)
		for links in self.links:
			print(links) 
	
	def __str__(self):
		return self.id
			
	
	
class Link(object):
	# Link class stores the information on what node a link connects and 
	# what the cost of the link is.
	
	def __init__(self, nodeObj, weight):
		self.nodeObj = nodeObj
		self.weight = weight
	
	def getNode(self):
		return self.nodeObj
	
	def getNodeId(self):
		return self.nodeObj.id
	
	def getCost(self):
		return self.weight
	
	def __str__(self):
		return "\tLink: " + str(self.nodeObj) + "  weight: " + str(self.weight)

	

def breadthOrDepthFirstSearch(sn, gn, type):
	# Algorithm to accomplish breadth-first search or depth first search across the node list.
	# The only difference between the two types of search is breadth uses a queue for frontier
	# and depth uses a stack.  The type argument tell the function which type of search to do.
	
	frontier = deque()  # frontier = FIFO queue and add sn to frontier
	frontier.append(sn)  # add start node to frontier
	explored = []   # nodes explored
	path = []  # stores node path info from start node to end node
	previousNode = None  # used to temporarily hold information about parent node

	
	if sn == gn:  # if start node = goal node, return explored list with start node only
		path.append(sn.getId())
		return path
	else:
		while frontier: 
			
			if type == "Breadth":
				tempNode = frontier.popleft()  # frontier acts as a queue for breadth search
			else:  # type == "Depth"
				tempNode = frontier.pop()  # frontier acts as a stack for depth search
			explored.append(tempNode)  #  add popped node to explored list
			

			for childLink in tempNode.getLinks():  # for each child of popped node
				childNode = childLink.getNode()
				if not (childNode in frontier) and not (childNode in explored):  # if node not in either list
					
					childNode.setParentNode(tempNode)  # child node records who it's parent is
					
					if childNode.getId() == gn.getId():  # check to see if node is goal node
						
						path.append(childNode.getId())
						previousNode = childNode.getParentNode()
						
						while previousNode != None:
							path.append(previousNode.getId())  # fills path list with node path info
							previousNode = previousNode.getParentNode()
							
							
						return path # return solution list (path from start to goal)
					
					else:
						frontier.append(childNode)  # add child node to frontier		
				
	return path  # returns empty set



def uniformSearch(sn, gn):
	path = []  # stores node path info from start node to end node
	frontier = []  # a priority queue, lowest cost node are popped first
	explored = []  # nodes explored
	previousNode = None  # used to temporarily hold information about parent node
	cost = 0  # Accumulated cost to get to a node from start node
	
	sn.setWeight(0)  # start node has a cost of 0
	frontier.append(sn)  # add start node to frontier
	
	
	if sn == gn:  # if start node = goal node, return explored list with start node only
		path.append(sn.getId())
		return path
	else:
		while frontier:
			
			tempNode = frontier.pop()  # pop least cost node from stack
			cost = tempNode.getWeight()  # update current path cost
			
			# Check if popped node is goal node.  Goal node is only popped if it is
			# currently the least cost node in the stack.
			if tempNode.getId() == gn.getId():
				
				path.append(tempNode.getId())
				previousNode = tempNode.getParentNode()
				
				while previousNode != None:
					path.append(previousNode.getId())  # fills path list with node path inf
					previousNode = previousNode.getParentNode()
				return path  # return path info of solution
				
				
			explored.append(tempNode)  # node has been explored
			
			for childLink in tempNode.getLinks():
				childNode = childLink.getNode()
				
				if not (childNode in frontier) and not (childNode in explored):  # if node not in frontier or explored
				
					childNode.setParentNode(tempNode)
				
					childNode.setWeight(cost + childLink.getCost())  # child node records path cost info
					frontier.append(childNode)  # child node added to frontier

					# Bubble Sort.  Very small frontier size so went with simplest coding option
					i = len(frontier) - 1
					if i > 0:
						unsorted = True
						while unsorted:
							if frontier[i].getWeight() >= frontier[i-1].getWeight():
								swapNode = frontier[i-1]
								frontier[i-1] = frontier[i]
								frontier[i] = swapNode
							else:
								unsorted = False
							i -= 1
							if i == 0:
								unsorted = False
						
				
				else:  # child node already either in explored or frontier
					# If node in frontier, check if updated cost is less than the cost currently
					# stored by node.  If updated cost is less, update node with new cost info
					if childNode in frontier:
						if (cost + childLink.getCost()) < childNode.getWeight():
							childNode.setWeight = cost + childLink.getCost()
							
		
		return path  # returns empty path list
	
	

# START OF PROGRAM
def main(arg1, arg2, arg3, arg4, arg5):

	f = open(arg1, 'r')  # open input text file, read only
	output = ""

	nodeList = []  # contains list of node objects
	# Read each line in txt file and create a node for each link
	for nodeInfo in f:  # for each line in input text file
		newNode = True
		for node in nodeList:  # traverse nodeList
			if node.id == nodeInfo[:1]:  # read first character for node name, check if exists
				newNode = False
				nodeAddingLink = node 
		if newNode == True:  
			nodeList.append(Node(nodeInfo[:1]))  # add new node to nodeList
			nodeAddingLink = nodeList[-1]  # the node just added in the line above
		
		newNode = True
		for node in nodeList:  # traverse nodeList
			if node.id == nodeInfo[2:3]:  # check if linked node is a new node
				newNode = False
				linkedNode = node  # node to be linked to
		if newNode == True:	
			nodeList.append(Node(nodeInfo[2:3]))
			linkedNode = nodeList[-1]  # the node being linked is the node just added in line above
		
		nodeAddingLink.addLink(linkedNode, int(nodeInfo[3:]))  # adds a Link object in node adding new link
			
	#for node in nodeList:
	#	node.printInfo()
	
	startNode = None
	goalNode = None
	solution = None
	
	for node in nodeList:
		if node.id == arg3:
			startNode = node
		if node.id == arg4:
			goalNode = node
	
	if startNode != None and goalNode != None:  # make sure the user given start/goal node names exist

		if arg2 == "Breadth" or arg2 == "Depth":
			solution = breadthOrDepthFirstSearch(startNode, goalNode, arg2)  # do a breadth-first or depth-first search
		if arg2 == "Uniform":
			solution = uniformSearch(startNode, goalNode)  # do a Uniform cost search

		if solution == []:
			output = "No Solution."
			print("No solution.")
			
		else:
			while len(solution) > 0:  # prepare solution path for writing to .txt file
				tempString = ""
				tempString = solution.pop()
				output += tempString + "\n"
		
		outFile = open(arg5, 'w')  # write solution path to .txt file, named by user
		outFile.write(output)
		
		f.close()
		outFile.close()
		
	else:
		print("Start/Goal node input error.")  # user given start or goal node name didn't exist
	
# END OF PROGRAM


main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

	#arg1 input filename, "sample1.txt"
	#arg2 "search type to run, Breadth" or "Depth" or "Uniform"
	#arg3 start node, "A"
	#arg4 goal noade, "G"
	#arg5 output file to write solution, "output1.txt"