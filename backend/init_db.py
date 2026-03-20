from werkzeug.security import generate_password_hash

from backend.app import create_app
from backend.extensions import db
from backend.models import School, User


def seed_data():
    app = create_app()

    with app.app_context():
        db.create_all()

        school = School.query.filter_by(name="Test School").first()
        if not school:
            school = School(name="Test School", address="Istanbul")
            db.session.add(school)
            db.session.commit()

        admin = User.query.filter_by(email="admin@test.com").first()
        if not admin:
            admin = User(
                email="admin@test.com",
                password_hash=generate_password_hash("123456"),
                role="system_admin",
                school_id=None
            )
            db.session.add(admin)

        teacher = User.query.filter_by(email="teacher@test.com").first()
        if not teacher:
            teacher = User(
                email="teacher@test.com",
                password_hash=generate_password_hash("123456"),
                role="teacher",
                school_id=school.id
            )
            db.session.add(teacher)
        else:
            teacher.password_hash = generate_password_hash("123456")
            teacher.role = "teacher"
            teacher.school_id = school.id

        school_admin = User.query.filter_by(email="schooladmin@test.com").first()
        if not school_admin:
            school_admin = User(
                email="schooladmin@test.com",
                password_hash=generate_password_hash("123456"),
                role="school_admin",
                school_id=school.id
            )
            db.session.add(school_admin)
        else:
            school_admin.password_hash = generate_password_hash("123456")
            school_admin.role = "school_admin"
            school_admin.school_id = school.id

        db.session.commit()
        print("Database seeded successfully.")


if __name__ == "__main__":
    seed_data()