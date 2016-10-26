import random
import sys
import numpy as np
import operator
from scipy.stats import mode
import scipy.stats

#user, movie, rating
def user_based_cf(datafile, userid, movieid, distance, k, iFlag, numOfUsers, numOfItems):
    #hardcoded number of users by number of films (have to be one more than usual because ids are not zero indexed)
    ratings = np.zeros((944,1683))
    #all users where distance is key and vector is value
    neighbors = dict()
    #list of ratings of k closest neighbors
    k_ratings = []
    trueRating = float()
    predictedRating = float()
    
    for line in datafile:
        review = line.strip()
        review = review.split('\t')
        
        ratings[int(review[0])][int(review[1])] = float(review[2])

    #manhattan distance    
    if distance == 1:
        #iterate through each user
        for i in xrange(1, 944):
            if i == int(userid):
                pass
            else:
                #find manhattan distance between target userid and this given user
                distance = manhattan_distance(ratings[int(userid)], ratings[i])
                #create a dictionary where distance maps to vector
                neighbors[distance] = ratings[i]
                
        #sort users based on distance 
        sorted_neighbors = sorted(neighbors.items(), key=operator.itemgetter(0))
        
    #pearson's correlation  
    if distance == 0:
        #iterate through each user
        for i in xrange(1, 944):
            if i == int(userid):
                pass
            else:
                #find pearson's correlation between target userid and this given user
                correlation = (scipy.stats.pearsonr(ratings[int(userid)], ratings[i]))[0]
                #create a dictionary where distance maps to vector
                neighbors[correlation] = ratings[i]
                
        #sort users based on distance 
        sorted_neighbors = sorted(neighbors.items(), key=operator.itemgetter(0))
        sorted_neighbors = list(reversed(sorted_neighbors))
        
    #get k closest neighbors based on distance calculation above
    counter = 0
    i = 0
    while counter < k:
        rating = sorted_neighbors[i][1][int(movieid)]
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
        
    return predictedRating

def manhattan_distance(list1, list2):
    distance = 0
    for i in xrange(len(list1)):
        distance+= abs(list1[i]-list2[i])
    return distance

def main():
    datafile = sys.argv[1]
    distance = int(sys.argv[2])
    k = int(sys.argv[3])
    i = int(sys.argv[4])
    numOfUsers = 943
    numOfItems = 1682
    file = open(datafile)
    content = file.readlines()
    samples = [[] for i in xrange(50)]
    indices = [[] for i in xrange(50)]
    
    for i in xrange(50):
        temp_content = content
        for j in xrange(100):
            index = random.randint(0, len(temp_content)-1)
            draw = temp_content[index]
            samples[i].append(draw)
            temp_content = temp_content[0:index]+temp_content[(index+1):]
    
    for i in xrange(50):
        for j in xrange(100):
            review = samples[i][j].strip()
            review = review.split('\t')
            userid = review[0]
            movieid = review[1]
            trueRating = review[2]
            
            datafile = list(set(content) - set(samples[i]))
                        
            predictedRating = user_based_cf(datafile,userid, movieid, distance, k, i, numOfUsers, numOfItems)
            
            print 'userID:{} movieID:{} trueRating:{} predictedRating:{} distance:{} K:{} I:{}'\
            .format(userid, movieid, trueRating, predictedRating, distance, k, i)




if __name__ == "__main__":
    main()