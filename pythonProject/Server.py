from flask import Flask, jsonify, request

# Flask constructor takes the name of
# current module (__name__) as argument.
import main
import requests

app = Flask(__name__)


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route("/")
def home():
    return main.readFile(r'H:\Final Project\בטיחות.pdf')


@app.route("/date")
def date():
    return main.getDate(main.readFile(r'H:\Final Project\בטיחות.pdf'))


@app.route("/number")
def getNumberProblems():
    return main.getNumberProblems()

@app.route('/api/FileUrls', methods=['GET'])
def get_file_urls():
    status = request.args.get('status')
    # Implement your logic to fetch URLs based on the status from the C# backend or any other data source
    urls = get_urls("Proccecing")
    return jsonify(urls)


def get_urls(status):
    url = f'http://localhost:5029/api/File/UrlsByStatus?status={status}'  # Replace with your Flask server URL
    params = {'status': status}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        urls = response.json()
        text = main.readFile(urls[0])
        # urls_string = '\n'.join(urls)
        return text


        # urls_string = '\n'.join(urls)
        # main.readFileAndNumberPage(urls_string)
    return 'An error occurred:', response.status_code


if __name__ == '__main__':
    app.run()
