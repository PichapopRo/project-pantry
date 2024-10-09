from abc import ABC
from django.db.models import QuerySet
from webpage.models import Recipe

class GetData(ABC):
    """ 
    Abstract base class defining the interface for data retrieval from a recipe API.

    This class serves as a blueprint for concrete implementations that will provide 
    methods to find recipes by their ID or name.
    """
    def find_by_id(self, id: int):
        """
        Find the recipe using the recipe's id.
        
        :param id: the recipe id
        """
        pass
    
    def find_by_name(self, name: str):
        """
        Find the recipe using the recipe's name.
        
        :param name: The recipe name.
        """
        pass


class GetDataProxy(GetData):
    """ 
    Proxy class that controls access to the underlying GetData service.

    This class adds an additional layer of abstraction, allowing for operations 
    such as saving data into database when retrieving recipes which does not
    exist in the database from the API.
    """
    def __init__(self, service: GetData):
        """
        Initialize with a specific service instance for data retrieval.
        
        This method might includes additional logic to save
        the data into the database.
        
        :param service: An instance of a class that implements the GetData interface.
        """
        pass
    
    def find_by_id(self, id: int) -> QuerySet[Recipe]:
        """
        Find the recipe from the api using the recipe's id.
        
        This method might includes additional logic to save
        the data into the database.
        
        :param id: the recipe id
        """
        pass
    
    def find_by_name(self, name: str) -> QuerySet[Recipe]:
        """
        Find the recipe from the api using the recipe's name.
        
        :param name: The recipe name.
        """
        pass
    

class GetDataSpoonacular(GetData):
    """
    Concrete implementation of GetData that interacts with the Spoonacular API.

    This class provides specific methods for retrieving recipes by ID or name 
    using Spoonacular's API endpoints.
    """
    def __init__(self):
        pass
    
    def find_by_id(self, id: int) -> QuerySet[Recipe]:
        """
        Find the recipe from Spoonacular's API using the recipe's ID.
        
        :param id: The recipe id.
        :return: QuerySet containing the Recipe object corresponding to the provided ID.
        """
        pass
    
    def find_by_name(self, name: str) -> QuerySet[Recipe]:
        """
        Find the recipe from Spoonacular's API using the recipe's name.
        
        :param name: The recipe name.
        :return: QuerySet containing the Recipe object corresponding to the provided name.
        """
        pass
