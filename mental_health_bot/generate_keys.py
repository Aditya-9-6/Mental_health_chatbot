import streamlit_authenticator as stauth

hashed_passwords = stauth.Hasher(['abc', 'def']).generate()
print(hashed_passwords)
