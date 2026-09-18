from app import create_app
from app.models.user import User
from extensions import db


def test_user_model_password_hash():
    app = create_app()
    with app.app_context():
        user = User(full_name="Test User", email="test@example.com")
        user.set_password("secret123")
        assert user.check_password("secret123") is True
        assert user.check_password("wrong") is False


def test_db_creates_tables():
    app = create_app()
    with app.app_context():
        db.create_all()
        assert User.query.count() >= 0
