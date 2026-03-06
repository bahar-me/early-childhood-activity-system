from backend.extensions import db
from backend.app import create_app
from backend.models.user import User

app = create_app()

def init_db():
    with app.app_context():

        # tüm modelleri oluştur
        db.create_all()

        print("✅ Database tables created")

        # örnek admin oluştur
        if not User.query.filter_by(email="admin@example.com").first():

            admin = User(
                username="admin",
                email="admin@example.com",
                password="admin123",
                role="system_admin"
            )

            db.session.add(admin)
            db.session.commit()

            print("✅ Admin user created")

        else:
            print("Admin already exists")


if __name__ == "__main__":
    init_db()