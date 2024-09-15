from flask import Blueprint
from flask_restful import Api
from flask_restful import Resource
from flask_restful import reqparse

from .sheets import getAnggota
from .sheets import addAbsensi

api_bp = Blueprint("api", __name__)
api = Api(api_bp)

class Siswa(Resource):
    def __init__(self) -> None:
        self.parser = reqparse.RequestParser()
        super().__init__()

    def get(self):
        self.parser.add_argument("id", type=int, location="args")
        args = self.parser.parse_args()

        return getAnggota(**args)

    def post(self):
        self.parser.add_argument("id", type=int)
        args = self.parser.parse_args()
        print(args)

        return addAbsensi(**args)

api.add_resource(Siswa, "/siswa")
