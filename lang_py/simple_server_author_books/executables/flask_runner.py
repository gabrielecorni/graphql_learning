from flask import Flask
from flask_graphql import GraphQLView
from data.dummy_data_wrapper import get_schema


app = Flask(__name__)


@app.route('/')
def homepage():
    html_home = """
    <html>
        <head>
            <title>GraphQL - Demo Server</title>
        </head>
        <body>
            <h1>GraphQL - Demo Server</h1>
            <p>
                Hello, World!
                <br>
                Let's learn GraphQL together :)
            </p>
            <p>
                <a href="/graphql"><b>Let's go</b></a>.
            </p>
        </body>
    </html>
    """
    return html_home


def run():
    schema = get_schema()
    app.debug = True
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True
        )
    )
    app.run(host='0.0.0.0', port=5000)
