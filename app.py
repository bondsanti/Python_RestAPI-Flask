from flask import Flask,request
from flask_restful import Api,Resource,abort,reqparse,marshal_with,fields
from flask_sqlalchemy import SQLAlchemy,Model


app = Flask(__name__)
#connect database
db=SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///database.db"
#create api
api = Api(app)


class ProvinceModel(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    weather=db.Column(db.String(200),nullable=False)
    temp=db.Column(db.String(50),nullable=False)

    def __repr__(self):
        return "Province(name={name},weather={weather},temp={temp})"

db.create_all()

add_args_data = reqparse.RequestParser()
add_args_data.add_argument("name",type=str,required=True,help="กรุณาป้อน ชื่อจังหวัด")
add_args_data.add_argument("weather",type=str,required=True,help="กรุณาป้อน สภาพอากาศ")
add_args_data.add_argument("temp",type=str,required=True,help="กรุณาป้อน อุณภูมิ")

update_args_data = reqparse.RequestParser()
update_args_data.add_argument("name",type=str,help="กรุณาป้อน ชื่อจังหวัด ที่ต้องการแก้ไข")
update_args_data.add_argument("weather",type=str,help="กรุณาป้อน สภาพอากาศ ที่ต้องการแก้ไข")
update_args_data.add_argument("temp",type=str,help="กรุณาป้อน อุณภูมิ ที่ต้องการแก้ไข")



resource_field={
    "id":fields.Integer,
    "name":fields.String,
    "weather":fields.String,
    "temp":fields.String
}




#design
class WeatherCity(Resource):
    #get
    @marshal_with(resource_field)  
    def get(self,pID):
       result = ProvinceModel.query.filter_by(id=pID).first()
       if not result:
           abort(404,message="ไม่พบข้อมูล")
       return result  
    #post
    @marshal_with(resource_field)  
    def post(self,pID):
        result = ProvinceModel.query.filter_by(id=pID).first()
        if result:
           abort(409,message="ID ซ้ำ")
        args=add_args_data.parse_args()
        province=ProvinceModel(id=pID,name=args["name"],weather=args["weather"],temp=args["temp"])
        db.session.add(province)
        db.session.commit()
        return province,201
    
    
    @marshal_with(resource_field)
    def patch(self,pID): 
        args=update_args_data.parse_args()
        result = ProvinceModel.query.filter_by(id=pID).first()
        if not result:
            abort(404,message="ไม่พบข้อมูลที่ต้องการแก้ไข")
        if args["name"]:
            result.name=args["name"]
        if args["weather"]:
            result.weather=args["weather"]
        if args["temp"]:
            result.temp=args["temp"]
        db.session.commit()
        return result



#call
api.add_resource(WeatherCity,"/weather/<int:pID>")#path url api


@app.route('/')
def index():
    query = request.args.get("query")
    print(query)
    return {"msg" : "Hello! API"},201


if __name__ == "__main__":
    app.run(debug=True)