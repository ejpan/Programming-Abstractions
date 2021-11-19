"""
Name: movie_recommendations.py
Date: October 21, 2021
Author: Eric Pan and Rayan Pal
Description: Predicts movie ratings for users.
"""

import math
import csv
from scipy.stats import pearsonr

class BadInputError(Exception):
    """Exception for invalid user or movie ID"""
    print("user ID or movie ID is not in database")

class Movie_Recommendations:

    def __init__(self, movie_filename, training_ratings_filename):
        """
        Initializes the Movie_Recommendations object from 
        the files containing movie names and training ratings.  
        The following instance variables should be initialized:
        self.movie_dict - A dictionary that maps a movie id to
               a movie objects (objects the class Movie)
        self.user_dict - A dictionary that maps user id's to a 
               a dictionary that maps a movie id to the rating
               that the user gave to the movie.    
        """

        #Creates a movie dictionary.
        self.movie_dict = dict()
        
        #Creates a user dictionary.
        self.user_dict = dict()

        #Reads movie file and assigns user ID to the key of user_dict. 
        f = open(movie_filename)
        csv_reader = csv.reader(f, delimiter = ',', quotechar = '"')
        #The value of the key is the movie object and this iteration assigns the movie ID and title to object.
        for line in csv_reader:
            movie = Movie(int(line[0]), line[1])
            self.movie_dict[int(line[0])] = movie
        
        #Reads movie rating file and assigns user ID to key in user dictionary. 
        g = open(training_ratings_filename)
        user_reader = g.readlines()
        #Value is a dictionary containing the key as the movie ID and rating for that particular movie for a user.
        for line in user_reader:
            spline = line.split(',')
            if (int(spline[0]) in self.user_dict):
                self.user_dict[int(spline[0])][int(spline[1])] = (float(spline[2]))
            else:
                self.user_dict[int(spline[0])] = dict()
                self.user_dict[int(spline[0])][int(spline[1])] = (float(spline[2]))
            #Adds user to the users instance variable which contains a list of users that have watched a particular movie.
            self.movie_dict[int(spline[1])].users.append(int(spline[0]))
            

    def predict_rating(self, user_id, movie_id):
        """
        Returns the predicted rating that user_id will give to the
        movie whose id is movie_id. 
        If user_id has already rated movie_id, return
        that rating.
        If either user_id or movie_id is not in the database,
        then BadInputError is raised.
        """
    
        total = 0
        denominator = 0
        #Checks if user ID and movie ID is valid.
        if (user_id not in self.user_dict) or (movie_id not in self.movie_dict):
            raise BadInputError
        #Returns rating if user has watched the movie.
        elif (user_id in self.movie_dict[movie_id].users):
            return self.user_dict[user_id][movie_id]
        else:
            #Computes the similiarty for user_id if they haven't watched movie_id.
            for other_movie_id in self.user_dict[user_id].keys():
                similarity_num = (self.user_dict[user_id][other_movie_id]) * (self.movie_dict[other_movie_id].get_similarity(movie_id, self.movie_dict, self.user_dict))
                total += similarity_num
                denominator += (self.movie_dict[other_movie_id].get_similarity(movie_id, self.movie_dict, self.user_dict))
            if denominator == 0:
                return 2.5
            else:
                rating = (total/denominator)
                return rating
        
            

    def predict_ratings(self, test_ratings_filename):
        """
        Returns a list of tuples, one tuple for each rating in the
        test ratings file.
        The tuple should contain
        (user id, movie title, predicted rating, actual rating)
        """

        #Creates a list containing tuples of user id, movie title, predicted rating, and actual rating.
        f = open(test_ratings_filename)
        lines = f.readlines()
        rating_list = []
        for i in lines:
            line = i.split(",")
            #creates tuple.
            one_review = (int(line[0]),self.movie_dict[int(line[1])].title,self.predict_rating(int(line[0]),int(line[1])),float(line[2]))
            #Adds tuple to list.
            rating_list.append(tuple(one_review))
        return (rating_list)
        

    def correlation(self, predicted_ratings, actual_ratings):
        """
        Returns the correlation between the values in the list predicted_ratings
        and the list actual_ratings.  The lengths of predicted_ratings and
        actual_ratings must be the same.
        """

        #Returns correlation value.
        return pearsonr(predicted_ratings, actual_ratings)[0]

        
class Movie: 
    """
    Represents a movie from the movie database.
    """
    def __init__(self, id, title):
        """ 
        Constructor.
        Initializes the following instances variables.  You
        must use exactly the same names for your instance 
        variables.  (For testing purposes.)
        id: the id of the movie
        title: the title of the movie
        users: list of the id's of the users who have
            rated this movie.  Initially, this is
            an empty list, but will be filled in
            as the training ratings file is read.
        similarities: a dictionary where the key is the
            id of another movie, and the value is the similarity
            between the "self" movie and the movie with that id.
            This dictionary is initially empty.  It is filled
            in "on demand", as the file containing test ratings
            is read, and ratings predictions are made.
        """
        "Instance Variables"

        #Creates instance variables for the object Movie.
        self.id = id
        self.title = title
        self.users = []
        self.similarities = dict()

    def __str__(self):
        """
        Returns string representation of the movie object.
        Handy for debugging.
        """

        #Returns string for debugging.
        return ("The movie ID and title are:", self.id,"," ,self.title)

    def __repr__(self):
        """
        Returns string representation of the movie object.
        """

        #Returns string for debugging.
        return ("repr:",self.id,",",self.title,",",self.users,",",self.similarities)

    def get_similarity(self, other_movie_id, movie_dict, user_dict):
        """ 
        Returns the similarity between the movie that 
        called the method (self), and another movie whose
        id is other_movie_id.  (Uses movie_dict and user_dict)
        If the similarity has already been computed, return it.
        If not, compute the similarity (using the compute_similarity
        method), and store it in both
        the "self" movie object, and the other_movie_id movie object.
        Then return that computed similarity.
        If other_movie_id is not valid, raise BadInputError exception.
        """

        #Checks if other_movie_id is valid.
        if other_movie_id not in movie_dict:
            raise BadInputError
        if self.id in self.similarities:
            return self.similarities[self.id]
        #Gets similarity of movies and adds it to the similiarity instance variable dictionary.
        else:
            sim = movie_dict[self.id].compute_similarity(other_movie_id, movie_dict, user_dict)
            self.similarities[other_movie_id] = sim
            movie_dict[other_movie_id].similarities[self.id] = sim
            return sim
        


    def compute_similarity(self, other_movie_id, movie_dict, user_dict):
        """ 
        Computes and returns the similarity between the movie that 
        called the method (self), and another movie whose
        id is other_movie_id.  (Uses movie_dict and user_dict)
        """
        
        #Computes similarity between movies.
        averages = []
        count = 0
        for user in self.users:
            #Checks if a user has watched both movies.
            if (user in self.users and user in movie_dict[other_movie_id].users):
                id_average = abs(user_dict[user][self.id] - user_dict[user][other_movie_id])
                averages.append(id_average)
                count+=1
        if count>=1:
            ave = sum(averages)
            diff = ave / count
            similarity = 1 - (diff)/4.5
        else:
            similarity = 0
        return similarity

if __name__ == "__main__":
    # Create movie recommendations object.
    movie_recs = Movie_Recommendations("movies.csv", "training_ratings.csv")

    # Predict ratings for user/movie combinations
    rating_predictions = movie_recs.predict_ratings("test_ratings.csv")
    print("Rating predictions: ")
    for prediction in rating_predictions:
        print(prediction)
    predicted = [rating[2] for rating in rating_predictions]
    actual = [rating[3] for rating in rating_predictions]
    correlation = movie_recs.correlation(predicted, actual)
    print(f"Correlation: {correlation}")    