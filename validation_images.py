import pymongo

client = pymongo.MongoClient(
    'mongodb+srv://tunaxx:w92WdYDt0CkX6imY@cluster0.dkt5fwz.mongodb.net/?retryWrites=true&w=majority'
)
db = client.get_database('herocode')

options = {
    'validator': {
      '$jsonSchema': {
        'bsonType': 'object',
        'required': ['image_id'],
        'properties': {
          'image_id': {
            'bsonType': 'objectId',
            'enum': list(map(lambda image: image.get('_id'), db.Images.find({})))
          }
        }
      }
    },
    'validationLevel': "moderate"
}

print(db.command('collMod', 'Ability', **options))
print(db.command('collMod', 'Enemy', **options))
print(db.command('collMod', 'Item', **options))