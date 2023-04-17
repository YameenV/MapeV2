import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import uuid

@st.cache_resource  
def loadDb():
    cred = credentials.Certificate("./mapekey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db

def getAllUsers(db):
    users = db.collection(u'user')
    users = users.get()
    return users

def addUser(db, username:str,aadhar_number, date_of_birth, address):
    doc_ref = db.collection(u'user').document(str(uuid.uuid4()))
    doc_ref.set({
        u'aadhar_number': str(aadhar_number),
        u'name': str(username),
        u'date_of_birth': str(date_of_birth),
        u'address': str(address),
    })
    print("$$$$$$$$$$$$$$$ user upadate ######################")

if __name__ == "__main__":
    loadDb()
    addUser()
