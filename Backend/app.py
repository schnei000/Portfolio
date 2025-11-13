from flask import Flask, render_template
from Backend.models import db, Project, Skill
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Initialisation de notre application avec Flask
app = Flask(__name__,
          template_folder=os.path.join(basedir, '../Frontend/templates'),
          static_folder=os.path.join(basedir, '../Frontend/static'))

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la base de données avec l'application Flask
db.init_app(app)


def add_initial_data():
    """Ajoute les données initiales si les tables sont vides"""
    if not Skill.query.first():
        skills_data = [
            {'name': 'HTML', 'percentage': 90},
            {'name': 'CSS', 'percentage': 80},
            {'name': 'JavaScript', 'percentage': 80},
            {'name': 'Backend (Python/Flask)', 'percentage': 85},
            {'name': 'SQL', 'percentage': 80},
            {'name': 'React', 'percentage': 75}
        ]
        for skill_data in skills_data:
            db.session.add(Skill(**skill_data))
        db.session.commit()

    #ajout du projet Elib
    if not Project.query.first():
        elib_project = Project(
            name="eLib - Bibliothèque Électronique", 
            description="Une bibliothèque électronique pour la gestion et la consultation de livres numériques, développée en Python avec Flask.", 
            url="https://capstone-frontend-elib.vercel.app/"
        )
        db.session.add(elib_project)
        db.session.commit()


# Créer les tables au démarrage de l'application
with app.app_context():
    db.create_all()
    add_initial_data()


# Route Accueil
@app.route('/')
def home():
    projects = Project.query.all()
    skills = Skill.query.order_by(Skill.percentage.desc()).all()

    about_me = "Je suis St Fleur Walker, Développeur Full Stack passionné par la tech et le code.\nAprès deux ans en sciences informatiques à l'Université INUKA, j'ai poursuivi ma formation au bootcamp Akademi, en partenariat avec l'Université Quisqueya, où j'ai suivi un programme intensif en Software Engineering.\nJ'y ai appris et pratiqué des technologies comme HTML, CSS, JavaScript, React, Python et SQL, en construisant des projets concrets et modernes.\nAujourd'hui, je continue d'évoluer, avec une seule idée en tête : créer des solutions web utiles, performantes et centrées sur l'expérience utilisateur."
    contact_info = {
        "email": "walkerstfleur007@gmail.com",
        "github": "https://github.com/schnei000",
        "linkedin": "https://www.linkedin.com/in/walker-st-fleur-160084355/",
    }

    return render_template('index.html', 
                           projects=projects, 
                           skills=skills,
                           about_me=about_me,
                           contact_info=contact_info)


if __name__ == '__main__':
    app.run(port=5000, debug=True)