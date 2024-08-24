"""
animal_shelter.py

This script defines the AnimalShelter class, which provides methods for interacting with 
a MongoDB database to manage animal records in a shelter. The class includes functionality 
for creating, reading, updating, and deleting animal records.

Dependencies:
    - pymongo: MongoDB driver for Python.
    - bson: Library for BSON (Binary JSON) data handling.

Class:
    - AnimalShelter: Provides methods to interact with the MongoDB database.

Methods:
    - __init__(self, username: str, password: str): Initializes the MongoDB client 
      and sets up the database and collection.
    - create(self, data: dict) -> bool: Inserts a new document into the collection.
    - read(self, query: dict) -> list: Retrieves documents from the collection based 
      on a query.
    - update(self, query: dict, update_data: dict) -> int: Updates documents in 
      the collection based on a query.
    - delete(self, query: dict) -> int: Deletes documents from the collection based 
      on a query.
      
Author: Hannah Rose Morgenstein
Date: 08-04-2024
"""

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
from bson.objectid import ObjectId

class AnimalShelter:
    """
    A class to interact with the AnimalShelter database.

    Attributes:
        client (MongoClient): The MongoDB client.
        database (Database): The specific database for the shelter.
        collection (Collection): The collection of animal records.
    """

    def __init__(self, username, password):
        """
        Initializes the AnimalShelter class with MongoDB credentials.

        Args:
            username: The MongoDB username.
            password: The MongoDB password.
        """
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 30644
        DB = 'AAC'
        COL = 'animals'
        
        try:
            # Initialize the MongoDB client with authentication
            self.client = MongoClient(f'mongodb://{username}:{password}@{HOST}:{PORT}')
            # Access the specific database and collection
            self.database = self.client[DB]
            self.collection = self.database[COL]
        except ServerSelectionTimeoutError as e:
            raise Exception(f"Could not connect to MongoDB: {e}")
        except OperationFailure as e:
            raise Exception(f"Authentication failed: {e}")
            
    def create(self, data):
        """
        Inserts a new document into the collection.

        Args:
            data (dict): The document data to be inserted.

        Returns:
            bool: True if insertion was successful, False otherwise.
        """
        if data:
            try:
                # Insert the document into the collection
                self.collection.insert_one(data)
                return True
            except Exception as e:
                raise Exception(f"An error occurred while inserting data: {e}")
        else:
            raise Exception("Nothing to save, because data parameter is empty")
            
    def read(self, query):
        """
        Retrieves documents from the collection based on a query.

        Args:
            query (dict): The query criteria for retrieval.

        Returns:
            list: A list of documents matching the query.
        """
        if query is not None:
            try:
                # Retrieve documents matching the query
                cursor = self.collection.find(query)
                result = [document for document in cursor]
                return result
            except Exception as e:
                raise Exception(f"An error occurred while reading data: {e}")
        else:
            return []
            
    def update(self, query, new_values):
        """
        Updates documents in the collection based on a query.

        Args:
            query (dict): The query criteria to find documents.
            new_values (dict): The update operations to be applied.

        Returns:
            int: The number of documents modified.
        """
        if query and new_values:
            try:
                # Update the documents matching the query with new data
                update_result = self.collection.update_many(query, {"$set": new_values})
                return update_result.modified_count
            except Exception as e:
                raise Exception(f"An error occurred while updating data: {e}")
        else:
            raise Exception("Query and/or new_values parameters are empty")

    def delete(self, query):
        """
        Deletes documents from the collection based on a query.

        Args:
            query (dict): The query criteria for deletion.

        Returns:
            int: The number of documents deleted.
        """
        if query:
            try:
                # Delete documents matching the query
                delete_result = self.collection.delete_many(query)
                return delete_result.deleted_count
            except Exception as e:
                raise Exception(f"An error occurred while deleting data: {e}")
        else:
            raise Exception("Query parameter is empty")

