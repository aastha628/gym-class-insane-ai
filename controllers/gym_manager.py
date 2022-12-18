from fastapi import Response, status, HTTPException
from utils.dbConnection import Database
from models.gym_manager import GymManager as GymManagerModel, LoginRequest
from utils.json_formatter import getJsonResponse
from utils.auth import AuthHandler


class GymManager:

    def __init__(self):
        self.connection = Database.getInstance()
        self.cur = self.connection.cursor()
        self.table_name = 'managers'

    def register_manager(self, manager: GymManagerModel, res: Response):
        try:
            check_query = """select * from managers where email = %s """
            query_param = (manager.email,)
            self.cur.execute(check_query, query_param)
            if self.cur.rowcount > 0:
                res.body = {'message': "User already registered!"}
                raise
            hashed_password = AuthHandler().get_password_hash(manager.password)

            record_to_insert = (manager.name, manager.email, hashed_password)
            query = """insert into managers (name,email,password) values(%s,%s,%s) returning *"""
            self.cur.execute(query, record_to_insert)
            res.body = {"message": "User created successfully!"}
            self.connection.commit()
            return res.body
        except Exception as e:
            res.status_code = status.HTTP_400_BAD_REQUEST
            self.connection.rollback()
            return res.body or {'message': str(e)}

    def login_manager(self, manager: LoginRequest, res: Response):
        try:
            check_query = """select * from managers where email = %s"""
            query_param = (manager.email,)
            self.cur.execute(check_query, query_param)
            result = getJsonResponse(self.cur)
            if not result or (not AuthHandler().verify_password(manager.password, result['password'])):
                res.status_code = 401
                res.body = {"message": "Invalid email and/or password!"}
                raise
            token = AuthHandler().encode_token(result['id'])
            response = {"message": "Login successfully!", "token": token}
            return response
        except Exception as e:
            if res.status_code != 401:
                res.status_code = 500
            self.connection.rollback()
            return res.body or {'message': str(e)}


#     user=None
#     for x in users:
#         if x['email']==user_details.email:
#             user = x

#     if (user is None) or (not auth_handler.verify_password(user_details.password,user['password'])):
#         raise HTTPException(status_code=401,detail="Invalid email and/or password!")
#     token=auth_handler.encode_token(user['email'])
#     return {'token':token}
