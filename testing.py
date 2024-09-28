from Tools.scripts.make_ctype import method
from flask import Flask,render_template,request
from sklearn.neighbors import NearestNeighbors
import pickle

popular_df=pickle.load(open('popular.pkl','rb'))
pivot_table=pickle.load(open('pt.pkl','rb'))

books=pickle.load(open('books.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html",
                           book_name=list(popular_df["Book-Title"].values),
                           author=list(popular_df["Book-Author"].values),
                           image=list(popular_df["Image-URL-M"].values),
                           votes=list(popular_df["Num-Rating"].values),
                           rating=list(popular_df["Avg-Rating"].values))


@app.route('/recommend')
def recommend_ui():
    return render_template("recommend.html")




popular_df=pickle.load(open('popular.pkl','rb'))
pivot_table=pickle.load(open('pt.pkl','rb'))

books=pickle.load(open('books.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html",
                           book_name=list(popular_df["Book-Title"].values),
                           author=list(popular_df["Book-Author"].values),
                           image=list(popular_df["Image-URL-M"].values),
                           votes=list(popular_df["Num-Rating"].values),
                           rating=list(popular_df["Avg-Rating"].values))


@app.route('/recommend')
def recommend_ui():
    return render_template("recommend.html")


@app.route('/recommend_books',methods=['POST'])
def recommend_books():
    user_input=request.form.get("user_input")
    n_neighbors = 6
    # Initialize the NearestNeighbors model
    model = NearestNeighbors(algorithm="brute", metric="cosine")

    # Fit the model on the pivot_table
    model.fit(pivot_table.values)

    # Get the index of the book in the pivot_table
    book_index = pivot_table.index.get_loc(user_input)

    # Reshape the data for the selected book to match the input format for the model
    distances, indices = model.kneighbors(pivot_table.iloc[book_index, :].values.reshape(1, -1),
                                          n_neighbors=n_neighbors)

    # Fetch the book titles based on the indices returned by the model
    recommended_books = [pivot_table.index[indices.flatten()[i]] for i in
                         range(1, len(indices.flatten()))]  # Skip the first one

    data_list = []
    for book in recommended_books:
        # Find the corresponding book details in the 'books' DataFrame
        book_info = books[books["Book-Title"] == book].iloc[0]  # Assuming there's at least one match
        author = book_info["Book-Author"]
        image = book_info["Image-URL-M"]
        data_list.append(list([book, author, image]))

    return data_list


if __name__ == '__main__':
    app.run(debug=True)

