from flask import Flask
from flask import request
#import ipdb
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
