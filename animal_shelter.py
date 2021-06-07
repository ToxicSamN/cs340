
from pymongo import MongoClient
from bson.objectid import ObjectId


class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password, host, port, database):
        # Initializing the MongoClient. This helps to
        # access the MongoDB databases and collections.
        self.client = MongoClient(f'mongodb://{username}:{password}@{host}:{port}/{database}')
        self.database = self.client[f'{database}']

        # default collection is animals. Caller can change this with set_collection(str) method
        self.collection = None
        self.set_collection()

    def set_collection(self, collection="animals"):
        """
             The set_collection method is a setter method for changing the database collection.
             By default this is set to "animals".
            :param collection:
            :return:
        """
        self.collection = self.database[collection]

    def create(self, data=None) -> bool:
        """
            The create method inserts a document into the database collection
            :param data: dict type object to be inserted to the database
            :return: bool for success or failure
        """
        if data is not None:
            # insert the document to the database. insert() is deprecated, using insert_one()
            result = self.collection.insert_one(data)  # data should be dictionary
            # retrieve the document that was just inserted
            result = self.collection.find_one(data)

            # validate the document was inserted
            if result is not None:
                return True
        else:
            raise Exception("Nothing to save, because data parameter is empty")

        return False

    def read(self, query_filter=None, **kwargs) -> dict:
        """
            The read method will find a document in the database and return it to the user
            :param query_filter: (Optional) dict object to filter the find command. If left blank then all documents are
            retrieved.
            Use a dict to exclude fields from the result (e.g. projection={'_id': False}).
            :return: list of dict objects are returned
        """
        # check if parameter is None and set it to a default
        if query_filter is None:
            query_filter = {}

        return self.collection.find(filter=query_filter, **kwargs)

    def update(self, update_filter=None, update=None, upsert=False) -> bool:
        """
            The update method will accespt an update filter and an update set to send to the database
            :param update_filter: a query that matches the document to update.
            :param update: The modifications to apply to the document.
            :param upsert: If True, perform an insert if no documents match the filter.
            :return: bool True if modified count is 1.
        """

        if not isinstance(update, dict) or not isinstance(update_filter, dict):
            raise Exception(f"invalid parameter type:\nupdate_filter: {type(update_filter)}\nupdate: {type(update)}\n"
                            f"Expected dict, dict")

        result = self.collection.update_one(filter=update_filter, update=update, upsert=upsert)
        if result.modified_count == 1:
            return True

        return False

    def delete(self, delete_filter=None) -> bool:
        """
            The delete method will take a single document and delete it from the database
            :param delete_filter: rdict type object that is required in order to delete the document from the database
            :return: returns a bool for success or failure
        """

        # validate the query is not None
        if not isinstance(delete_filter, dict):
            print(type(delete_filter))
            raise Exception("invalid parameter: delete_filter")

        result = self.collection.delete_one(delete_filter)
        # result is a DeletedResult object with a count of deleted items
        # if one item is deleted then return true
        if result.deleted_count == 1:
            return True

        return False
