import lipsum
import json
import osmapi
import sys
import argparse
from nominatim import Nominatim
import os
import random

def basename(x):
    return os.path.split(x)[-1]

def generate_product_data(n):
    pass

def generate_categories_data(n, d):
    pass

def generate_shop_data(n, d):
    shops = ['Vasilopoulos', 'Sklavenitis', 'Lidl', 'Elomas']
    results = []
    i = 0
    while len(results) <= n or i < len(shops):
        results.extend(nom.query(shops[i]))
        i += 1

    results = results[:n]
    output = []

    for i, r in enumerate(results):
        x = {
            'model' : 'cheapiesgr.shop',
            'pk' : i + 1,
            'fields' : {
                'address' : r['display_name'],
                'city' : r['display_name'],
                'location' : 'POINT({} {})'.format(r['lon'], r['lat'])
                }
            }

        output.append(x)

    return output

def generate_user_data(n, d):
    output = []
    with open('FunnyNames.txt') as f:
        names = f.read().splitlines()

    for i in range(1, n+1):
        uname = 'user' + str(i)
        temp = names[i].split(' ')
        first_name = temp[0]
        last_name = ' '.join(temp[1:])

        user = {
            'model': 'cheapiesgr.myuser',
            'pk' : i,
            'fields' : {
                'username' : uname,
                'email' : uname + '@example.com'
            }
        }

        volunteer = {
            'model' : 'cheapiesgr.volunteer',
            'pk' : i,
            'fields' : {
                'user' : i,
                'first_name' : first_name,
                'last_name' : last_name
            }
        }

        output.extend([user, volunteer])

    return output

def generate_qar_data(n, d):
    output = []

    for i in range(1, n + 1):

        question = {
            'model' : 'cheapiesgr.question',
            'pk' : i,
            'fields' : {
                'question_text' : lipsum.generate_words(20),
                'registration' : i
            }
        }

        answer = {
            'model' : 'cheapiesgr.answer',
            'pk' : i,
            'fields' : {
                'answer_text' : lipsum.generate_words(20),
                'question' : i
            }
        }

        rating = {
            'model' : 'cheapiesgr.rating',
            'pk' : i,
            'fields' : {
                'rate_explaination' : lipsum.generate_words(20),
                'registration' : i,
                'volunteer' : i,
                'stars' : random.randint(1, 5),
                'validity_of_this_rating' : random.randint(1, 5)
            }
        }

        output.extend([question, answer, rating])

    return output

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-n', type=int, default=10, help='Number of data')
    argparser.add_argument('-t', type=str, default='')
    argparser.add_argument('-d', type=str, help='Crawled data directory')

    options = {
        'shop' : generate_shop_data,
        'categories': generate_categories_data,
        'products' : generate_product_data,
        'user' : generate_user_data,
        'qar' : generate_qar_data
    }


    nom = Nominatim()

    args = argparser.parse_args()
    # Generate desired data
    if args.t == '':
        pipeline = ['shop', 'user']
    else:
        pipeline = [args.t]

    for p in pipeline:
        output = options[p](args.n, args.d)

        # Write to file
        with open(p + '.json', 'w+') as f:
            f.write(json.dumps(output, ensure_ascii=False))
