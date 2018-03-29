#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = 'jarethmoyo'

import Tkinter as tk
import ttk
from xlrd import open_workbook
import anydbm
import random
import pickle as pk
from recommendations import *

# Users that are actually in the database are shown below in the critics lis. Can change current_user variable
# to any one of them
# critics=["Murat","Phillips","Wendy","Emily","Samantha","Elif","Merve","Lexy","Peter",
#         "Timothy","Veronica","Ahmet","John"]
current_user="Neo"  # current user selected, not in food_critics.db

class FetchData(object):
    def __init__(self, excel_file, critics_database):
        self.critics_database=critics_database
        self.excel_file=excel_file
        self.meals = self.fetch_meals()
        self.method = "userbased"
        self.similarity="euclidean"
        self.sim_dict={"euclidean":sim_distance, "pearson":sim_pearson, "jaccard":sim_jaccard}
        self.counter=1
        self.chosen_meals=[]

    def fetch_meals(self):
        """Fetches all the meals from an excel file and returns a list of all
           these meals, to be stored in the init variable self.meals"""
        book = open_workbook(self.excel_file)
        sheet = book.sheet_by_index(0)
        meals=[sheet.cell(row_index,col_index).value.encode('utf-8') for row_index in range(sheet.nrows)\
               for col_index in range(sheet.ncols) if col_index == 0]
        return meals[1:]  # omit the meal header

    def store_to_db(self, user, val):
        """This method saves into a database a user as key, and val as value. In the case of the
           Food_Critics the value is a dictionary of the user's ratings"""
        database=anydbm.open(self.critics_database,"c")
        database[user]=pk.dumps(val)

#data = FetchData("Menu.xlsx","Food_Critics.db")


class Recommender(FetchData):
    def __init__(self, new_master):
        super(Recommender,self).__init__("Menu.xlsx","cc_ratings.db")
        new_master.title("Enter the Recommender")
        self.new_master=new_master
        # define our frames
        frame1 = tk.Frame(new_master)
        frame1.pack()
        frame2 = tk.Frame(new_master)
        frame2.pack(anchor=tk.W)
        frame3 = tk.Frame(new_master)
        frame3.pack(anchor=tk.W)
        s_frame=tk.Frame(frame3)
        s_frame.pack(side=tk.RIGHT)
        ss_frame=tk.Frame(s_frame)
        ss_frame.pack(side=tk.RIGHT)
        sss_frame=tk.Frame(ss_frame)
        sss_frame.pack(side=tk.RIGHT)
        frame4 = tk.Frame(new_master)
        frame4.pack(anchor=tk.E)
        frame5 = tk.Frame(new_master)
        frame5.pack()
        frame6 = tk.Frame(new_master)
        frame6.pack(anchor=tk.W)
        frame7 = tk.Frame(new_master)
        frame7.pack(anchor=tk.W)
        frame8 = tk.Frame(new_master)
        frame8.pack(anchor=tk.W)
        frame9 = tk.Frame(new_master)
        frame9.pack(anchor=tk.E)
        s2_frame = tk.Frame(frame9)
        s2_frame.pack(side=tk.RIGHT)
        frame10 =tk.Frame(new_master)
        frame10.pack(anchor=tk.W)
        frame11 =tk.Frame(new_master)
        frame11.pack(anchor=tk.W)
        self.user_frame=tk.Frame(frame11)
        self.user_frame.pack(side=tk.RIGHT)
        self.user_subframe=tk.Frame(self.user_frame)
        self.user_subframe.pack(side=tk.RIGHT)

        # top level labels definitions
        top_label_text="Cafe Crown Recommendation Engine-Sehir Special Edition"
        top_label = tk.Label(frame1, text=top_label_text, width=50, bg="black",
                             font="Arial 25 bold", fg="yellow")
        top_label.pack()
        intro_text="Welcome.\nPlease rate entries that you've had at CC, and" \
                   " we will recommend you what you may like to have"
        rate_a_meal = tk.Label(frame1, text=intro_text, font="Times 18")
        rate_a_meal.pack()
        skip_label = tk.Label(frame1, text="'"*332)
        skip_label.pack()

        # rate a meal labels
        meal_label = tk.Label(frame3, text="Choose a meal:",font="Helvetica 16", fg="brown")
        meal_label.pack(anchor=tk.W, padx=20)

        # initialising our combobox that will contain all meals from the cafe
        self.box_value=tk.StringVar()
        self.box=ttk.Combobox(frame3, state="readonly", textvariable=self.box_value,width=30)
        self.box['values'] = self.meals
        self.box.current(0)
        self.box.bind("<<ComboboxSelected>>")
        self.box.pack(side=tk.LEFT, anchor=tk.W, padx=20, pady=5)

        rate_label = tk.Label(s_frame, text="Enter your rating:", font="Helvetica 16", fg="brown")
        rate_label.pack(anchor=tk.W, padx=20)

        # scale widget
        self.scale= tk.Scale(s_frame,from_=1, to_=10, orient="horizontal", length=140)
        self.scale.pack(side=tk.LEFT,padx=40)

        # add button
        add = tk.Button(s_frame, text="Add", width=8, fg="blue", font="Times 13 bold", command=self.get_user_ratings)
        add.pack(side=tk.LEFT, padx=20)
        # user rating list box
        self.choice_box=tk.Listbox(ss_frame,height=6, width=30,font="Times 11")
        scroll_0=ttk.Scrollbar(ss_frame,command=self.choice_box.yview)
        scroll_0.pack(side=tk.RIGHT,fill=tk.Y)
        self.choice_box.config(yscrollcommand=scroll_0.set)
        self.choice_box.pack(side=tk.LEFT)
        # remove button
        remove = tk.Button(sss_frame, text="Remove\nSelected", font="Times 12 bold", fg="red", width=10,
                           command=self.remove_rating)
        remove.pack(padx=10)

        # skip label
        skip_label2 = tk.Label(frame5, text="."*332)
        skip_label2.pack()
        ###############################################################################################################
        # GET A RECOMMENDATION WIDGETS
        # top level labels
        gar_label = tk.Label(frame5, text="Get Recommendations", font="Times 18 bold") # get a recommendation
        gar_label.pack()
        skip_label3 = tk.Label(frame5, text="'"*332)
        skip_label3.pack()
        standard_label = tk.Label(frame6, text="Standard Recommendation", font="Helvetica 16 bold", fg="brown")
        standard_label.pack(side=tk.LEFT, padx=20)
        custom_label = tk.Label(frame6, text="Custom Recommendation", font="Helvetica 16 bold", fg="brown")
        custom_label.pack(padx=200)

        # standard recommendation widgets
        choose_num_ratings=tk.Label(frame7, text="Number of recommendations:", font="Verdana 10")
        choose_num_ratings.pack(side=tk.LEFT, padx=22)
        self.num_recommendations= tk.Text(frame7, width=2, height=1)
        self.num_recommendations.pack(side=tk.LEFT)
        self.num_recommendations.insert(tk.END,"3")  # set a default number of recommendations

        placeholder=tk.Label(frame8, text="."*26+".", font="Helvetica 19 bold", fg="white")
        placeholder.pack(side=tk.LEFT,padx=20,pady=10)

        # custom recommendation widgets
        settings_label= tk.Label(frame7, text="Configure your settings:", font="Verdana 10 italic",fg="purple")
        settings_label.pack(padx=260)
        # set up our radio buttons
        self.v=tk.IntVar()
        self.v.set(1)
        user_based=tk.Radiobutton(frame8,text='User Based',variable=self.v,value=1,font='Times 10 bold',
                                  command=self.user_based_sim)
        user_based.pack(anchor=tk.W,padx=292)
        item_based=tk.Radiobutton(frame8,text='Item Based',variable=self.v,value=2,font='Times 10 bold',
                                  command=self.item_based_sim)
        item_based.pack(anchor=tk.W, padx=292)
        # similarity widgets
        sim_label = tk.Label(frame9, text="Choose your similarity metric:", font="Verdana 10 italic",fg="purple")
        sim_label.pack(anchor=tk.E, padx=43)

        # similarity radio buttons
        self.v2=tk.IntVar()
        self.v2.set(1)
        euclidean=tk.Radiobutton(frame9,text='Euclidean Score',variable=self.v2,value=1,font='Times 10 bold',
                                 command=self.euclidean_method)
        euclidean.pack(anchor=tk.E, padx=130)
        pearson=tk.Radiobutton(frame9,text='Pearson Score',variable=self.v2,value=2,font='Times 10 bold',
                               command=self.pearson_method)
        pearson.pack(anchor=tk.E, padx=138)
        jaccard=tk.Radiobutton(frame9,text='Jaccard Score',variable=self.v2,value=3,font='Times 10 bold',
                               command=self.jaccard_method)
        jaccard.pack(anchor=tk.E, padx=140)
        get_std_rec=tk.Button(s2_frame, text="Get Recommendations", font="Helvetica 13 bold", fg="blue",
                              command=self.standard_reco)
        get_std_rec.pack(anchor=tk.E,padx=20,pady=10)

        skip_label4=tk.Label(frame10, text="."*332)
        skip_label4.pack()

        # configuration and results widgets
        result_label=tk.Label(frame10, text="Result Box (Recommendations):", font="Times 13")
        result_label.pack(side=tk.LEFT)

        self.result_box = tk.Text(frame11,width=40, height=7)
        scroll_1=ttk.Scrollbar(frame11,command=self.result_box.yview)
        scroll_1.pack(side=tk.RIGHT,fill=tk.Y)
        self.result_box.config(yscrollcommand=scroll_1.set)
        self.result_box.pack(side=tk.LEFT, pady=3, padx=5)

        # Custom reco widgets
        config=self.user_frame
        self.cus_label=tk.Label(config, text="Users similar to you", font="Verdana 11 bold", width=21,bg="purple",
                       fg="white")
        self.cus_label.pack()
        self.list_box=tk.Listbox(config, height=5, width=30,font="Times 11")
        self.list_box.bind("<<ListboxSelect>>", self.view_func)
        self.list_box.pack(side=tk.LEFT,anchor=tk.W, padx=10,pady=5)
        self.var = tk.StringVar()

         # result box
        self.rb_label = tk.Label(self.user_subframe, width=35, text="User ratings() select a user on the left",
                                 font="Verdana 10 bold", bg="brown", fg="white")
        self.rb_label.pack(anchor=tk.W, padx=5)
        self.result_box2 = tk.Text(self.user_subframe,width=40, height=6)
        scroll_1=ttk.Scrollbar(self.user_subframe,command=self.result_box2.yview)
        scroll_1.pack(side=tk.RIGHT,fill=tk.Y)
        self.result_box2.config(yscrollcommand=scroll_1.set)
        self.result_box2.pack(pady=3, padx=5)
        self.open_previous_ratings()

    def open_previous_ratings(self):
        """opens any previous ratings that the user made"""
        try:
            db=anydbm.open("ownratings.db","c")
            ratings=pk.loads(db[current_user])
            for meal, rating in ratings.items():
                meal_index=self.meals.index(meal)
                self.chosen_meals.append(meal_index)
                self.choice_box.insert(tk.END, "%s --> %s"%(meal, rating))
        except KeyError:
            db=anydbm.open("ownratings.db","c")
            db[current_user]=pk.dumps({})

    def get_user_ratings(self):
        """This method returns the meal, rating and any reviews that the user entered
           and then stores that information to the database by calling the method from
           the parent class. In addition it also populates the listbox with the user's
           current choice in ratings"""
        selected_meal=self.meals[self.box.current()]
        self.chosen_meals.append(self.box.current())
        meal_rating = self.scale.get()
        f_critics=anydbm.open("ownratings.db","c")
        if current_user in f_critics.keys():
            rate_and_rev = pk.loads(f_critics[str(current_user)])
            rate_and_rev[str(selected_meal)]= meal_rating
            f_critics[str(current_user)]=pk.dumps(rate_and_rev)
        else:
            # if not in critics database then add him in there
            db=anydbm.open("ownratings.db","c")
            user_ratings=dict()
            rate_rev=meal_rating
            user_ratings[str(selected_meal)]=rate_rev
            db[str(current_user)]=pk.dumps(user_ratings)
            db.close()
        self.choice_box.insert(tk.END, "%s --> %s"%(selected_meal, meal_rating))

    def remove_rating(self):
        """This method basically removes a meal rating that the user entered, as shown
           in the listbox containing all the ratings of the user"""
        try:
            meal_selection=self.choice_box.curselection()
            a=self.chosen_meals.pop(meal_selection[0])
            meal_to_pop=self.meals[a]
            self.choice_box.delete(self.choice_box.curselection())
            db = anydbm.open("ownratings.db","c")
            ratings=pk.loads(db[current_user])
            ratings.pop(meal_to_pop)
            db[current_user]=pk.dumps(ratings)  # update the database ratings
        except KeyError:
            pass

    def standard_reco(self):
        """This method is the command for the get standard recommendations button widget in the
           application. It uses the database to create a dictionary that will be used to feed into the
           get_recommendations function"""
        global current_user
        self.clear_result_box()
        self.clear_result_box2()
        food_ratings_dict=self.get_dict_from_database()
        if self.method == "userbased":
            sim_func=self.sim_dict[self.similarity]
            if current_user not in food_ratings_dict:
                self.result_box.insert(tk.END, "Please rate a couple of meals")
                return
            recommendations=getRecommendations(food_ratings_dict, current_user, sim_func)
            num_of_rec=self.num_recommendations
            self.result_box.insert(tk.END, "Similarity Score --> Recommendation\n")
            loop_range=int(num_of_rec.get('1.0','end-1c'))
            if loop_range>len(recommendations):
                loop_range=len(recommendations)
            if loop_range==0:
                self.result_box.insert(tk.END,"No recommendations found. Try rating more meals")
            for i in range(loop_range):
                sim_score=recommendations[i][0]  # similarity score
                rec=recommendations[i][1]  # recommended meal
                self.result_box.insert(tk.END, "%.2f --> %s\n"%(sim_score, rec))
            self.custom_reco()
        else:
            sim_func=self.sim_dict[self.similarity]
            if current_user not in food_ratings_dict:
                self.result_box.insert(tk.END, "Please rate a couple of meals")
                return
            num_of_rec=self.num_recommendations
            loop_range=int(num_of_rec.get('1.0','end-1c'))
            similar_items=calculateSimilarItems(food_ratings_dict)
            recommendations=getRecommendedItems(food_ratings_dict, similar_items, current_user)
            self.result_box.insert(tk.END, "Similarity Score --> Recommendation\n")
            if loop_range>len(recommendations):
                loop_range=len(recommendations)
            if loop_range==0:
                self.result_box.insert(tk.END,"No recommendations found. Try rating more meals")
            for i in range(loop_range):
                sim_score=recommendations[i][0]  # similarity score
                rec=recommendations[i][1]  # recommended meal
                self.result_box.insert(tk.END, "%.2f --> %s\n"%(sim_score, rec))
            self.custom_reco()


    def get_dict_from_database(self):
        """This method gets the correct dictionary representation from the database so as to use
           to feed into our recommendation functions"""
        self.db=anydbm.open(self.critics_database, "r")
        food_ratings_dict=dict()
        for critic in self.db:
            critic_data=pk.loads(self.db[critic])  # critics rating
            # but we only need the rating not the review of the critic at this point
            food_ratings_dict[critic]=critic_data
        # now to add original user to the food ratings dict
        user_db=anydbm.open("ownratings.db","c")
        if current_user in user_db:
            ratings=pk.loads(user_db[current_user])
            food_ratings_dict[current_user]=ratings
        return food_ratings_dict

    def custom_reco(self):
        """This method sets up the custom recommendation option
           on the user's choice of user based or item based recommendation"""
        if self.method=="userbased":
            self.clear_list_box()
            self.cus_label.config(text="Users similar to you", bg="purple")
            self.rb_label.config(text="User ratings (select a user on the left)", bg="brown")
            self.populate_listbox()
        if self.method=="itembased":
            self.clear_list_box()
            self.cus_label.config(text="Your Original Ratings", bg="orange")
            self.rb_label.config(text="Similar items (select an item on the left)", bg="blue")
            og_meals=self.choice_box.get(0, tk.END)
            og_meals =list(og_meals)
            self.all_meals = [x.split(" --> ") for x in og_meals]
            for meal, rating in self.all_meals:
                self.list_box.insert(tk.END, "%s --> %s" %(meal, rating))

    def clear_list_box(self):
        self.list_box.delete(0, tk.END)

    def populate_listbox(self):
        food_ratings_dict=self.get_dict_from_database()
        sim_func=self.sim_dict[self.similarity]
        top=topMatches(food_ratings_dict,current_user,5,sim_func)
        for score, person in top:
            self.list_box.insert(tk.END, "%.2f-%s" % (score,person))

    def view_func(self, val):
        """Once the user selects the users that are similar to them, the view_func will enable them to
           see other meals that the selected user also liked"""
        if self.method =="userbased":
            self.clear_result_box2()
            sel_user=self.list_box.get(self.list_box.curselection())  # selected user
            sel_user=str(sel_user.split("-")[1])
            user_details=pk.loads(self.db[sel_user])
            ratings_data={}
            # we need to sort the data in order to get the top meals from a user
            for meal, lst in user_details.items():
                ratings_data[lst]=meal
            sorted_ratings=ratings_data.items()
            sorted_ratings.sort(reverse=True)
            # now to put results in the resultbox
            self.result_box2.insert(tk.END, "%s also rated the following\n\n"%sel_user)
            for rating, meal in sorted_ratings:
                self.result_box2.insert(tk.END, "%s --> %s\n"%(meal, rating))
        else:
            self.find_similar_meals()

    def find_similar_meals(self):
        """using item based recommendation, the goal that this method tries to achieve is finding
           meals similar to the one that the user selects"""
        self.clear_result_box2()
        food_critics=self.get_dict_from_database()
        item_critics=transformPrefs(food_critics)  # reversed dictionary for item based recommendation
        sel_meal_ind=self.list_box.curselection()[0]
        selected_meal=self.meals[self.chosen_meals[sel_meal_ind]]
        sim_func=self.sim_dict[self.similarity]
        try:
            similar_meals=topMatches(item_critics,selected_meal,5, sim_func)
            self.result_box2.insert(tk.END, "The following meals are similar to %s\n\n" %selected_meal)
            for rating, meal in similar_meals:
                self.result_box2.insert(tk.END, "%s --> %.2f\n"%(meal, rating))
        except KeyError:
            self.result_box2.insert(tk.END,"The following meals are similar to %s\n\n" %selected_meal)

    def clear_result_box(self):
        # clears everything that is in the result box
        self.result_box.delete("1.0","end-1c")

    def clear_result_box2(self):
        self.result_box2.delete("1.0", "end-1c")

    # the following 5 methods are made as commands for radio buttons
    def euclidean_method(self):
        self.similarity="euclidean"

    def pearson_method(self):
        self.similarity="pearson"

    def jaccard_method(self):
        self.similarity="jaccard"

    def user_based_sim(self):
        self.method="userbased"

    def item_based_sim(self):
        self.method="itembased"


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(0,0)
    Recommender(root)
    root.mainloop()



