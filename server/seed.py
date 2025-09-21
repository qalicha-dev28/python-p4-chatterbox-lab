from app import app, db, Message

with app.app_context():
    db.drop_all()
    db.create_all()

    m1 = Message(body="Hello 👋", username="alice")
    m2 = Message(body="Hi there!", username="bob")
    m3 = Message(body="Welcome to Chatterbox 💬", username="carol")

    db.session.add_all([m1, m2, m3])
    db.session.commit()

    print("✅ Seeded 3 messages")
