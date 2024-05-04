import pandas as pd
import warnings
import neattext.functions as nfx
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def process_data():
    warnings.filterwarnings('ignore')

    data = pd.read_csv('udemy_courses.csv')
    #removing duplicate records
    if(data.duplicated().any()):
        data = data.drop_duplicates()

    #removing special characters and stopwords from the title
    data['course_title'] = data['course_title'].apply(nfx.remove_stopwords)
    data['course_title'] = data['course_title'].apply(nfx.remove_special_characters)
    data['title_subject'] = data['course_title'] + data['subject']

    return data

def similarity_calc(data):
    cv = CountVectorizer(max_features=3000)
    vectors = cv.fit_transform(data['title_subject']).toarray() #converting to vectors
    similarity = cosine_similarity(vectors) #calculating cosine similarity among every pair in the dataset
    return similarity

def get_recommendations(course):
    data = process_data()
    similarity = similarity_calc(data)

    course_index = data[data['course_title'].str.contains(course)].index[0] #getting  the index of the course input by the user
    sim_score = similarity[course_index]    #getting the similarity vector of the corresponding course
    course_list = sorted(enumerate(sim_score), reverse=True, key=lambda x:x[1])[1:11] #finding top 10 similar courses
    course_names = []
    for i in course_list:
        print(data.iloc[i[0]]['course_title'])
        course_names.append(data.iloc[i[0]]['course_title']) #getting the names of the top 10 courses based on their index
    return course_names