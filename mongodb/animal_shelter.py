
from pymongo import MongoClient
from bson.objectid import ObjectId


class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password, host, port, database):
        # Initializing the MongoClient. This helps to
        # access the MongoDB databases and collections.
        self.client = MongoClient(f'mongodb://{username}:{password}@{host}:{port}/{database}')
        self.database = self.client[f'{database}']
        self.collection = self.database["animals"]

    def create(self, data=None) -> bool:
        """
            The create method inserts a document into the database collection
            :param data: dict type object to be inserted to the database
            :return: bool for success or failure
        """
        if data is not None:
            # insert the document to the database. insert() is deprecated, using insert_one()
            result = self.database.animals.insert_one(data)  # data should be dictionary
            # retrieve the document that was just inserted
            result = self.collection.find_one(data)

            # validate the document was inserted
            if result is not None:
                return True
        else:
            raise Exception("Nothing to save, because data parameter is empty")

        return False

    def read(self, query_filter=None) -> dict:
        """
            The read method will fond a docuement in the database and return it to the user
            :param query_filter: (Optional) dict object to filter the find command. If left blank then all documents are
            retieved.
            :return: list of dict objects are returned
        """
        # check if parameter is None and set it to a default
        if query_filter is None:
            query_filter = {}

        return self.collection.find(query_filter)

    # TODO: Requires proper implementation. Not yet working
    def update(self, update=None, update_filter=None) -> bool:
        """
        The update method will accespt an update filter and an update set to send to the database
        :param update:
        :param update_filter:
        :return:
        """
        # FIXME: Broken, need to debug and figure it out
        if update is not dict or update_filter is not dict:
            raise Exception("unable to process update with invalid arguments")

        result = self.collection.update_one(update_filter, update)
        if result == 1:
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
