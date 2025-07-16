from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config

class InputImageOne(Input):
    name: Literal["inputImageOne"] = "inputImageOne"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Input Image One"


class InputImageTwo(Input):
    name: Literal["inputImageTwo"] = "inputImageTwo"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Input Image Two"


class OutputImageOne(Output):
    name: Literal["outputImageOne"] = "outputImageOne"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Output Image One"


class OutputImageTwo(Output):
    name: Literal["outputImageTwo"] = "outputImageTwo"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Output Image Two"


class GrayTypeNormal(Config):
    name: Literal["Normal"] = "Normal"
    alpha: int = Field(default=1, ge=0, le=5)
    beta: int = Field(default=0, ge=-100, le=100)
    value: Literal["Normal"] = "Normal"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Normal Gray"


class GrayTypeWeighted(Config):
    name: Literal["Weighted"] = "Weighted"
    red_weight: float = Field(default=0.299, ge=0.0, le=1.0)
    green_weight: float = Field(default=0.587, ge=0.0, le=1.0)
    blue_weight: float = Field(default=0.114, ge=0.0, le=1.0)
    blur_kernel: int = Field(default=3, ge=1, le=15)
    value: Literal["Weighted"] = "Weighted"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Weighted Gray"



class GrayMethod(Config):
    name: Literal["grayMethod"] = "grayMethod"
    value: Union[GrayTypeNormal, GrayTypeWeighted]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Gray Method"


class KeepSideFalse(Config):
    name: Literal["False"] = "False"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Disable"

class KeepSideTrue(Config):
    name: Literal["True"] = "True"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable"

class KeepSideBBox(Config):
    """
        Rotate image without catting off sides.
    """
    name: Literal["KeepSide" ] = "KeepSide"
    value: Union[KeepSideTrue, KeepSideFalse]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Keep Sides"

class Degree(Config):
    """
        Positive angles specify counterclockwise rotation while negative angles indicate clockwise rotation.
    """
    name: Literal["Degree"] = "Degree"
    value: int = Field(ge=-359.0, le=359.0,default=0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Angleee"


class GrayZeynepExecutorInputs(Inputs):
    inputImageOne: InputImageOne


class GrayZeynepExecutorConfigs(Configs):
    degree: Degree
    drawBBox: KeepSideBBox
    grayMethod: GrayMethod

class GrayZeynepExecutorRequest(Request):
    inputs: Optional[GrayZeynepExecutorInputs]
    configs: GrayZeynepExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class GrayZeynepExecutorOutputs(Outputs):
    outputImageOne: OutputImageOne

class GrayZeynepExecutorResponse(Response):
    outputs: GrayZeynepExecutorOutputs

class GrayZeynepExecutor(Config):
    name: Literal["GrayZeynepExecutor"] = "GrayZeynepExecutor"
    value: Union[GrayZeynepExecutorRequest, GrayZeynepExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Package"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class FlipModeSimple(Config):
    name: Literal["Simple"] = "Simple"
    flip_code: Union["FlipVertical", "FlipHorizontal", "FlipBoth"]
    contrast: float = Field(default=1.0, ge=0.1, le=3.0)
    value: Literal["Simple"] = "Simple"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Simple Flip"


class FlipModeAdvanced(Config):
    name: Literal["Advanced"] = "Advanced"
    flip_code: Union["FlipVertical", "FlipHorizontal", "FlipBoth"]
    gamma: float = Field(default=1.0, ge=0.1, le=3.0)
    noise_level: int = Field(default=0, ge=0, le=50)
    blur_strength: int = Field(default=0, ge=0, le=10)
    value: Literal["Advanced"] = "Advanced"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Advanced Flip"

class FlipProcessType(Config):
    name: Literal["flipProcessType"] = "flipProcessType"
    value: Union[FlipModeSimple, FlipModeAdvanced]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Process Type"


class FlipVertical(Config):
    name: Literal["Vertical"] = "Vertical"
    value: Literal[0] = 0
    type: Literal["number"] = "number"
    field: Literal["option"] = "option"

    class Config:
        title = "Vertical Flip"

class FlipHorizontal(Config):
    name: Literal["Horizontal"] = "Horizontal"
    value: Literal[1] = 1
    type: Literal["number"] = "number"
    field: Literal["option"] = "option"

    class Config:
        title = "Horizontal Flip"

class FlipBoth(Config):
    name: Literal["Both"] = "Both"
    value: Literal[-1] = -1
    type: Literal["number"] = "number"
    field: Literal["option"] = "option"

    class Config:
        title = "Vertical + Horizontal Flip"

class FlipCode(Config):
    """
       Select flip angle from dropdown options.

    """
    name: Literal["flipCode"] = "flipCode"
    value: Union[FlipVertical, FlipHorizontal, FlipBoth]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Flip Mode"


class FlipBrightness(Config):
    name: Literal["Brightness"] = "Brightness"
    value: int = Field(default=0, ge= -100, le=100)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title= "Brightness "


class FlipExecutorInputs(Inputs):
    inputImageOne: InputImageOne
    inputImageTwo: InputImageTwo



class FlipExecutorConfigs(Configs):

    flipCode: FlipCode
    brightness: FlipBrightness
    flipProcessType: FlipProcessType


class FlipExecutorRequest(Request):
    inputs: Optional[FlipExecutorInputs]
    configs: FlipExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class FlipExecutorOutputs(Outputs):
    outputImageOne: OutputImageOne
    outputImageTwo: OutputImageTwo

class FlipExecutorResponse(Response):
    outputs: FlipExecutorOutputs



class FlipExecutor(Config):
    name: Literal["FlipExecutor"] = "FlipExecutor"
    value: Union[FlipExecutorRequest, FlipExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Package"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }





class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[GrayZeynepExecutor, FlipExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Choose the Model"

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["GrayZeynep"] = "GrayZeynep"
