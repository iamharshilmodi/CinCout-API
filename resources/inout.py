from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from models import InOutTime
from schemas import InOutSchema, InOutTimeUpdateSchema

from db import db 

blp = Blueprint("Times", "times", description="Operations on in-out Times")


@blp.route("/item/<string:mis>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, InOutSchema)
    def get(self, mis):
        item = InOutTime.find_latest(mis)
        if item:
            return item
        abort(404, message="Item not found")

    @jwt_required()
    @blp.arguments(InOutSchema)
    @blp.response(201, InOutSchema)
    def post(self, item_data, mis):
        obj = InOutTime.find_latest(item_data['mis'])
        if (obj) and (obj.time_in is None):
            # abort(400, message="In Time for the entry at" + obj.time_out + "dated" + obj.date_out + "is not marked yet.")
            abort(400, message="In Time for the last entry not marked yet.")

        item = InOutTime(**item_data)

        try:
            item.save_to_db()
        except SQLAlchemyError:
            abort(500, message=SQLAlchemyError)

        return item

    @jwt_required()
    def delete(self, mis):
        # jwt = get_jwt()
        # if not jwt["is_admin"]:
        #     abort(401, message="Admin privilege required.")

        item = InOutTime.find_latest(mis)
        if item:
            tid=item.in_out_id
            item.delete_from_db()
            return {"message": "Item with id " + str(tid) + " deleted."}
        abort(404, message="Item not found.")

    @blp.arguments(InOutTimeUpdateSchema)
    @blp.response(200, InOutSchema)
    def put(self, item_data, mis):
        item = InOutTime.find_latest(item_data['mis'])

        # return item
    
        if item:
            item.time_in = item_data['time_in']
            item.date_in = item_data['date_in']
        else:
            abort(400, message="Item not found.")

        print(item.time_in)
        
        try:
            item.update_to_db()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item


@blp.route("/all_items/<string:mis>")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, InOutSchema(many=True))
    def get(self,mis):
        return InOutTime.find_by_mis(mis=mis)
