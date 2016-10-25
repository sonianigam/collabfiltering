# Starter code for uesr-based collaborative filtering
# Complete the function user_based_cf below. Do not change it arguments and return variables. 
# Do not change main() function, 

# import modules you need here.
import sys
import numpy as np

#user, movie, rating
def user_based_cf(datafile, userid, movieid, distance, k, iFlag, numOfUsers, numOfItems):
    #dont get title line in content
    file = open(datafile)
    first_line = file.readline()
    #read rest of the file 
    content = file.readlines()
    #hardcoded number of users by number of films (have to be one more than usual because ids are not zero indexed)
    ratings = np.zeros((944,1683))
    neighbors = dict()
        
    for line in content:
        review = line.strip()
        review = review.split('\t')
        ratings[int(review[0])][int(review[1])] = float(review[2])
    
    #manhattan distance    
    if iFlag == 1:
        for i in xrange(944):
            if i == userid:
                pass
            else:
                distance = manhattan_distance(ratings[userid], ratings[i])
                neighbors[distance] = ratings[i]
        
    print neighbors
        
        
        
    return 4,5
    #return trueRating, predictedRating

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
    
    print datafile
    
    trueRating, predictedRating = user_based_cf(datafile, userid, movieid, distance, k, i, numOfUsers, numOfItems)
    print 'userID:{} movieID:{} trueRating:{} predictedRating:{} distance:{} K:{} I:{}'\
    .format(userid, movieid, trueRating, predictedRating, distance, k, i)




if __name__ == "__main__":
    main()