import pymongo

client = pymongo.MongoClient(
    'mongodb+srv://tunaxx:w92WdYDt0CkX6imY@cluster0.dkt5fwz.mongodb.net/?retryWrites=true&w=majority'
)
db = client.get_database('herocode')

options = {
    'validator': {
      '$jsonSchema': {
        'bsonType': 'object',
        'required': [
          'abilities', 'items'
        ],
        'properties': {
          'abilities': {
            'bsonType': [
              'array'
            ],
            'items': {
              'bsonType': [
                'objectId'
              ],
              'enum': list(map(lambda ability: ability.get('_id'), db.Ability.find({})))
            }
          },
          'items': {
            'bsonType': [
              'array'
            ],
            'items': {
              'bsonType': [
                'objectId'
              ],
              'enum': list(map(lambda item: item.get('_id'), db.Item.find({})))
            }
          }
        }
      }
    },
    'validationLevel': "moderate"
}

print(db.command('collMod', 'Player', **options))
