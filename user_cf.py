# Starter code for uesr-based collaborative filtering
# Complete the function user_based_cf below. Do not change it arguments and return variables. 
# Do not change main() function, 

# import modules you need here.
import sys
import numpy as np
from operator import itemgetter
from scipy.stats import mode
import scipy.stats

#user, movie, rating
def user_based_cf(datafile, userid, movieid, distance, k, iFlag, numOfUsers, numOfItems):
    file = open(datafile)
    #read file 
    content = file.readlines()
    #hardcoded number of users by number of films (have to be one more than usual because ids are not zero indexed)
    ratings = np.zeros((944,1683))
    #all users where distance is key and vector is value
    neighbors = []
    #list of ratings of k closest neighbors
    k_ratings = []
    trueRating = float()
    predictedRating = float()
    sorted_neighbors = []
        
    for line in content:
        review = line.strip()
        review = review.split('\t')
        
        ratings[int(review[0])][int(review[1])] = float(review[2])

    #manhattan distance    
    if distance == 1:
        #iterate through each user
        for i in xrange(1, 944):
            if i == int(userid):
                #find true rating
                trueRating = ratings[int(userid)][int(movieid)]
                
            else:
                #find manhattan distance between target userid and this given user
                distance = manhattan_distance(ratings[int(userid)], ratings[i])
                #create a dictionary where distance maps to vector
                neighbors.append((distance, ratings[i]))
                
        #sort users based on distance 
        sorted_neighbors = sorted(neighbors, key=itemgetter(0))
        
    #pearson's correlation  
    if distance == 0:
        #iterate through each user
        for i in xrange(1, 944):
            if i == int(userid):
                #find true rating
                trueRating = ratings[int(userid)][int(movieid)]
            else:
                #find pearson's correlation between target userid and this given user
                correlation = (scipy.stats.pearsonr(ratings[int(userid)], ratings[i]))[0]
                #create a dictionary where distance maps to vector
                neighbors.append((correlation, ratings[i]))
                
        #sort users based on distance 
        sorted_neighbors = sorted(neighbors, key=itemgetter(0))
        sorted_neighbors = list(reversed(sorted_neighbors))
        
    #get k closest neighbors based on distance calculation above
    counter = 0
    i = 0
    while counter < k:
        if i > 941:
            break
            
        rating = sorted_neighbors[i][1][movieid]
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
    if len(k_ratings) == 0:
        predictedRating = 0
    else:     
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
        
    trueRating, predictedRating = user_based_cf(datafile, userid, movieid, distance, k, i, numOfUsers, numOfItems)
    print 'userID:{} movieID:{} trueRating:{} predictedRating:{} distance:{} K:{} I:{}'\
    .format(userid, movieid, trueRating, predictedRating, distance, k, i)




if __name__ == "__main__":
    main()