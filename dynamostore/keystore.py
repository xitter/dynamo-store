import boto3
import json, decimal
from botocore.exceptions import ClientError
from dynamostore.exception import InvalidInputException, NotFoundException

__all__ = ['KeyStore']


class _DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(_DecimalEncoder, self).default(o)


class KeyStore:
    _db = boto3.resource('dynamodb')
    _table_repository = {}

    @classmethod
    def put(cls, table, primary_key, data):
        model = cls._register_table(table)
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
            return json.dumps(model.put_item(Item=data), cls=_DecimalEncoder)
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
            ), cls=_DecimalEncoder)

    @classmethod
    def get(cls, table, primary_key):
        model = cls._register_table(table)
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
                return json.dumps(response['Item'], cls=_DecimalEncoder)
            else:
                raise NotFoundException()

    @classmethod
    def _register_table(cls, table):
        model = cls._table_repository[table] if table in cls._table_repository else None
        if model is None:
            model = cls._db.Table(table)
        cls._table_repository[table] = model
        return model
