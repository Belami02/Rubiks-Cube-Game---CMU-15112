import csv
scores = []

# reading
with open('scores.csv') as file:
    for i in file:
        scores.append(i)

    file.close()

# manipulating the ranking
scores.insert(0, 'Youssef, 11\n')

# writing
file = open('scores.csv', 'w')
file.writelines(scores)
file.close()

# onAppStart
#   read the ranking

def displayLeaderBoard():
    for i in scores[0:3]: # list of name, score
        # draw the score
        pass

# when the person finishes the rubik
#   check if the time the person completed is smaller than the 3 first people in the ranking
#       if yes
#           insert the person in the correct position in the ranking
#           write the new list in the file
#       else
#           do nothing
