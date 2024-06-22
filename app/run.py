import secrets
from flask import Flask, jsonify
from dotenv import load_dotenv
from models import Institution, Review, db
from flask import request
import urllib.parse

import os  # Import the os module

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Generate a random secret key

# Get the Database credentials from the environment variable.
db_username = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_port = os.getenv('DB_PORT')
print("password: ", db_password)
print("username: ", db_username)
print("host: ", db_host)

# URL-encode the password
encoded_password = urllib.parse.quote_plus(db_password)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{db_username}:{encoded_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

translations = {
    "language_prompt": {
        "english": "CON Select language / Hitamo ururimi / Chagua lugha:\n1. English\n2. Kinyarwanda\n3. Swahili\n",
        "kinyarwanda": "CON Hitamo ururimi:\n1. Icyongereza\n2. Ikinyarwanda\n3. Kiswahili\n",
        "swahili": "CON Chagua lugha:\n1. Kiingereza\n2. Kinyarwanda\n3. Kiswahili\n"
    },
    "institution_prompt": {
        "english": "CON Select an institution:\n1. Hospital A\n2. Government Office B\n",
        "kinyarwanda": "CON Hitamo ikigo:\n1. Ibitaro A\n2. Ibiro bya Leta B\n",
        "swahili": "CON Chagua taasisi:\n1. Hospitali A\n2. Ofisi ya Serikali B\n"
    },
    "rate_prompt": {
        "english": {
            "1": "CON Rate Hospital A (1-5):\n",
            "2": "CON Rate Government Office B (1-5):\n"
        },
        "kinyarwanda": {
            "1": "CON Tanga amanota ku Bitaro A (1-5):\n",
            "2": "CON Tanga amanota ku Biro bya Leta B (1-5):\n"
        },
        "swahili": {
            "1": "CON Pima huduma ya Hospitali A (1-5):\n",
            "2": "CON Pima huduma ya Ofisi ya Serikali B (1-5):\n"
        }
    },
    "thank_you": {
        "english": {
            "1": "END Thank you for rating Hospital A\n",
            "2": "END Thank you for rating Government Office B\n"
        },
        "kinyarwanda": {
            "1": "END Murakoze gutanga amanota ku Bitaro A\n",
            "2": "END Murakoze gutanga amanota ku Biro bya Leta B\n"
        },
        "swahili": {
            "1": "END Asante kwa kupima huduma ya Hospitali A\n",
            "2": "END Asante kwa kupima huduma ya Ofisi ya Serikali B\n"
        }
    }
}


@app.route('/ussd', methods=['POST'])
def ussd():
    session_id = request.values.get("sessionId")
    service_code = request.values.get("serviceCode")
    phone_number = request.values.get("phoneNumber")
    text = request.values.get("text")

    text_array = text.split('*')
    response = ""

    if text == "":
        response = translations["language_prompt"]["english"]
    elif text_array[0] == "1":
        language = "english"
        if len(text_array) == 1:
            response = translations["institution_prompt"][language]
        elif len(text_array) == 2:
            response = translations["rate_prompt"][language].get(text_array[1], "END Invalid input\n")
        elif len(text_array) == 3:
            response = translations["thank_you"][language].get(text_array[1], "END Invalid input\n")
    elif text_array[0] == "2":
        language = "kinyarwanda"
        if len(text_array) == 1:
            response = translations["institution_prompt"][language]
        elif len(text_array) == 2:
            response = translations["rate_prompt"][language].get(text_array[1], "END Invalid input\n")
        elif len(text_array) == 3:
            response = translations["thank_you"][language].get(text_array[1], "END Invalid input\n")
    elif text_array[0] == "3":
        language = "swahili"
        if len(text_array) == 1:
            response = translations["institution_prompt"][language]
        elif len(text_array) == 2:
            response = translations["rate_prompt"][language].get(text_array[1], "END Invalid input\n")
        elif len(text_array) == 3:
            response = translations["thank_you"][language].get(text_array[1], "END Invalid input\n")
    else:
        response = "END Invalid input\n"

    return response
@app.route('/register_institution', methods=['POST'])
def register_institution():
    """The route for posting institutions in the db."""
    try:
        # Get the institution name and description from the request
        data = request.get_json()
        if not data or not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400

        name = data.get('name')
        description = data.get('description')

        # Create a new Institution object
        institution = Institution(name=name, description=description)

        # Add the Institution object to the database
        db.session.add(institution)
        db.session.commit()

        return jsonify({'message': f'Institution: {name} registered successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/retrieve_institutions', methods=['GET'])
def retrieve_institutions():
    """The route for retrieving all institutions from the db."""
    try:
        # Get all institutions from the database
        institutions = Institution.query.all()
        print(institutions)
        print(type(institutions))

        # Create a list of dictionaries containing the institutions
        institutions_list = []
        for institution in institutions:
            institution_dict = {
                'id': institution.id,
                'name': institution.name,
                'description': institution.description
            }
            institutions_list.append(institution_dict)

        return jsonify({'institutions': institutions_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/register_review', methods=['POST'])
def register_review():
    """The route for posting reviews in the db."""
    try:
        # Get the review details from the request
        data = request.get_json()
        if not data or not data.get('institution_id') or not data.get('rating'):
            return jsonify({'error': 'Institution ID and Rating are required'}), 400

        institution_id = data.get('institution_id')
        rating = data.get('rating')
        institution_name = Institution.query.filter_by(id=institution_id).first().name

        # Create a new Review object
        review = Review(institution_id=institution_id, rating=rating)

        # Add the Review object to the database
        db.session.add(review)
        db.session.commit()

        return jsonify({'message': f'Review for Institution ID: {institution_id}  and name: {institution_name}registered successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/retrieve_reviews', methods=['GET'])
def retrieve_reviews():
    """The route for retrieving all reviews from the db."""
    try:
        # Get all reviews from the database
        reviews = Review.query.all()

        # Create a list of dictionaries containing the reviews
        reviews_list = []
        for review in reviews:
            review_dict = {
                'review_id': review.review_id,
                'institution_id': review.institution_id,
                'rating': review.rating,
                'review_date': review.review_date
            }
            reviews_list.append(review_dict)

        return jsonify({'reviews': reviews_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Create all tables based on the defined models
with app.app_context():
    db.create_all() 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
