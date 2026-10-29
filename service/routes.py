######################################################################
# REST API ROUTES
######################################################################

from flask import jsonify, request, abort, make_response
from flask_api import status

from service import app
from service.models import Account


######################################################################
# GET INDEX
######################################################################

@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(name="Account REST API Service", version="1.0"),
        status.HTTP_200_OK,
    )


@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify(status="OK"), status.HTTP_200_OK


######################################################################
# CREATE A NEW ACCOUNT
######################################################################

@app.route("/accounts", methods=["POST"])
def create_accounts():
    """Creates an Account"""
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    message = account.serialize()
    location_url = "/"
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


######################################################################
# LIST ALL ACCOUNTS
######################################################################

@app.route("/accounts", methods=["GET"])
def list_accounts():
    """Returns all accounts"""
    app.logger.info("Request to list all accounts")
    accounts = Account.all()
    results = [account.serialize() for account in accounts]
    return jsonify(results), status.HTTP_200_OK


######################################################################
# READ AN ACCOUNT
######################################################################

@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_accounts(account_id):
    """Returns an account by ID"""
    app.logger.info("Request to read account with id %s", account_id)
    account = Account.find(account_id)
    if not account:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Account with id '{account_id}' was not found.",
        )
    return jsonify(account.serialize()), status.HTTP_200_OK


######################################################################
# UPDATE AN EXISTING ACCOUNT
######################################################################

# UPDATE endpoint will be implemented in the next task.
@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    """Updates an existing account"""
    app.logger.info("Request to update account with id %s", account_id)

    account = Account.find(account_id)
    if not account:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Account with id '{account_id}' was not found.",
        )

    check_content_type("application/json")
    account.deserialize(request.get_json())
    account.update()

    return jsonify(account.serialize()), status.HTTP_200_OK

######################################################################
# DELETE AN ACCOUNT
@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    """Deletes an account"""
    app.logger.info("Request to delete account with id %s", account_id)

    account = Account.find(account_id)
    if not account:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Account with id '{account_id}' was not found.",
        )

    account.delete()
    return "", status.HTTP_204_NO_CONTENT
######################################################################

# DELETE endpoint will be implemented in the next task.


######################################################################
# UTILITY FUNCTIONS
######################################################################

def check_content_type(media_type):
    """Checks that the request content type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
