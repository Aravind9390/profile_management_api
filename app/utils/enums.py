from enum import Enum

class GenderEnum(str, Enum):
    male = "Male"
    female = "Female"
    others = "Others"