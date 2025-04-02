from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    print(heroes)  # Debugging print to check data
    return jsonify([{"id": h.id, "name": h.name, "super_name": h.super_name} for h in heroes])


@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    return jsonify({
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "hero_powers": [{
            "id": hp.id,
            "hero_id": hp.hero_id,
            "power_id": hp.power_id,
            "strength": hp.strength,
            "power": {"id": hp.power.id, "name": hp.power.name, "description": hp.power.description}
        } for hp in hero.hero_powers]
    })

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([{"id": p.id, "name": p.name, "description": p.description} for p in powers])

@app.route('/powers/<int:id>', methods=['GET', 'PATCH'])
def power_details(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    
    if request.method == 'PATCH':
        data = request.json
        new_description = data.get('description')
        
        if not new_description or len(new_description) < 20:
            return jsonify({"errors": ["Description must be at least 20 characters long."]}), 400
        
        power.description = new_description
        db.session.commit()
    
    return jsonify({"id": power.id, "name": power.name, "description": power.description})


@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.json
    
    # Validate strength value
    if data['strength'] not in ["Strong", "Weak", "Average"]:
        return jsonify({"errors": ["Strength must be Strong, Weak, or Average."]}), 400
    
    # Check if hero and power exist
    hero = Hero.query.get(data['hero_id'])
    power = Power.query.get(data['power_id'])
    
    if not hero or not power:
        return jsonify({"errors": ["Hero or Power not found."]}), 404
    
    # Create new HeroPower
    new_hero_power = HeroPower(
        strength=data['strength'], hero_id=data['hero_id'], power_id=data['power_id']
    )
    db.session.add(new_hero_power)
    db.session.commit()
    
    # Return the newly created HeroPower
    return jsonify({
        "id": new_hero_power.id,
        "hero_id": new_hero_power.hero_id,
        "power_id": new_hero_power.power_id,
        "strength": new_hero_power.strength,
        "hero": {"id": hero.id, "name": hero.name, "super_name": hero.super_name},
        "power": {"id": power.id, "name": power.name, "description": power.description}
    }), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the tables are created
    app.run(debug=True)
