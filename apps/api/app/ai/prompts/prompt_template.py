from dataclasses import dataclass

@dataclass(frozen=True)
class PromptTemplate:
    """
    Template used to construct prompts for the LLM
    """
    
    system_prompt : str
    user_prompt : str 
    