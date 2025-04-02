from app import app, db
from models import Hero, Power, HeroPower

def seed_data():
    with app.app_context():
        # Clear existing data
        db.session.query(HeroPower).delete()
        db.session.query(Hero).delete()
        db.session.query(Power).delete()
        db.session.commit()

        # Create Heroes
        hero1 = Hero(name="Peter Parker", super_name="Spider-Man")
        hero2 = Hero(name="Bruce Wayne", super_name="Batman")
        hero3 = Hero(name="Clark Kent", super_name="Superman")

        # Create Powers
        power1 = Power(name="Web-slinging", description="Shoots strong, elastic webs")
        power2 = Power(name="Martial Arts", description="Expert hand-to-hand combat skills")
        power3 = Power(name="Flight", description="Can fly at incredible speeds")

        db.session.add_all([hero1, hero2, hero3, power1, power2, power3])
        db.session.commit()

        # Create HeroPowers
        hero_power1 = HeroPower(hero_id=hero1.id, power_id=power1.id, strength="Strong")
        hero_power2 = HeroPower(hero_id=hero2.id, power_id=power2.id, strength="Average")
        hero_power3 = HeroPower(hero_id=hero3.id, power_id=power3.id, strength="Strong")

        db.session.add_all([hero_power1, hero_power2, hero_power3])
        db.session.commit()

        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
