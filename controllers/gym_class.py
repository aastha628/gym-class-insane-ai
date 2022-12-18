from fastapi import Response, status, HTTPException
from utils.dbConnection import Database
from models.gym_class import GymClass as GymClassModel
from models.gym_class import UpdateClass
from utils.json_formatter import getJsonResponse
from utils.auth import AuthHandler


class GymClass():
    def __init__(self):
        self.connection = Database.getInstance()
        self.cur = self.connection.cursor()
        self.table_name = 'gym_class'

    def create_gym_class(self, gym_class: GymClassModel, res: Response):
        try:
            check_query = """select * from gym_class where name = %s """
            query_param = (gym_class.name,)
            self.cur.execute(check_query, query_param)
            if self.cur.rowcount > 0:
                res.body = {'message': "Class already exist!"}
                raise
            if gym_class.current_member_count == None:
                gym_class.current_member_count = 0

            if gym_class.capacity < gym_class.current_member_count:
                res.body = {
                    "message": "Current member count cannot be more than capacity of class!"}
                raise

            record_to_insert = (gym_class.name, gym_class.instructor, gym_class.time,
                                gym_class.capacity, gym_class.current_member_count)
            query = """insert into gym_class (name,instructor,time,capacity,current_member_count) values(%s,%s,%s,%s,%s) returning *"""
            self.cur.execute(query, record_to_insert)
            res.body = {"message": "Class created successfully!"}
            self.connection.commit()
            return res.body
        except Exception as e:
            res.status_code = status.HTTP_400_BAD_REQUEST
            self.connection.rollback()
            return res.body or {'message': str(e)}

    def delete_gym_class(self, id, res: Response):
        try:
            params = (id,)
            query = """delete from gym_class where id=%s"""
            self.cur.execute(query, params)
            res.body = {"message": "Class deleted successfully!"}
            self.connection.commit()
            return res.body

        except Exception as e:
            res.status_code = status.HTTP_400_BAD_REQUEST
            self.connection.rollback()
            return res.body or {'message': str(e)}

    def update_gym_class(self, id, gym_class: UpdateClass, res: Response):
        try:
            params = (id,)
            query = """select * from members where id=%s"""
            self.cur.execute(query, params)
            if self.cur.rowcount == 0:
                res.body = {"message": "Class does not exist!"}
                raise
            result = getJsonResponse(self.cur)
            if gym_class.instructor == None:
                gym_class.instructor = result['instructor']
            if gym_class.time == None:
                gym_class.time = result['time']
            if gym_class.capacity == None:
                gym_class.capacity = result['capacity']
            if gym_class.current_member_count == None:
                gym_class.current_member_count = result['current_member_count']

            if gym_class.capacity < gym_class.current_member_count:
                res.body = {
                    "messaeg": "Current capacity of class is greater than total capacity of class"}
                raise
            record_to_update = (gym_class.instructor, gym_class.time,
                                gym_class.capacity, gym_class.current_member_count, id)
            query = """update members set instructor=%s, time= %s, capacity=%s , current_member_count=%s where id = %s"""
            self.cur.execute(query, record_to_update)
            res.body = {"message": "Class updated successfully!"}
            self.connection.commit()
            return res.body

        except Exception as e:
            res.status_code = status.HTTP_400_BAD_REQUEST
            self.connection.rollback()
            return res.body or {'message': str(e)}

    def get_all_gym_classes(self, res: Response):
        try:
            query = """select * from gym_class"""
            self.cur.execute(query)
            if self.cur.rowcount == 0:
                res.body = {"message": "No class exist!"}
                raise
            result = getJsonResponse(self.cur,True)
            self.connection.commit()
            return result

        except Exception as e:
            res.status_code = status.HTTP_400_BAD_REQUEST
            self.connection.rollback()
            return res.body or {'message': str(e)}

    def get_all_members(self, id, res: Response):
        try:
            query = """select * from members where gym_class=%s"""
            gym_class = (id,)
            self.cur.execute(query, gym_class)
            if self.cur.rowcount == 0:
                res.body = {"message": "No member exist in this class!!"}
                raise
            result = getJsonResponse(self.cur,True)
            self.connection.commit()
            return result

        except Exception as e:
            res.status_code = status.HTTP_400_BAD_REQUEST
            self.connection.rollback()
            return res.body or {'message': str(e)}
