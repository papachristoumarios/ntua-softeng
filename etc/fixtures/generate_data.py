# Generate a fake database for the django application
import datetime
import glob
import lipsum
import json
import osmapi
import sys
import argparse
from nominatim import Nominatim
import os
import random

def basename(x):
    # Returns the basename of a file
    return os.path.split(x)[1]

def generate_product_data(n, d):
    # Generate product registrations
    output = []

    categories = glob.glob(os.path.join(os.path.abspath(d), '*/'))
    pk = 1
    for i, c in enumerate(categories[:n]):
        with open(os.path.join(c, 'data.csv')) as f:
            products = f.read().splitlines()

        for j, p in enumerate(products[:n]):
            q = p.split(', ')
            try:
                pr = float(q[1])
            except:
                pr = 10 * random.random()
            registration = {
                'model' : 'cheapiesgr.registration',
                'pk' : pk,
                'fields' : {
                    'price' : pr,
                    'product_description' : ', '.join(q[2:-1]),
                    'shop' : random.randint(1, 5),
                    'volunteer' : j + 1,
                    'category' : i + 1,
                    'date_of_registration' : '2018-11-27'
                }
            }
            pk += 1

        output.extend([registration])

    return output

def generate_categories_data(n, d):
    # Generate data on categories and (sub)-sub-categories
    output = []

    categories = glob.glob(os.path.join(os.path.abspath(d), '*/'))

    for i, c in enumerate(categories[:n]):
        img_path = glob.glob(os.path.join(c, 'images', '*'))
        category2 = {
            'model' : 'cheapiesgr.category2',
            'pk' : i + 1,
            'fields' : {
                'category2_description' : basename(c) + '2',
                # 'image' : random.choice(img_path)
            }
        }

        category1 = {
            'model' : 'cheapiesgr.category1',
            'pk' : i + 1,
            'fields' : {
                'category1_description' : basename(c) + '1',
                'category2' : i + 1,
                # 'image' : random.choice(img_path)
            }
        }

        category = {
            'model' : 'cheapiesgr.category',
            'pk' : i + 1,
            'fields' : {
                'category_description' : basename(c),
                'category1' : i + 1,
                # 'image' : random.choice(img_path)
            }
        }

        output.extend([category, category1, category2])

    return output

def generate_shop_data(n, d):
    # Generate points on the map for various stores using OSM Nominatim API
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
    # Generate fake user data
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
    # Generate questions, answers and ratings
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
                'rate_explanation' : lipsum.generate_words(20),
                'registration' : i,
                'volunteer' : i,
                'stars' : random.randint(1, 5),
                'validity_of_this_rate' : random.randint(1, 5)
            }
        }

        output.extend([question, answer, rating])

    return output

def apply_fixtures(pipeline):
    os.chdir('../..')
    for p in pipeline:
        os.system('python3 manage.py loaddata etc/fixtures/{}.json'.format(p))	

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-n', type=int, default=10, help='Number of data')
    argparser.add_argument('-t', type=str, default='')
    argparser.add_argument('-d', type=str, help='Crawled data directory')
    argparser.add_argument('--apply', action='store_true', help='Apply fixtures')
    options = {
        'shop' : generate_shop_data,
        'categories': generate_categories_data,
        'products' : generate_product_data,
        'user' : generate_user_data,
        'qar' : generate_qar_data,
    }


    nom = Nominatim()

    args = argparser.parse_args()
    # Generate desired data
    if args.t == '':
	# Use default pipeline
        pipeline = ['shop', 'user', 'categories', 'products', 'qar']
    else:
        pipeline = [args.t]

    for p in pipeline:
        output = options[p](args.n, args.d)

        # Write to file
        with open(p + '.json', 'w+') as f:
            f.write(json.dumps(output, ensure_ascii=False))

        if args.apply_fixtures:
            apply_fixtures(pipeline)
