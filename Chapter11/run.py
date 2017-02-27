import gp

# Building and Evaluating Trees
# exampletree=gp.exampletree()
# print exampletree.evaluate([2,3])
# print exampletree.evaluate([5,3])

# Displaying the Programs
# exampletree.display()

# Creating the Initial Population

# random1=gp.makerandomtree(2)
# print random1.evaluate([7,1])
# print random1.evaluate([2,4])
# random2=gp.makerandomtree(2)
# print random2.evaluate([5,3])
# print random2.evaluate([5,20])
# print('\n')
# random1.display()
# print('\n')
# random2.display()

# A Simple Mathematical Test
# print gp.buildhiddenset()

# Mutating Programs
# random1 = gp.makerandomtree(2)
# random1.display()
# random2 = gp.makerandomtree(2)
# random2.display()
# mutttee = gp.mutate(random2, 2)
# mutttee.display()
# cross = gp.crossover(random1, random2)
# cross.display()
# hiddenset = gp.buildhiddenset()
# print gp.scorefunction(random2, hiddenset)
# print gp.scorefunction(mutttee, hiddenset)
# print gp.scorefunction(cross, hiddenset)

rf = gp.getrankfunction(gp.buildhiddenset())
gp.evolve(2, 500, rf, mutationrate=0.2, breedingrate=0.1, pexp=0.7, pnew=0.1)
