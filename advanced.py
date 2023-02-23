import pymongo

client = pymongo.MongoClient(
    'mongodb+srv://tunaxx:w92WdYDt0CkX6imY@cluster0.dkt5fwz.mongodb.net/?retryWrites=true&w=majority'
)
db = client.get_database('herocode')
#"size_in_bytes": {"$binarySize": "$data"}
def images_info() -> [dict]:
    results_size = db.get_collection("Images").aggregate([{
        "$group": {
            "_id": {"size_in_pixels": {"$multiply": ["$height", "$width"]}},
            "sum_size": {"$sum": {"$binarySize": "$data"}},
            "count": {"$sum": 1},
            "average": {"$avg": {"$multiply": ["$height", "$width"]}},
            "max": {"$max": {"$multiply": ["$height", "$width"]}},
            "min": {"$min": {"$multiply": ["$height", "$width"]}}
        }
    }])
    results_bsize = db.get_collection("Images").aggregate([{
        "$group": {
            "_id": {"size_in_bytes": {"$binarySize": "$data"}},
            "sum_size_in_bytes": {"$sum": {"$binarySize": "$data"}},
            "count": {"$sum": 1},
            "average": {"$avg": {"$binarySize": "$data"}},
            "max": {"$max": {"$binarySize": "$data"}},
            "min": {"$min": {"$binarySize": "$data"}}
        }
    }])
    results_all = db.get_collection("Images").aggregate([{
        "$group": {
            "_id": None,
            "count": {"$sum": 1},
            "sum_size_binary": {"$sum": {"$binarySize": "$data"}},
            "average_size_binary": {"$avg": {"$binarySize": "$data"}},
            "max_size_binary": {"$max": {"$binarySize": "$data"}},
            "min_size_binary": {"$min": {"$binarySize": "$data"}},

            "sum_size": {"$sum": {"$binarySize": "$data"}},
            "average_size": {"$avg": {"$multiply": ["$height", "$width"]}},
            "max_size": {"$max": {"$multiply": ["$height", "$width"]}},
            "min_size": {"$min": {"$multiply": ["$height", "$width"]}}
        }
    }])
    print("Images size grouping")
    for r in results_size:
        print("\n".join("{!r}: {!r},".format(k, v) for k, v in r.items()))
        print('\n')
    print("\nImages binary size grouping")
    for r in results_bsize:
        print("\n".join("{!r}: {!r},".format(k, v) for k, v in r.items()))
        print('\n')
    print("\nImages grouping all")
    for r in results_all:
        print( "\n".join("{!r}: {!r},".format(k, v) for k, v in r.items()))
    return results_bsize

images_info()

# Using this index, to optimize frequent request Battles
#db.get_collection("Battle").create_index([("last_action_data", -1)])

# Using this index, to optimize item search by name in all items
#db.get_collection("Item").create_index([("name", 1)])
