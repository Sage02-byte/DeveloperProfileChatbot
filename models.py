from pydantic import BaseModel, Field, ConfigDict, model_validator, EmailStr 
from typing import Literal, Optional, List

class DeveloperProfile(BaseModel):

    model_config = ConfigDict(strict=True)

    fullname: str = Field(
        ...,
        min_length=2, 
        description = "User's full or perfered professional name is required"
    )
    age: int = Field(
        ...,
        ge=16,
        le=65,
        description= "User's age must be between 16 to 65"
    )
    email: EmailStr = Field(
        ...,
        description = "User's professional email is required and should be validly formatted"
    )
    primary_role: Literal[
        "Full-Stack Developer",
        "Web Developer",
        "Prompt Engineer",
        "AI Agent"
    ] = Field(
        ...,
        description="User's primary professional roles"
    )
    experience_level: Literal[
        "Junior",
        "Mid",
        "Senior"
    ] = Field(
        ...,
        description = "Porfessional Seniorty level"
    )
    tech_stack: list[str] = Field(
        ...,
        min_length = 1,
        description = "List of mastered technologies, levels, and fields"
    )

    account_type: Literal[
        "professional",
        "enterprise"
    ] = Field(
        ...,
        description = "Type of portfolio account being registered"
    )
    company_name: Optional[str] = Field(
        default = None,
        description = "Company or agency name required ot registered. Forbidden for personal"
    )

    
    @model_validator(mode="after")
    def validate_enterprise_requirements(self):
        if self.account_type == "enterprise" and not self.company_name:
            raise ValueError("Company name is required while registering for an enterprise.")
        if self.account_type == "professional" and self.company_name:
            raise ValueError("Peronal accounts not do not to register compnay names.")
        return self
