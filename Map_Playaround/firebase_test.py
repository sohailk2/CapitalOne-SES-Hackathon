import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore



cred = credentials.Certificate("ses-hackathon-c6cf5-firebase-adminsdk-mm5ur-ca18b38a5f.json")

# Use the application default credentials
# cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': 'ses-hackathon-c6cf5',
})

db = firestore.client()

users_ref = db.collection(u'cards')
docs = users_ref.stream()

for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))


def overallBestCard(transactionHistory):
    #so for each card calculate the best input card value then return the overall best card to match

    #track currentBest?
    currentBest = None
    cardDict = {}

    for transaction in transactionHistory:
        bestCard = bestCard()
        if not url in urls_d:
            cardDict[bestCard] = 1
        else:
            cardDict[bestCard] += 1

    

    
        