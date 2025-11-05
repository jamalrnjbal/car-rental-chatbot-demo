"""
Pydantic models for structured chatbot outputs using Instructor
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal, Union
from enum import Enum


class CarCategory(str, Enum):
    """Available car categories"""
    ECONOMY = "Economy"
    COMPACT_SUV = "Compact SUV"
    MID_SIZE_SUV = "Mid-Size SUV"
    FULL_SIZE_SUV = "Full-Size SUV"
    LUXURY = "Luxury"
    MINIVAN = "Minivan"
    ELECTRIC = "Electric"
    PICKUP_TRUCK = "Pickup Truck"
    SPORTS = "Sports"


class FuelType(str, Enum):
    """Available fuel types"""
    GASOLINE = "Gasoline"
    HYBRID = "Hybrid"
    ELECTRIC = "Electric"


class CarSearchCriteria(BaseModel):
    """
    Search criteria for filtering available rental cars.
    Use this when a customer specifies preferences like budget, passenger count, or vehicle type.
    """
    max_price: Optional[float] = Field(
        None,
        description="Maximum daily rental price in dollars (e.g., 50.00)",
        gt=0
    )
    min_passengers: Optional[int] = Field(
        None,
        description="Minimum number of passengers the car must accommodate",
        ge=1,
        le=15
    )
    category: Optional[CarCategory] = Field(
        None,
        description="Type of car (e.g., Economy, SUV, Luxury)"
    )
    fuel_type: Optional[FuelType] = Field(
        None,
        description="Preferred fuel type (Gasoline, Hybrid, or Electric)"
    )

    class Config:
        use_enum_values = True


class GetCarInventory(BaseModel):
    """
    Request to retrieve all available rental cars.
    Use this when a customer asks to see all available cars or browse the inventory.
    """
    retrieve_all: Literal[True] = Field(
        default=True,
        description="Flag to retrieve complete car inventory"
    )


class DirectResponse(BaseModel):
    """
    Direct text response without any function calling.
    Use this for greetings, general questions, or when no car data is needed.
    """
    message: str = Field(
        description="The chatbot's response message to the user"
    )


class ChatbotAction(BaseModel):
    """
    The action the chatbot should take based on user input.
    This is a discriminated union of all possible actions.
    """
    action_type: Literal["search_cars", "get_inventory", "direct_response"] = Field(
        description="Type of action to perform"
    )
    search_criteria: Optional[CarSearchCriteria] = Field(
        None,
        description="Search parameters when action_type is 'search_cars'"
    )
    get_inventory: Optional[GetCarInventory] = Field(
        None,
        description="Inventory request when action_type is 'get_inventory'"
    )
    response: Optional[str] = Field(
        None,
        description="Direct response text when action_type is 'direct_response'"
    )
