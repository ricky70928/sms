import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Server(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('ilo_ip', 
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id', 
        type=int,
        required=True,
        help="Every item needs a store id."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Itme now found'}, 404
    
    def post(self, name): 
        if ItemModel.find_by_name(name):
            return {'message': "A item with name '{}' already exists.".format(name)}, 400 # 400 bad request

        #data = request.get_json()
        data = self.parser.parse_args()

        item = ItemModel(name, **data)
        
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500 # internal server error

        return item.json(), 201 # 201 for create, 202 accept

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        
        return {'message': 'Item deleted'}

    def put(self, name):
        data = self.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ServerList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        #return {'items': list(map(lambda x: x.json, ItemModel.query.all()))}
