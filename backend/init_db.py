from werkzeug.security import generate_password_hash

from backend.app import create_app
from backend.extensions import db
from backend.models import School, User


def seed_data():
    app = create_app()

    with app.app_context():
        db.create_all()

        school = db.session.query(School).filter_by(name="Test Okul").first()
        if not school:
            school = School(name="Test Okul", address="Istanbul")
            db.session.add(school)
            db.session.commit()

        admin = db.session.query(User).filter_by(email="admin@test.com").first()
        if not admin:
            admin = User(
                email="admin@test.com",
                password_hash=generate_password_hash("Test123!"),
                role="system_admin",
                school_id=None
            )
            db.session.add(admin)
        else:
            admin.password_hash = generate_password_hash("Test123!")
            admin.role = "system_admin"
            admin.school_id = None

        teacher = db.session.query(User).filter_by(email="teacher@test.com").first()
        if not teacher:
            teacher = User(
                email="teacher@test.com",
                password_hash=generate_password_hash("Test123!"),
                role="teacher",
                school_id=school.id
            )
            db.session.add(teacher)
        else:
            teacher.password_hash = generate_password_hash("Test123!")
            teacher.role = "teacher"
            teacher.school_id = school.id

        school_admin = db.session.query(User).filter_by(email="schooladmin@test.com").first()
        if not school_admin:
            school_admin = User(
                email="schooladmin@test.com",
                password_hash=generate_password_hash("Test123!"),
                role="school_admin",
                school_id=school.id
            )
            db.session.add(school_admin)
        else:
            school_admin.password_hash = generate_password_hash("Test123!")
            school_admin.role = "school_admin"
            school_admin.school_id = school.id

        db.session.commit()
        print("Veritabanı dolduruldu.")


if __name__ == "__main__":
    seed_data()