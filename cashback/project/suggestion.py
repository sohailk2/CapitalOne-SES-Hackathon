import math
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import numpy as np
import datetime
import os

data = os.path.join(os.path.dirname(__file__), '../project/firestore.json')
cred = credentials.Certificate(data)

firebase_admin.initialize_app(cred, {
  'projectId': 'ses-hackathon-c6cf5',
})

db = firestore.client()
users_ref = db.collection(u'users')

def category_to_word(category_list):
    if category_list:
        for category in category_list:
            if category in category_map:
                return category_map[category]
    return "any store"

category_map = {
    'restaurant': 'restaurants',
    'gas_station': 'gas stations',
    'movie_theater': 'movie theaters',
    'grocery_or_supermarket': 'grocery stores',
    'walmart': 'Walmart',
    'lodging': 'hotels'
}

def monthToQuarter(month):
    return (math.ceil(month / 3) - 1) 

def rewardsEarned(transaction, card):
    rewards = card['rewards']
    reward_rate = rewards['other']
    if 'rotation' in rewards:
        quarter = monthToQuarter(transaction['date'].month)
        if (rewards['rotation'][quarter] == transaction['category']):
            reward_rate = rewards['rotation_value']
    if transaction['category']:
        for category in transaction['category']:
            if category in rewards:
                reward_rate = max(rewards[category], reward_rate)
    return reward_rate * transaction['amount']

# use for finding best card for a certain place
def bestCard(category, user):
    user_cards = db.collection(u'users').document(user).get().to_dict()[u'cards']
    cards = db.collection(u'cards').stream()
    date = datetime.datetime.now()
    transaction = {'amount': 1, 'date': date, 'category': category}
    card_list = []
    for card in cards:
        if card.id in user_cards:
            card_data = card.to_dict()
            points = rewardsEarned(transaction, card_data)
            card_data['currentPoints'] = points
            card_data['id'] = card.id
            message = "{} earns ${} back on every $100 spent at {}.".format(card_data['name'], card_data['currentPoints'], category_to_word(category))
            card_data['message'] = message
            card_list.append(card_data)
    sorted_cards = sorted(card_list, key=lambda card: card['currentPoints'], reverse=True)
    return sorted_cards

# called within newCard
def maxPoints(transaction, candidate_cards):
    max_points = 0
    for card in candidate_cards.values():
        max_points = max(max_points, rewardsEarned(transaction, card))
    return max_points

# find best new card based on transaction history
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
        transaction['category'] = [transaction['category']]
        if (today - date < datetime.timedelta(weeks=12)):
            current_rewards = maxPoints(transaction, candidate_cards)
            for id in candidate_cards:
                delta_rewards = rewardsEarned(transaction, candidate_cards[id]) - current_rewards
                if (delta_rewards > 0):
                    candidate_cards[id]['benefit'] += delta_rewards
    for id in candidate_cards:
        candidate_cards[id]['benefit'] *= 8
        candidate_cards[id]['benefit'] /= 100
        candidate_cards[id]['benefit'] += candidate_cards[id]['bonus'] - candidate_cards[id]['intro'] - candidate_cards[id]['annual']
    sorted_cards = []
    for key, value in sorted(candidate_cards.items(), key=lambda card: card[1]['benefit'], reverse=True):
        sorted_cards.append([key, value])
    return sorted_cards

if __name__ == '__main__':
    new_cards = newCard('Alice')
    print(new_cards)
    best_card = bestCard('restaurant', 'Alice')
    print(best_card)