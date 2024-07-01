from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    new_user = User(
        username='victor', password='secret', email='victor@gmail.com'
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'victor'))

    assert user.username == 'victor'
