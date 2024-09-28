import difflib

from flask import Flask, render_template, request, jsonify
from sklearn.neighbors import NearestNeighbors
import pickle
from  account_manager import  account_manager

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

    if user_input not in pivot_table.index:
        return render_template("recommend.html",data=[])
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

    return render_template('recommend.html',data=data_list)


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/signin", methods=['POST'])
def sign_in():
    acc_mng=account_manager()
    name= request.form.get("username")
    password=request.form.get("password")
    return str(acc_mng.sign_in(name,password))


@app.route('/get_book_suggestions')
def get_book_suggestions():
    query = request.args.get('query', '').strip()
    books = [pivot_table['index']]
    # Create a list of (book_title, score) tuples
    results = [(book, difflib.SequenceMatcher(None, query.lower(), book.lower()).ratio()) for book in books]
    # Sort results based on the score in descending order
    results.sort(key=lambda x: x[1], reverse=True)

    # Extract the book titles from the sorted results
    sorted_books = [book for book, score in results if score > 0]  # Only include matches with a positive score

    return jsonify(sorted_books)

@app.route("/signup",methods=['POST'])
def sign_up():
    acc_mng=account_manager()
    name= request.form.get("name")
    password=request.form.get("password")
    return str(acc_mng.sign_up(name,password))

@app.route("/signuppage")
def sign_up_page():
    return render_template("sign_up_page.html")




@app.route('/add_comment', methods=['POST'])
def add_comment():
    comments=[]
    comment = request.json.get('comment')
    if comment:
        comments.append(comment)
        print(comment)
        return jsonify({'success': True})

    return jsonify({'success': False})

if __name__ == '__main__':
    app.run(debug=True)
