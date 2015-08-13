data-products
=============

# Good Morning Lecture:  Setting up a simple flask app.
Before we do anything, we must pip install flask. `pip install flask`  

Below is a starter file with the most simple flask app ever. What it does is sets the route to the current directory, and returns HTML code that says 'Something' as the h1 header.

```python
from flask import Flask
from flask import request
app = Flask(__name__)

# OUR HOME PAGE
#============================================
@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>title</title>
    </head>

  <body>
    <!-- page content -->
    <div>
        This is where text can live or pics or go anything your little heart wishes to be done.
    </div>
  </body>

</html>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969, debug=True)

```
** Above is copy and pasteable flask starter code. In your browser go to **    http://0.0.0.0:8080/

---

<br>
<br>
## This is how to make a new page at a new address.
This code makes a new page called `zack_rules`, and fills it up with content generated when that page is visited.
You do this via the `@app.route()` method.  and put your function below it.  

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1> Something </h1>'


# adding a new page
@app.route('/zack_rules')
def zack_rules():
    content = ''
    # generate some content
    for i in xrange(1000):
        content += 'zack rules! '
    return '<h1> Yo: %s </h1>' % content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
```
**Above is copy and pasteable example of how you can pass a list of strings into your webpage onto a page named 'zack_rules'.**
*http://0.0.0.0:8080/zack_rules*

---
<br>
<br>
<br>


# Basic human interaction a.k.a. using web forms.
Feeding user submitted data from your webpage into python, doing something with that data (like feed it into your model and make a prediction), then returning an output to the web.

So what we are doing here is using our flask app to interact with new information.  Here is the a simple example of how to setup a web page with a text box that the user can use to 'pass' information into your app.

To setup this 'pipeline' we are going to  build an html form in in actual html inside of our python app.  The form looks like this.  

```python

from flask import Flask
from flask import request
app = Flask(__name__)


# Form page to submit text
#============================================
# create page with a form on it
@app.route('/')
def submission_page():
    return '''
    <form action="/word_counter" method='POST' >
        <input type="text" name="user_input" />
        <input type="submit" />
    </form>
    '''


# My word counter app
#==============================================
# create the page the form goes to
@app.route('/word_counter', methods=['POST'] )
def word_counter():

    # get data from request form, the key is the name you set in your form
    data = request.form['user_input']

    # convert data from unicode to string
    data = str(data)

    # run a simple program that counts all the words
    dict_counter = {}
    for word in data.lower().split():
        if word not in dict_counter:
            dict_counter[word] = 1
        else:
            dict_counter[word] += 1
    total_words = len(dict_counter)

    # now return your results
    return 'Total words is %i, <br> dict_counter is: %s' % (total_words, dict_counter)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

```

---

# Required reading is in the welcome repo.  

##### Optional Reading

* Agile Data: p. 38-54
* [Pete Skomoroch: Data Exhaust](http://www.slideshare.net/pskomoroch/distilling-data-exhaust)
* [Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)


##### Other References

* [API design with Flask](http://blog.luisrei.com/articles/rest.html)
* [Flask + Bootstrap + Heroku](http://ryaneshea.com/lightweight-python-apps-with-flask-twitter-bootstrap-and-heroku)
* [Flask-restful](http://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful)
