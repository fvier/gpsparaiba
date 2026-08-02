#!/usr/bin/env python3
import sys
from apps import create_app, db
from apps.config import config_dict
from apps.pages.models import User

app = create_app(config_dict['Production'])

def add_user(email, password, username=None):
    with app.app_context():
        db.create_all()
        if not username:
            username = email.split('@')[0]
        
        user = User.query.filter((User.email == email) | (User.username == username)).first()
        if user:
            user.set_password(password)
            db.session.commit()
            print(f"✅ Usuário {email} atualizado com nova senha!")
        else:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            print(f"🎉 Usuário {email} criado com sucesso!")

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        email_input = sys.argv[1]
        pass_input = sys.argv[2]
        add_user(email_input, pass_input)
    else:
        raise SystemExit('Uso: python create_user.py EMAIL SENHA')
