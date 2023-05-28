from flask import Flask, render_template, request, redirect, url_for, session
import wikipedia

app = Flask(__name__)
app.secret_key = 'IT@JCUA0Zr98j/3yXa R~XHH!jmN]LWX/,?RT'


@app.route('/')
def home():
    return render_template("Home.html", about_url=url_for('about'))


@app.route('/about')
def about():
    details = "The website is created for a Demo purpose."
    return render_template("Aboutus.html", details=details)


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        session['search_term'] = request.form['search']
        return redirect(url_for('results'))
    return render_template("Search.html")


@app.route('/results')
def results():
    search_term = session['search_term']
    page = get_page(search_term)
    return render_template("Results.html", page=page, title=page.title)


def get_page(search_term):
    try:
        page = wikipedia.page(search_term)
    except wikipedia.exceptions.PageError:
        page = wikipedia.page(wikipedia.random())
    except wikipedia.exceptions.DisambiguationError:
        page_titles = wikipedia.search(search_term)
        if page_titles[1].lower() == page_titles[0].lower():
            title = page_titles[2]
        else:
            title = page_titles[1]
        page = get_page(title)
    return page


if __name__ == '__main__':
    app.run()
