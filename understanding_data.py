# Starter code for item-based collaborative filtering
# Complete the function item_based_cf below. Do not change its name, arguments and return variables. 
# Do not change main() function, 

# import modules you need here.
import sys
import numpy as np
import matplotlib.pyplot as plt
import operator


def common_movie_reviews(datafile):
    #dont get title line in content
    file = open(datafile)
    first_line = file.readline()
    #read rest of the file 
    content = file.readlines()
    #central reviews dictionary
    reviews = dict()
    #keeps track of pairs with same number of reviews
    numbers = dict()
    raw_mm_calc = []
            
    for line in content:

        review = line.strip()
        review = review.split('\t')
        
        if review[0] in reviews.keys():
            reviews[review[0]].append(review[1])
        else:
            reviews[review[0]] = [review[1]]
            
    
    for x in reviews:
        for y in reviews:
            if y == x:
                pass
            else:
                common = set(reviews[x])&set(reviews[y])
                raw_mm_calc.append(len(common))

    median = np.median(np.array(raw_mm_calc))
    mean = np.mean(np.array(raw_mm_calc))
    
    return mean, median, raw_mm_calc
    

def movie_reviews(datafile):
    file = open(datafile)
    first_line = file.readline()
    #read rest of the file 
    content = file.readlines()
    #central reviews dictionary
    reviews = dict()
    maximum = []
    minimum = []
    
    for line in content:
        movie = line.strip()
        movie = movie.split('\t')
        
        if movie[1] in reviews.keys():
            reviews[movie[1]] += 1
        else:
            reviews[movie[1]] = 1
            
    sorted_reviews = sorted(reviews.items(), key=operator.itemgetter(1))
    
    max_value = sorted_reviews[len(sorted_reviews)-1][1]
    min_value = sorted_reviews[0][1]
    
    for x in sorted_reviews:
        if x[1] == max_value:
            maximum.append(x[0])
        elif x[1] == min_value:
            minimum.append(x[0])
            
    print "Movie " + str(maximum) + " had the maximum number of reviews with: " + str(max_value) + " reviews"
    print "The following movies had the minimum number of reviews " + str(minimum) + " with: " + str(min_value) + " review"
        
    return sorted_reviews

def main():
    datafile = sys.argv[1]
    # mean, median, raw = common_movie_reviews(datafile)
    # bins = len(set(raw))
    # print "Mean number of common reviewed movies: " + str(mean)
    # print "Median number of common reviewed movies: "+ str(median)
    #
    # plt.hist(raw,bins)
    # plt.ylabel('Number of Users')
    # plt.xlabel('Number in Common')
    # plt.axis([0, 150, 0, 80000])
    # plt.title('MovieLens 100K Dataset Analysis')
    # plt.savefig('Data.png')

    reviews = movie_reviews(datafile)
    
    X = []
    Y = []
    
    for movie in reviews:
        X.append(movie[0])
        Y.append(movie[1])

    plt.plot(X, Y, 'ro')
    plt.ylabel('Number of Reviews')
    plt.xlabel('Movie ID')
    plt.axis([0, 1700, 0, 600])
    plt.title('MovieLens 100K Dataset Analysis: Movie Reviews')
    plt.savefig('MovieReviews.png')
    
    
    
if __name__ == "__main__":
    main()