import math
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import numpy as np
import datetime

cred_file = '/Users/wwick/ses/CapitalOne-SES-Hackathon/cashback/project/firestore.json'
cred = credentials.Certificate(cred_file)
firebase_admin.initialize_app(cred, {
  'projectId': 'ses-hackathon-c6cf5',
})

db = firestore.client()
users_ref = db.collection(u'users')

def monthToQuarter(month):
    return (math.ceil(month / 3) - 1) 

def rewardsEarned(transaction, card):
    rewards = card['rewards']
    reward_rate = rewards['other']
    if 'rotation' in rewards:
        quarter = monthToQuarter(transaction['date'].month)
        if (rewards['rotation'][quarter] == transaction['category']):
            reward_rate = rewards['rotation_value']
    if transaction['category'] in rewards:
        reward_rate = rewards[transaction['category']]
    return reward_rate * transaction['amount']

def bestCard(category, user):
    user_cards = db.collection(u'users').document(user).get().to_dict()[u'cards']
    cards = db.collection(u'cards').stream()
    best_option = {'points': 0, 'id':0, 'name':''}
    date = datetime.datetime.now()
    transaction = {'amount': 1, 'date': date, 'category': category}
    for card in cards:
        if card.id in user_cards:
            card_data = card.to_dict()
            points = rewardsEarned(transaction, card_data)
            if (points > best_option['points']):
                best_option['points'] = points
                best_option['id'] = card.id 
                best_option['name'] = card_data['name']
    return best_option

def maxPoints(transaction, candidate_cards):
    best_option = 0
    for card in candidate_cards.values():
        best_option = max(rewardsEarned(transaction, card), best_option)
    return best_option

def newCard(user):
    transactions = db.collection(u'users').document(user).collection(u'transactions').stream()
    cards = db.collection(u'cards').stream()
    user_cards = db.collection(u'users').document(user).get().to_dict()[u'cards']
    candidate_cards = {}
    today = datetime.date.today()
    for card in cards:
        if card.id not in user_cards:
            candidate_cards[card.id] = card.to_dict()
            candidate_cards[card.id]['benefit'] = 0
    for transaction in transactions:
        transaction = transaction.to_dict()
        date = transaction['date'].date()
        if (today - date < datetime.timedelta(weeks=12)):
            current_rewards = maxPoints(transaction, candidate_cards)
            for id in candidate_cards:
                delta_rewards = rewardsEarned(transaction, candidate_cards[id]) - current_rewards
                if (delta_rewards > 0):
                    candidate_cards[id]['benefit'] += delta_rewards
    for id in candidate_cards:
        candidate_cards[id]['benefit'] /= 100
        candidate_cards[id]['benefit'] *= 8
        candidate_cards[id]['benefit'] += candidate_cards[id]['bonus'] - candidate_cards[id]['intro'] - candidate_cards[id]['annual']
    sorted_cards = []
    for key, value in sorted(candidate_cards.items(), key=lambda card: card[1]['benefit'], reverse=True):
        sorted_cards.append([key, value])
    return sorted_cards

if __name__ == '__main__':check
    new_cards = newCard('Alice')
    print(new_cards)
    best_card = bestCard('restaurant', 'Alice')
    print(best_card)
