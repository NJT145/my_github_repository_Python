# A dictionary of movie critics and their ratings of a small
# set of movies
import csv
critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                         'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5},
           'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                                'Superman Returns': 3.5, 'The Night Listener': 4.0},
           'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                            'The Night Listener': 4.5, 'Superman Returns': 4.0,
                            'You, Me and Dupree': 2.5},
           'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                            'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 2.0},
           'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                             'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
           'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0},
           'Ali': {'Just My Luck': 1.0, 'You, Me and Dupree': 2.0, 'The Night Listener': 4.5, 'Superman Returns': 1.0,
                   'Snakes on a Plane': 4.5}}

from math import sqrt

# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs, person1, person2):
    # Get the list of shared_items
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]: si[item] = 1

    # if they have no ratings in common, return 0
    if len(si) == 0: return 0

    # Add up the squares of all the differences
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                          for item in prefs[person1] if item in prefs[person2]])

    return 1 / (1 + sqrt(sum_of_squares))


# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs, p1, p2):
    # Get the list of mutually rated items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item] = 1

    # if they are no ratings in common, return 0
    if len(si) == 0: return 0

    # Sum calculations
    n = len(si)

    # Sums of all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    # Sums of the squares
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    # Sum of the products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    # Calculate r (Pearson score)
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0: return 0

    r = num / den

    return r


def sim_jaccard(prefs, genre1, genre2):  # Jaccard Distance (A, B) = |A intersection B| / |A union B|

    # Get the list of shared_items
    p1_intersect_p2 = {}
    for item in prefs[genre1]:
        if item in prefs[genre2]: p1_intersect_p2[item] = 1

    # if they have no items in common, return 0
    if len(p1_intersect_p2) == 0: return 0

    # Get the list of all items that we have
    p1_union_p2 = prefs[genre1]
    for item in prefs[genre2]:
        if item not in p1_union_p2: p1_union_p2[item] = 1

    #Get the total number of items for intersection and union
    p1_intersect_p2, p1_union_p2 = len(p1_intersect_p2), len(p1_union_p2)

    return float(p1_intersect_p2) / float(p1_union_p2) # return jaccard distance


def sim_jaccard2(prefs, genre1, genre2):

    #Get the list of items
    genre1_movies = prefs[genre1].keys()
    genre2_movies = prefs[genre2].keys()

    # Make them sets in order to be able to use built-in methods of it such as intersection and union
    p1, p2 = set(genre1_movies), set(genre2_movies)
    p1_intersect_p2 = p1.intersection(p2)
    p1_union_p2 = p1.union(p2)

    #Get the total number of items for intersection and union
    p1_intersect_p2, p1_union_p2 = len(p1_intersect_p2), len(p1_union_p2)

    # if they have no items in common, return 0
    if p1_intersect_p2 == 0: return 0

    return float(p1_intersect_p2) / float(p1_union_p2) # return jaccard distance


# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]


# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs, person, similarity=sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        # don't compare me to myself
        if other == person: continue
        sim = similarity(prefs, person, other)

        # ignore scores of zero or lower
        if sim <= 0: continue
        for item in prefs[other]:

            # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # Similarity * Score
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                # Sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim

    # Create the normalized list
    rankings = [(total / simSums[item], item) for item, total in totals.items()]

    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings


def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})

            # Flip item and person
            result[item][person] = prefs[person][item]
    return result


def calculateSimilarItems(prefs, n=10):
    # Create a dictionary of items showing which other items they
    # are most similar to.
    result = {}
    # Invert the preference matrix to be item-centric
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        # Status updates for large datasets
        c += 1
        if c % 100 == 0: print "%d / %d" % (c, len(itemPrefs))
        # Find the most similar items to this one
        scores = topMatches(itemPrefs, item, n=n, similarity=sim_distance)
        result[item] = scores
    return result


def getRecommendedItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}
    # Loop over items rated by this user
    for (item, rating) in userRatings.items():

        # Loop over items similar to this one
        for (similarity, item2) in itemMatch[item]:

            # Ignore if this user has already rated this item
            if item2 in userRatings: continue
            # Weighted sum of rating times similarity
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating
            # Sum of all the similarities
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity

    # Divide each total score by total weighting to get an average
    rankings = [(score / totalSim[item], item) for item, score in scores.items()]

    # Return the rankings from highest to lowest
    rankings.sort()
    rankings.reverse()
    return rankings


def loadMovieLens(path='/data/u.item'):
    # Get movie titles
    movies = {}
    for line in open(path + '/u.item'):
        (id, title) = line.split('|')[0:2]
        movies[id] = title

    # Load data
    prefs = {}
    for line in open(path + '/u.data'):
        (user, movieid, rating, ts) = line.split('\t')
        prefs.setdefault(user, {})
        prefs[user][movies[movieid]] = float(rating)
    return prefs


def loadMovieGenre(data):

    # define list of genres
    genres = ["Unknown", "Action", "Adventure", "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama",
              "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]

    #define a nested dict for each genre
    prefs = dict()
    for genre in genres:
        prefs.setdefault(genre, {})

    # parse the data
    for line in open(data):
        (id, title, releaseDate, videoReleaseDate, imdbUrl, unknown, action, adventure, animation, children_s,
         comedy, crime, documentary, drama, fantasy, film_noir, horror, musical, mystery, romance, sci_fi,
         thriller, war, western) = line.split('|')
        for index, genre in enumerate(
                [unknown, action, adventure, animation, children_s, comedy, crime, documentary, drama,
                 fantasy, film_noir, horror, musical, mystery, romance, sci_fi, thriller, war, western]):
            if genre == "1": # if it is of that genre
                prefs[genres[index]][title] = float(genre)
    return prefs # return parsed data



#parse the file BX-Book-Ratings.csv
def loadBookRatings(data1):
    dictionary={}
    i = 1
    for line in open(data1):
        #skip first line of the file="User-ID";"ISBN";"Book-Rating"
        if i == 1:
            i += 1
            continue
        else:
            print line[1:-1].split('";"')
            break
            (UserID, ISBN,BookRating0)=line[1:-1].split('";"')
            BookRating=BookRating0.split('"')[0]
            dictionary.setdefault( UserID,{})
            dictionary[UserID][ISBN]=float(BookRating)
    return dictionary

#parse the file BX-Books.csv
#data1=BX-Book-Ratings.csv
#data2=BX-Books.csv

def loadBookRatingsWithTitles(data1, data2):
    #result is a dictionary dataset
    result=loadBookRatings(data1)
    dictionary={}
    for key in result:
        dictionary.setdefault( key,{})
    dict_={}
    for line in open(data2):
        #first line of the file="ISBN";"Book-Title";"Book-Author";"Year-Of-Publication";"Publisher";"Image-URL-S";"Image-URL-M";"Image-URL-L"
        if line.startswith('"ISBN"'):
            continue
        else:
            (ISBN, BookTitle,BookAuthor,YearOfPublication,Publisher,ImageURLS,ImageURLM,ImageURLL)=line[1:-1].split('";"')
            dict_[ISBN]=BookTitle
    for key in result:
        for isbn in result[key]:
            if isbn in dict_:
                #get the value of the dict_ which is the name of the film
                book_title=dict_[isbn]
                dictionary[key][book_title]=result[key][isbn]
    return dictionary



def loadBookRatings2(book_ratings_data):
    prefs = dict() # create an empty dict
    with open(book_ratings_data) as brd: # open the file with the best possible way, because it it automatically closed
        brd.readline() # ignore the first line
        book_ratings = csv.reader(brd, delimiter=";") # read files with csv module
        for line in book_ratings:
            user_id, isbn, rating = line
            prefs.setdefault(user_id, {}) # create an empty nested dict if id not in prefs
            prefs[user_id][isbn] = float(rating) # the same syntax that we are familiar with, from critics
    return prefs

def loadBookRatingsWithTitles2(book_ratings_data, books_data):
    prefs = loadBookRatings2(book_ratings_data) # parse the first file
    book_ids_names = {} # create an empty dict for second file
    with open(books_data) as bd: # open the file with the best possible way in which close operating is handled automatically
        bd.readline() # ignore/pass the first line
        books_info = csv.reader(bd, delimiter=";") # read lines with csv module
        for book_info in books_info:
            isbn, book_title = book_info[:2] # take isbn and book_title
            book_ids_names[isbn] = book_title
    for user_id in prefs:
        isbn_s = prefs[user_id].keys() # take the list of isbn_s for each user_id
        for isbn in isbn_s: # for each isbn
            try:
                book_title = book_ids_names[isbn] # try if we can find the same isbn in book_ids_names dict
                prefs[user_id][book_title] = prefs[user_id].pop(isbn) #if it is so, then delete isbn version of it and assign it to title.
            except KeyError: # if we cannot find it there, then just leave it with the isbn
                pass
    return prefs

data1 = "BX-Book-Ratings.csv"
# data2 = "BX-Books.csv"
loadBookRatings(data1)
# print loadBookRatingsWithTitles(data1,data2)



