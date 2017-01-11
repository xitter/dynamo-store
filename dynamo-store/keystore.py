import boto3
import json, decimal
from botocore.exceptions import ClientError
from dynamostore.exception import InvalidInputException, NotFoundException


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


class KeyStore():
    __db = boto3.resource('dynamodb')
    __table_repository = dict()

    @classmethod
    def put(cls, table, primary_key, data):
        model = cls.__register_table(table)
        try:
            response = model.get_item(
                Key={
                    'id': primary_key
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise e
        else:
            stored_data = response['Item'] if 'Item' in response else None

        if stored_data is None:
            return json.dumps(model.put_item(Item=data), cls=DecimalEncoder)
        else:
            expression = list()
            expression_attribute_values = {}
            for key, value in data.items():
                if 'id' != key:
                    expression.append(key + '= :' + key + ',')
                    expression_attribute_values[':' + key] = value
            if len(expression) < 1:
                raise InvalidInputException("provide at-least one attribute to update")
            expression = 'set ' + ''.join(expression)[:-1]
            return json.dumps(model.update_item(
                Key={
                    'id': primary_key
                },
                UpdateExpression=expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="UPDATED_NEW"
            ), cls=DecimalEncoder)

    @classmethod
    def get(cls, table, primary_key):
        model = cls.__register_table(table)
        try:
            response = model.get_item(
                Key={
                    'id': primary_key
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise e
        else:
            if 'Item' in response:
                return json.dumps(response['Item'], cls=DecimalEncoder)
            else:
                raise NotFoundException()

    @classmethod
    def __register_table(cls, table):
        model = cls.__table_repository[table] if table in cls.__table_repository else None
        if model is None:
            model = cls.__db.Table(table)
        cls.__table_repository[table] = model
        return model
