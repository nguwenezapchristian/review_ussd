import secrets
from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv
from models import Gov_institute, Hospitals, Gov_review, Hosp_review, db
import urllib.parse
import os

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
    "institution_type_prompt": {
        "english": "CON Select institution type:\n1. Hospitals\n2. Government Offices\n",
        "kinyarwanda": "CON Hitamo ubwoko bw'ikigo:\n1. Ibitaro\n2. Ibiro bya Leta\n",
        "swahili": "CON Chagua aina ya taasisi:\n1. Hospitali\n2. Ofisi za Serikali\n"
    },
    "rate_prompt": {
        "english": "CON Rate {} (1-5):\n",
        "kinyarwanda": "CON Tanga amanota ku {} (1-5):\n",
        "swahili": "CON Pima huduma ya {} (1-5):\n"
    },
    "thank_you": {
        "english": "END Thank you for rating {}\n",
        "kinyarwanda": "END Murakoze gutanga amanota ku {}\n",
        "swahili": "END Asante kwa kupima huduma ya {}\n"
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
            response = translations["institution_type_prompt"][language]
        elif len(text_array) == 2:
            if text_array[1] == "1":
                response = get_institutions("hospital", language)
            elif text_array[1] == "2":
                response = get_institutions("government_office", language)
            else:
                response = "END Invalid input\n"
        elif len(text_array) == 3:
            institution_type = "hospital" if text_array[1] == "1" else "government_office"
            institution_name = get_institution_name(institution_type, text_array[2])
            if institution_name:
                response = translations["rate_prompt"][language].format(institution_name)
            else:
                response = "END Invalid input\n"
        elif len(text_array) == 4:
            institution_type = "hospital" if text_array[1] == "1" else "government_office"
            institution_name = get_institution_name(institution_type, text_array[2])
            if institution_name:
                # Save the rating to the database
                save_rating(institution_type, text_array[2], text_array[3])
                response = translations["thank_you"][language].format(institution_name)
            else:
                response = "END Invalid input\n"
    elif text_array[0] == "2":
        language = "kinyarwanda"
        if len(text_array) == 1:
            response = translations["institution_type_prompt"][language]
        elif len(text_array) == 2:
            if text_array[1] == "1":
                response = get_institutions("hospital", language)
            elif text_array[1] == "2":
                response = get_institutions("government_office", language)
            else:
                response = "END Invalid input\n"
        elif len(text_array) == 3:
            institution_type = "hospital" if text_array[1] == "1" else "government_office"
            institution_name = get_institution_name(institution_type, text_array[2])
            if institution_name:
                response = translations["rate_prompt"][language].format(institution_name)
            else:
                response = "END Invalid input\n"
        elif len(text_array) == 4:
            institution_type = "hospital" if text_array[1] == "1" else "government_office"
            institution_name = get_institution_name(institution_type, text_array[2])
            if institution_name:
                # Save the rating to the database
                save_rating(institution_type, text_array[2], text_array[3])
                response = translations["thank_you"][language].format(institution_name)
            else:
                response = "END Invalid input\n"
    elif text_array[0] == "3":
        language = "swahili"
        if len(text_array) == 1:
            response = translations["institution_type_prompt"][language]
        elif len(text_array) == 2:
            if text_array[1] == "1":
                response = get_institutions("hospital", language)
            elif text_array[1] == "2":
                response = get_institutions("government_office", language)
            else:
                response = "END Invalid input\n"
        elif len(text_array) == 3:
            institution_type = "hospital" if text_array[1] == "1" else "government_office"
            institution_name = get_institution_name(institution_type, text_array[2])
            if institution_name:
                response = translations["rate_prompt"][language].format(institution_name)
            else:
                response = "END Invalid input\n"
        elif len(text_array) == 4:
            institution_type = "hospital" if text_array[1] == "1" else "government_office"
            institution_name = get_institution_name(institution_type, text_array[2])
            if institution_name:
                # Save the rating to the database
                save_rating(institution_type, text_array[2], text_array[3])
                response = translations["thank_you"][language].format(institution_name)
            else:
                response = "END Invalid input\n"
    else:
        response = "END Invalid input\n"

    return response

def get_institutions(institution_type, language):
    if institution_type == "hospital":
        institutions = Hospitals.query.all()
        prompt = "CON Select a hospital:\n"
    elif institution_type == "government_office":
        institutions = Gov_institute.query.all()
        prompt = "CON Select a government office:\n"

    for idx, institution in enumerate(institutions, start=1):
        prompt += f"{idx}. {institution.name}\n"

    return prompt

def get_institution_name(institution_type, index):
    index = int(index) - 1
    if institution_type == "hospital":
        institutions = Hospitals.query.all()
    elif institution_type == "government_office":
        institutions = Gov_institute.query.all()

    if 0 <= index < len(institutions):
        return institutions[index].name
    return None

def save_rating(institution_type, institution_index, rating):
    institution_index = int(institution_index) - 1
    rating = int(rating)

    if institution_type == "hospital":
        institutions = Hospitals.query.all()
        if 0 <= institution_index < len(institutions):
            institution_id = institutions[institution_index].id
            review = Hosp_review(institution_id=institution_id, rating=rating)
    elif institution_type == "government_office":
        institutions = Gov_institute.query.all()
        if 0 <= institution_index < len(institutions):
            institution_id = institutions[institution_index].id
            review = Gov_review(institution_id=institution_id, rating=rating)

    try:
        db.session.add(review)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

@app.route('/register_institution', methods=['POST'])
def register_institution():
    """The route for posting institutions in the db."""
    try:
        data = request.get_json()
        if not data or not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400

        name = data.get('name')
        description = data.get('description')

        institution_type = data.get('type', 'hospital').lower()
        if institution_type == 'hospital':
            institution = Hospitals(name=name, description=description)
        elif institution_type == 'government_office':
            institution = Gov_institute(name=name, description=description)
        else:
            return jsonify({'error': 'Invalid institution type'}), 400

        db.session.add(institution)
        db.session.commit()

        return jsonify({'message': f'{institution_type.capitalize()}: {name} registered successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/retrieve_institutions', methods=['GET'])
def retrieve_institutions():
    """The route for retrieving all institutions from the db."""
    try:
        hospitals = Hospitals.query.all()
        government_offices = Gov_institute.query.all()

        institutions_list = []
        for hospital in hospitals:
            institutions_list.append({
                'id': hospital.id,
                'name': hospital.name,
                'description': hospital.description,
                'type': 'hospital'
            })
        for gov_office in government_offices:
            institutions_list.append({
                'id': gov_office.id,
                'name': gov_office.name,
                'description': gov_office.description,
                'type': 'government_office'
            })

        return jsonify({'institutions': institutions_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/register_review', methods=['POST'])
def register_review():
    """The route for posting reviews in the db."""
    try:
        data = request.get_json()
        if not data or not data.get('institution_id') or not data.get('rating'):
            return jsonify({'error': 'Institution ID and Rating are required'}), 400

        institution_id = data.get('institution_id')
        rating = data.get('rating')

        institution = Hospitals.query.filter_by(id=institution_id).first() or Gov_institute.query.filter_by(id=institution_id).first()
        if not institution:
            return jsonify({'error': 'Invalid institution ID'}), 400

        if isinstance(institution, Hospitals):
            review = Hosp_review(institution_id=institution_id, rating=rating)
        else:
            review = Gov_review(institution_id=institution_id, rating=rating)

        db.session.add(review)
        db.session.commit()

        return jsonify({'message': f'Review for Institution ID: {institution_id} registered successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard')
def dashboard():
    return render_template('review_ussd.html')

@app.route('/register_institution')
def register_inst():
    return render_template('institution_reg.html')

@app.route('/retrieve_reviews', methods=['GET'])
def retrieve_reviews():
    """The route for retrieving all reviews from the db."""
    try:
        hosp_reviews = Hosp_review.query.all()
        gov_reviews = Gov_review.query.all()

        reviews_list = []
        for review in hosp_reviews:
            reviews_list.append({
                'review_id': review.id,
                'institution_id': review.institution_id,
                'rating': review.rating,
                'review_date': review.review_date,
                'type': 'hospital'
            })
        for review in gov_reviews:
            reviews_list.append({
                'review_id': review.id,
                'institution_id': review.institution_id,
                'rating': review.rating,
                'review_date': review.review_date,
                'type': 'government_office'
            })

        return jsonify({'reviews': reviews_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create all tables based on the defined models
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
