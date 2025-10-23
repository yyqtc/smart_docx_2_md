from pydantic import BaseModel, Field

from typing_extensions import TypedDict
from typing import Union, List, Tuple, Annotated

import operator

class ProjectStruct(TypedDict):
    project_name: str
    image_dir_path: str
