from fastapi import Response, status, HTTPException
from utils.dbConnection import Database
from models.gym_member import GymMembers as GymMemberModel
from models.gym_member import UpdateMember
from utils.json_formatter import getJsonResponse
from utils.auth import AuthHandler


class GymMember:

    def __init__(self):
        self.connection = Database.getInstance()
        self.cur = self.connection.cursor()
        self.table_name = 'members'

    def create_member(self, member: GymMemberModel, res: Response):
        try:
            check_query = """select * from members where email = %s """
            query_param = (member.email,)
            self.cur.execute(check_query, query_param)
            if self.cur.rowcount > 0:
                res.body = {'message': "Member already registered!"}
                raise
            if member.gym_class:
                query = """select capacity,current_member_count from gym_class where id=%s"""
                query_param = (member.gym_class,)
                self.cur.execute(query, query_param)
                result = getJsonResponse(self.cur)
                if result['capacity'] < result['current_member_count']+1:
                    res.body = {
                        "message": "Class filled cannot add more members to it!"}
                    raise
                else:
                    query = """update gym_class set current_member_count = current_member_count+1 where id = %s"""
                    query_param = (member.gym_class,)
                    self.cur.execute(query, query_param)

            record_to_insert = (member.name, member.email, member.contact,
                                member.membership_type, member.gym_class)
            query = """insert into members (name,email,contact,membership_type,gym_class) values(%s,%s,%s,%s,%s) returning *"""
            self.cur.execute(query, record_to_insert)
            res.body = {"message": "Member created successfully!"}
            self.connection.commit()

            return res.body
        except Exception as e:
            res.status_code = status.HTTP_400_BAD_REQUEST
            self.connection.rollback()
            return res.body or {'message': str(e)}

    def delete_member(self, id, res: Response):
        try:
            query = """select * from members where id=%s"""
            params = (id,)
            self.cur.execute(query, params)
            if self.cur.rowcount == 0:
                res.body = {"message": "No member exist!"}
                raise
            result = getJsonResponse(self.cur)
            if result['gym_class']:
                query = """update gym_class set current_member_count = current_member_count-1 where id = %s"""
                query_param = (result['gym_class'],)
                self.cur.execute(query, query_param)
            params = (id,)
            query = """delete from members where id=%s"""
            self.cur.execute(query, params)
            res.body = {"message": "Member deleted successfully!"}
            self.connection.commit()
            return res.body

        except Exception as e:
            res.status_code = status.HTTP_400_BAD_REQUEST
            self.connection.rollback()
            return res.body or {'message': str(e)}

    def update_member(self, id, member: UpdateMember, res: Response):
        try:
            params = (id,)
            query = """select * from members where id=%s"""
            self.cur.execute(query, params)
            if self.cur.rowcount == 0:
                res.body = {"message": "User does not exist!"}
                raise
            result = getJsonResponse(self.cur)

            if member.name == None:
                member.name = result['name']
            if member.contact == None:
                member.contact = result['contact']
            if member.gym_class == None:
                member.gym_class = result['gym_class']
            if member.membership_type == None:
                member.membership_type = result['membership_type']

            if member.gym_class and member.gym_class != result['gym_class']:

                query = """select capacity,current_member_count from gym_class where id=%s"""
                query_param = (member.gym_class,)
                self.cur.execute(query, query_param)
                result_class = getJsonResponse(self.cur)
                if result_class['capacity'] < result_class['current_member_count']+1:
                    res.body = {
                        "message": "Class filled cannot add more members to it!"}
                    raise
                else:
                    query = """update gym_class set current_member_count = current_member_count+1 where id = %s"""
                    query_param = (member.gym_class,)
                    self.cur.execute(query, query_param)

                    if result['gym_class']:
                        query = """update gym_class set current_member_count = current_member_count-1 where id = %s"""
                        query_param = (result['gym_class'],)
                        self.cur.execute(query, query_param)

            record_to_update = (member.name, member.contact,
                                member.membership_type, member.gym_class, id)
            query = """update members set name=%s, contact = %s,membership_type=%s , gym_class=%s where id = %s"""
            self.cur.execute(query, record_to_update)
            res.body = {"message": "Member updated successfully!"}
            self.connection.commit()
            return res.body

        except Exception as e:
            res.status_code = status.HTTP_400_BAD_REQUEST
            self.connection.rollback()
            return res.body or {'message': str(e)}

    def get_members_details(self, res: Response):
        try:
            query = """select * from members"""
            self.cur.execute(query)
            if self.cur.rowcount == 0:
                res.body = {"message": "No member exist!"}
                raise
            result = getJsonResponse(self.cur,True)
            self.connection.commit()
            return result

        except Exception as e:
            res.status_code = status.HTTP_400_BAD_REQUEST
            self.connection.rollback()
            return res.body or {'message': str(e)}
