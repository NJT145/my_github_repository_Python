from recommendations import *

user = "277168"

#step 2
prefs = loadBookRatings2('BX-Book-Ratings.csv')

#step 3
user_based_cf = getRecommendations(prefs, user, similarity=sim_distance)

print user_based_cf
#step 4

#
itemMatch = calculateSimilarItems(prefs)
#
item_based_cf = getRecommendedItems(prefs, itemMatch, user)
print item_based_cf
#
# #step 5
# print user_based_cf
# print item_based_cf
#
# #step 6 (extra practice)
# prefs=loadBookRatingsWithTitles('BX-Book-Ratings.csv', 'BX-Books.csv')
#
# #step 6.3
# user_based_cf = getRecommendations(prefs, user, similarity=sim_distance)
#
# #step 6.4
# itemMatch= calculateSimilarItems(prefs)
# item_based_cf = getRecommendedItems(prefs, itemMatch, user)
#
# #step 6.5
# print user_based_cf
# print item_based_cf


