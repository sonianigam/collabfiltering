# Starter code for item-based collaborative filtering
# Complete the function item_based_cf below. Do not change its name, arguments and return variables. 
# Do not change main() function, 

# import modules you need here.
import sys
import numpy as np
import operator
from scipy.stats import mode
import scipy.stats

#user, movie, rating
def item_based_cf(datafile, userid, movieid, distance, k, iFlag, numOfUsers, numOfItems):
    file = open(datafile)
    #read file 
    content = file.readlines()
    #hardcoded number of films by number of users (have to be one more than usual because ids are not zero indexed)
    ratings = np.zeros((1683,944))
    neighbors = dict()
    #list of ratings of k closest neighbors
    k_ratings = []
    #return values
    trueRating = float()
    predictedRating = float()
    sorted_neighbors = []
    
    for line in content:
        review = line.strip()
        review = review.split('\t')
        ratings[int(review[1])][int(review[0])] = float(review[2])
    
    #manhattan distance    
    if distance == 1:
        #iterate through each movie
        for i in xrange(1, 1683):
            if i == int(movieid):
                #find true rating
                trueRating = ratings[int(movieid)][int(userid)]

            else:
                #find manhattan distance between target userid and this given user
                distance = manhattan_distance(ratings[int(movieid)], ratings[i])
                #create a dictionary where distance maps to movie vector
                neighbors[distance] = ratings[i]
                
        #sort users based on distance 
        sorted_neighbors = sorted(neighbors.items(), key=operator.itemgetter(0))
    
    #pearson's correlation  
    if distance == 0:
        #iterate through each user
        for i in xrange(1, 1683):
            if i == int(movieid):
                #find true rating
                trueRating = ratings[int(movieid)][int(userid)]

            else:
                #find pearson's correlation between target userid and this given user
                correlation = (scipy.stats.pearsonr(ratings[int(movieid)], ratings[i]))[0]
                #create a dictionary where distance maps to vector
                neighbors[correlation] = ratings[i]
                
        #sort users based on distance 
        sorted_neighbors = sorted(neighbors.items(), key=operator.itemgetter(0))
        sorted_neighbors = list(reversed(sorted_neighbors))
                
    #get k closest neighbors based on distance calculation above
    counter = 0
    i = 0
    while counter < k:
        rating = sorted_neighbors[i][1][userid]
        if iFlag == 1:
            #aggregate k closest neighbors ratings even if they have a 0 rating for the given movie
            k_ratings.append(rating)
            counter += 1
            i+= 1
        else:
            if int(rating) != 0:
                k_ratings.append(rating)
                counter += 1
            i+= 1

    print k_ratings
    #find mode of k closest neighbors ratings
    predictedRating = mode(k_ratings)[0][0]
  
    return trueRating, predictedRating

def manhattan_distance(list1, list2):
    distance = 0
    for i in xrange(len(list1)):
        distance+= abs(list1[i]-list2[i])
    return distance

def main():
    datafile = sys.argv[1]
    userid = int(sys.argv[2])
    movieid = int(sys.argv[3])
    distance = int(sys.argv[4])
    k = int(sys.argv[5])
    i = int(sys.argv[6])
    numOfUsers = 943
    numOfItems = 1682

    trueRating, predictedRating = item_based_cf(datafile, userid, movieid, distance, k, i, numOfUsers, numOfItems)
    print 'userID:{} movieID:{} trueRating:{} predictedRating:{} distance:{} K:{} I:{}'\
    .format(userid, movieid, trueRating, predictedRating, distance, k, i)




if __name__ == "__main__":
    main()