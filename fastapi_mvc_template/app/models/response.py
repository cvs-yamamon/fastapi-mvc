# -*- coding: utf-8 -*-
"""Response models."""
from typing import Dict,  Any
from http import HTTPStatus

from pydantic import BaseModel, root_validator


class ErrorModel(BaseModel):
    """Error model definition.

    Attributes:
        code(int): HTTP error status code.
        message(str): Detail on HTTP error.
        status(str): HTTP error reason-phrase as per in RFC7235. NOTE! Set
            automatically based on HTTP error status code.

    Raises:
        pydantic.error_wrappers.ValidationError: If any of provided attribute
            doesn't pass type validation.

    """

    code: int
    message: str

    @root_validator(pre=False)
    def _set_status(cls, values: dict) -> dict:
        """This is a validator that sets the status field value based on the
        the code value.

        Args:
            values(dict): Stores the attributes of the ErrorModel object.

        Returns:
            dict: The attributes of the ErrorModel object with the status field.

        """
        values["status"] = HTTPStatus(values["code"]).name
        return values

    class Config:
        """Config sub-class needed to extend/override the generated JSON schema.

        More details can be found in pydantic documentation:
        https://pydantic-docs.helpmanual.io/usage/schema/#schema-customization

        """

        @staticmethod
        def schema_extra(schema: Dict[str, Any]) -> None:
            """Method for more fine-grained control to post-process the schema.

            Mathod can have one or two positional arguments. The first will be
            the schema dictionary. The second, if accepted, will be the model
            class. The callable is expected to mutate the schema dictionary
            in-place; the return value is not used.

            Args:
                schema(Dict[str, Any]): The schema dictionary.

            """
            # Override schema description, by default is taken from docstring.
            schema["description"] = "Error model."
            # Add status to schema properties.
            schema["properties"].update(
                {"status": {"title": "Status", "type": "string"}}
            )
            schema["required"].append("status")


class ErrorResponse(BaseModel):
    """Error response model definition.

    Attributes:
        error(ErrorModel): ErrorModel class object instance.

    Raises:
        pydantic.error_wrappers.ValidationError: If any of provided attribute
            doesn't pass type validation.

    """

    error: ErrorModel

    def __init__(self, **kwargs):
        """"""
        # Neat trick to still use kwargs on ErrorResponse model.
        super().__init__(error=ErrorModel(**kwargs))

    class Config:
        """Config sub-class needed to extend/override the generated JSON schema.

        More details can be found in pydantic documentation:
        https://pydantic-docs.helpmanual.io/usage/schema/#schema-customization

        """

        @staticmethod
        def schema_extra(schema: Dict[str, Any]) -> None:
            """Method for more fine-grained control to post-process the schema.

            Mathod can have one or two positional arguments. The first will be
            the schema dictionary. The second, if accepted, will be the model
            class. The callable is expected to mutate the schema dictionary
            in-place; the return value is not used.

            Args:
                schema(Dict[str, Any]): The schema dictionary.

            """
            # Override schema description, by default is taken from docstring.
            schema["description"] = "Error response model."
