import random
import sys
import numpy as np
import operator
from scipy.stats import mode
import scipy.stats
import math
from operator import itemgetter
import pickle
import matplotlib.pyplot as plt

#user, movie, rating
def item_based_cf(datafile, userid, movieid, distance, k, iFlag, numOfUsers, numOfItems):
    #hardcoded number of films by number of users (have to be one more than usual because ids are not zero indexed)
    ratings = np.zeros((1683,944))
    neighbors = []
    #list of ratings of k closest neighbors
    k_ratings = []
    #return values
    trueRating = float()
    predictedRating = float()
    sorted_neighbors = []
    
    for line in datafile:
        review = line.strip()
        review = review.split('\t')
        ratings[int(review[1])][int(review[0])] = float(review[2])
    
    #manhattan distance    
    if distance == 1:
        #iterate through each movie
        for i in xrange(1, 1683):
            if i == int(movieid):
                #find true rating
                pass

            else:
                #find manhattan distance between target userid and this given user
                distance = manhattan_distance(ratings[int(movieid)], ratings[i])
                #create a dictionary where distance maps to movie vector
                neighbors.append((distance, ratings[i]))
                
        #sort users based on distance 
        sorted_neighbors = sorted(neighbors, key=itemgetter(0))
    
    #pearson's correlation  
    if distance == 0:
        #iterate through each user
        for i in xrange(1, 1683):
            if i == int(movieid):
                #find true rating
                pass
            else:
                #find pearson's correlation between target userid and this given user
                correlation = (scipy.stats.pearsonr(ratings[int(movieid)], ratings[i]))[0]
                #create a dictionary where distance maps to vector
                neighbors.append((correlation, ratings[i]))
                
        #sort users based on distance 
        sorted_neighbors = sorted(neighbors, key=itemgetter(0))
        sorted_neighbors = list(reversed(sorted_neighbors))
                
    #get k closest neighbors based on distance calculation above
    counter = 0
    i = 0
    
    while counter < k:
        if i > 1680:
            break
            
        rating = sorted_neighbors[i][1][int(userid)]
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

    #print k_ratings
    #find mode of k closest neighbors ratings
    if len(k_ratings) == 0:
        predictedRating = 0
    else:     
        predictedRating = mode(k_ratings)[0][0]
      
    return predictedRating

#find manhattan distance between two lists
def manhattan_distance(list1, list2):
    distance = 0
    for i in xrange(len(list1)):
        distance+= abs(list1[i]-list2[i])
    return distance

def main():
    datafile = sys.argv[1]
    distance = int(sys.argv[2])
    k = int(sys.argv[3])
    iFlag = int(sys.argv[4])
    numOfUsers = 943
    numOfItems = 1682
    file = open(datafile)
    content = file.readlines()
    samples = [[] for i in xrange(50)]
    indices = [[] for i in xrange(50)]
    MSE_total = 0
    X = []
    Y = []
    
    
    #pickle the file so same sample is always used, get 50 samples of 100 draws
    try:
        samples = pickle.load(open("var.pickle", "rb"))
    except (OSError, IOError) as e:
        print "enter"
        for i in xrange(50):
            temp_content = content
            for j in xrange(100):
                index = random.randint(0, len(temp_content)-1)
                draw = temp_content[index]
                samples[i].append(draw)
                temp_content = temp_content[0:index]+temp_content[(index+1):]
                
        pickle.dump(samples, open("var.pickle", "wb"))
    
    for i in xrange(50):
        total_error = 0
        for j in xrange(100):
            review = samples[i][j].strip()
            review = review.split('\t')
            userid = review[0]
            movieid = review[1]
            trueRating = int(review[2])

            datafile = list(set(content) - set(samples[i]))
            predictedRating = item_based_cf(datafile,userid, movieid, distance, k, iFlag, numOfUsers, numOfItems)
            # print 'userID:{} movieID:{} trueRating:{} predictedRating:{} distance:{} K:{} I:{}'\
            # .format(userid, movieid, trueRating, predictedRating, distance, k, iFlag)
            
            #find error 
            error = predictedRating - trueRating
            #squared error and aggregate
            total_error += math.pow(error, 2)

        #add total MSE
        MSE_total += total_error/100
        print "THE MSE OF THIS SAMPLE WAS"
        Y.append(total_error/100)
        print total_error/100
    
    #data distribution
    print Y
    
    #average across all MSE
    final_MSE = MSE_total/50
    print "THE MSE OF THIS SAMPLING WAS: " + str(final_MSE)

    #plot graph of MSE by iteration
    for i in xrange(50):
        X.append(i)

    plt.plot(X, Y)
    plt.ylabel('MSE')
    plt.xlabel('Sample Number')
    plt.axis([0, 50, 0, 25])
    plt.title('Item Collab k = 32')
    plt.savefig('ICideal.png')



if __name__ == "__main__":
    main()