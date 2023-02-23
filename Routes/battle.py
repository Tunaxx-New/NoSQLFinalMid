from datetime import datetime

from main import db
from flask import Blueprint
from flask import request
from bson.json_util import ObjectId, Int64

#from Models.Player import Player
#from Models.Battle import Battle
#from Models.Enemy import Enemy

battle = Blueprint('battle', __name__)


@battle.route('/initialize_battle', methods=['POST'])
def initialize_battle():
    player_id = request.form.get('player_id', None)
    enemy_sql_id = request.form.get('enemy_sql_id', None)

    if None in [enemy_sql_id, player_id]:
        return dict(status=False)
    try:
        enemy_sql_id = int(enemy_sql_id)
    except ValueError:
        return dict(status=False)

    enemy = db.get_collection("Enemy").find_one({'enemy_id': enemy_sql_id})
    battle = db.get_collection("Battle").find_one({'player_id': ObjectId(player_id)})

    if battle is None:
        battle: dict = {'_id': ''}
        battle['_id'] = db.get_collection('Battle').insert_one({
            'player_id': ObjectId(player_id)
        }).inserted_id


    if None in [enemy]:
        return dict(status=False)

    db.get_collection("Battle").update_one(
        {
            '_id': ObjectId(battle.get('_id'))
        },
        {
            "$set": {
                'enemy_id': enemy.get('_id'),
                'enemy_hp': enemy.get('hp'),
                'last_action_data': datetime.utcnow()
            }
        }
    )

    return dict(status=True, enemy_hp=enemy.get('hp'))


@battle.route('/damage_enemy', methods=['POST'])
def damage_enemy():
    player_id = request.form.get('player_id', None)
    damage = request.form.get('damage', None)

    if None in [player_id, damage]:
        return dict(status=False)

    battle = db.get_collection("Battle").find_one({'player_id': ObjectId(player_id)})

    if None is battle:
        return dict(status=False)

    enemy_id = db.get_collection("Enemy").find_one({
        '_id': ObjectId(battle.get('enemy_id'))
    }).get('_id')

    if None in [enemy_id, damage]:
        return dict(status=False)
    try:
        damage = int(damage)
    except ValueError:
        return dict(status=False)

    player = db.get_collection("Player").find_one({
        '_id': ObjectId(battle.get('player_id'))
    })
    hp = player.get('hp')

    result = db.ItemPlayer.aggregate([{
      "$lookup": {
        "from": "Player",
        "localField": "player_id",
        "foreignField": "_id",
        "as": "PlayerData"
      }
    },
    {
      "$lookup": {
        "from": "Item",
        "localField": "item_id",
        "foreignField": "_id",
        "as": "ItemData"
      }
    },
    {"$unwind": "$ItemData"},
    {
      "$group": {
        "_id": {"player": "$player_id", "item": "$item_id"},
        "count": {"$sum": 1},
        "sum_increment_damage": {"$sum": "$ItemData.increment.damage"},
        "sum_decrement_damage": {"$sum": "$ItemData.decrement.damage"},
        "damage_unit": {"$max": "$ItemData.increment.damage"},

        "sum_increment_hp": {"$sum": "$ItemData.increment.hp"},
        "sum_decrement_hp": {"$sum": "$ItemData.decrement.hp"}
      }
    }
    ])

    for r in result:
        print(r)
        damage += r.get('sum_increment_damage') - r.get('sum_decrement_damage')
        hp += r.get('sum_increment_hp') - r.get('sum_decrement_hp')

    enemy_hp = battle.get('enemy_hp') - damage
    if enemy_hp < 0:
        enemy_hp = 0

    db.get_collection("Player").update_one(
        {
            '_id': ObjectId(player.get('_id'))
        },
        {
            "$set": {
                'hp': hp
            }
        }
    )

    db.get_collection("Battle").update_one(
        {
            '_id': ObjectId(battle.get('_id'))
        },
        {
            "$set": {
                'enemy_hp': enemy_hp,
                'last_action_data': datetime.utcnow()
            }
        }
    )

    return dict(status=True, enemy_hp=enemy_hp)


@battle.route('/damage_player', methods=['POST'])
def damage_player():
    player_id = request.form.get('player_id', None)
    damage = request.form.get('damage', None)

    damage = db.get_collection("Player").find_one({'player_id': ObjectId(player_id)}).get('base_damage')

    if None in [player_id, damage]:
        return dict(status=False)
    try:
        damage = int(damage)
    except ValueError:
        return dict(status=False)

    player = db.get_collection("Player").find_one({'user_id': Int64(player_id)})
    if None is player:
        return dict(status=False)


    player_hp = player.get('player_hp') - damage
    if player_hp < 0:
        player_hp = 0

    db.get_collection("Player").update_one(
        {
            '_id': ObjectId(player.get('_id'))
        },
        {
            "$set": {
                'player_hp': player_hp
            }
        }
    )

    return dict(status=True)


@battle.route('/push_item', methods=['POST'])
def push_item():
    player_id = request.form.get('player_id', None)
    item_id = request.form.get('item_id', None)

    if None in [player_id, item_id]:
        return dict(status=False)


    player = db.get_collection("Player").find_one({'user_id': Int64(player_id)})
    if None is player:
        return dict(status=False)

    db.get_collection("ItemPlayer").insert_one(
        {
            'item_id': ObjectId(item_id),
            'player_id': ObjectId(player.get('_id'))
        }
    )

    db.get_collection("Player").update_one(
        {
            "_id": ObjectId(player.get("_id"))
        },
        {
            "$push": {
                "items": ObjectId(item_id)
            }
        }
    )

    return dict(status=True)

@battle.route('/delete_item', methods=['POST'])
def delete_item():
    player_id = request.form.get('player_id', None)
    item_index = request.form.get('item_index', None)

    if None in [player_id, item_index]:
        return dict(status=False)

    try:
        item_index = int(item_index)
    except ValueError:
        return dict(status=False)

    db.get_collection("Player").update_one(
        {
            '_id': ObjectId(player_id)
        },
        {
            '$unset': {'items.{}'.format(item_index): 1}
        }
    )
    db.get_collection("Player").update_one(
        {
            '_id': ObjectId(player_id)
        },
        {
            '$pull': {'items': None}
        }
    )

    return dict(status=True)