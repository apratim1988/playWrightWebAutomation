
from pymongo import MongoClient
import os
import logging


class MongoDBConnection:
    def __init__(self, db_name, collection_name):
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None
        self.logger = logging.getLogger('MongoDB')

    def connect(self):
        try:
            mongo_uri = os.getenv('MONGO_URI')
            if not mongo_uri:
                raise EnvironmentError("MONGO_URI environment variable is not set.")

            self.client = MongoClient(mongo_uri)
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            self.logger.info(f"Connected to MongoDB database: {self.db_name}, collection: {self.collection_name}")
        except Exception as e:
            self.logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def disconnect(self):
        if self.client:
            self.client.close()
            self.logger.info("Disconnected from MongoDB")

    def insert_one(self, document):
        try:
            result = self.collection.insert_one(document)
            self.logger.info(f"Document inserted with id: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            self.logger.error(f"Failed to insert document: {e}")
            raise

    def insert_many(self, documents):
        try:
            result = self.collection.insert_many(documents)
            self.logger.info(f"{len(result.inserted_ids)} documents inserted")
            return result.inserted_ids
        except Exception as e:
            self.logger.error(f"Failed to insert documents: {e}")
            raise

    def find_one(self, query):
        try:
            document = self.collection.find_one(query)
            self.logger.info(f"Document found: {document}")
            return document
        except Exception as e:
            self.logger.error(f"Failed to find document: {e}")
            raise

    def find_many(self, query):
        try:
            documents = self.collection.find(query)
            documents_list = list(documents)
            self.logger.info(f"{len(documents_list)} documents found")
            return documents_list
        except Exception as e:
            self.logger.error(f"Failed to find documents: {e}")
            raise

    def update_one(self, query, update):
        try:
            result = self.collection.update_one(query, update)
            self.logger.info(f"Document updated: {result.modified_count} document(s) modified")
            return result.modified_count
        except Exception as e:
            self.logger.error(f"Failed to update document: {e}")
            raise

    def update_many(self, query, update):
        try:
            result = self.collection.update_many(query, update)
            self.logger.info(f"{result.modified_count} documents updated")
            return result.modified_count
        except Exception as e:
            self.logger.error(f"Failed to update documents: {e}")
            raise

    def delete_one(self, query):
        try:
            result = self.collection.delete_one(query)
            self.logger.info(f"Document deleted: {result.deleted_count} document(s) deleted")
            return result.deleted_count
        except Exception as e:
            self.logger.error(f"Failed to delete document: {e}")
            raise

    def delete_many(self, query):
        try:
            result = self.collection.delete_many(query)
            self.logger.info(f"{result.deleted_count} documents deleted")
            return result.deleted_count
        except Exception as e:
            self.logger.error(f"Failed to delete documents: {e}")
            raise
