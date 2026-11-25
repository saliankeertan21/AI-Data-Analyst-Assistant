from typing import Literal
from pydantic import BaseModel,Field

class BusinessAnalysis(BaseModel):

    business_problem:str=Field(
        description="the main business problem"
    )

    possible_causes:list[str]=Field(
        description="the possible reasons behind the problem"
    )

    relevant_kpis: list[str]=Field(
        description=" KPIs that can help investigate the problem"
    )

    recommendations: list[str] = Field(
            description="Practical actions to address the problem"
        )
    
    priority: Literal["High", "Medium", "Low"] = Field(
            description="The priority level of the business problem"
        )
    
