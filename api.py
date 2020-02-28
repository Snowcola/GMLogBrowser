from flask import Flask
from flask_graphql import GraphQLView

from parse import Session as session
from logschema import schema # Department
from flask_cors import CORS

app = Flask(__name__)
app.debug = True
CORS(app)
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)
'''
@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()
'''
if __name__ == '__main__':
    app.run()