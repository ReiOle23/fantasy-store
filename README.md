# fantasy-store

This is a project which recreates a store with unique items and auctions
Theres users which buy or bid on items.
Users can only register,log,buy,or bid.

For the Unique items, every one has a limit quantity and when that item hasn't quantity
the other users can't get it.

The system needs to be totally async because we have pics of 1000 people simultaneously buying the same item

For the Auction, the system needs to handle multiple bids simultaneously and care of the values of the bids. 
If two bids at the same time, only one is selected, the other is rejected and informed about the new item value.

## Database
The database will be a mongoDB as we have a large set of items and they have different fields depending on the object type
Example: An Item can be a weapon or an armor or a potion. weapon has durability, potion has time expense.
<!-- Usefull -->
MongoDB could be used as a complement for highly variable product catalogs or review/comment systems, but not as a primary database.
<!--  -->
In this example we don't have payment nor inventory so mongoDB is best option

To enter Mongo instance:
- docker exec -it fantasy_mongodb mongosh "mongodb://fantasy:fantasy@localhost:27017/fantasy_back?authSource=admin"

## Arquitecture
Arquitecture used is a monolitic by layers and using Hexagonal

<!-- Usefull -->
Celery(orquestrator of tasks) with Redis(database cache memory, very fast) you can have sincronous system that
replicates an async by executing tasks of the celery in order and by getting the info from the Redis.
<!--  -->