from pydantic import BaseModel
from typing import Optional

class WebsiteCreate(BaseModel):
    website_name: str
    domain: Optional[str] = None
    website_url: str
    website_licence: Optional[str] = None

class WebsiteUpdate(BaseModel):
    website_name: Optional[str] = None
    domain: Optional[str] = None
    website_url: Optional[str] = None
    website_licence: Optional[str] = None