import pymongo

client = pymongo.MongoClient(
    'mongodb+srv://tunaxx:w92WdYDt0CkX6imY@cluster0.dkt5fwz.mongodb.net/?retryWrites=true&w=majority'
)
db = client.get_database('herocode')

options = {
    'validator': {
      '$jsonSchema': {
        'bsonType': 'object',
        'required': ['item_id', 'player_id'],
        'properties': {
          'item_id': {
            'bsonType': 'objectId',
            'enum': list(map(lambda item: item.get('_id'), db.Item.find({})))
          },
          'player_id': {
            'bsonType': 'objectId',
            'enum': list(map(lambda player: player.get('_id'), db.Player.find({})))
          }
        }
      }
    },
    'validationLevel': "moderate"
}

print(db.command('collMod', 'ItemPlayer', **options))
