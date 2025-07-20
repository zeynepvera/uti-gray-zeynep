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


class MorphologyFalse(Config):
    name: Literal["False"] = "False"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Disable"

class MorphologyTrue(Config):
    name: Literal["True"] = "True"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable"

class MorphologyEnabled(Config):
    name: Literal["MorphologyEnabled"] = "MorphologyEnabled"
    value: Union[MorphologyTrue, MorphologyFalse]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Morphology Filter"

class BlurKernel(Config):
    name: Literal["BlurKernel"] = "BlurKernel"
    value: int = Field(ge=1, le=15, default=1)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Blur Kernel Size"

class GrayProcessingBasic(Config):
    blurKernel: BlurKernel
    morphologyEnabled: MorphologyEnabled
    name: Literal["BasicProcessing"] = "BasicProcessing"
    value: Literal["BasicProcessing"] = "BasicProcessing"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Basic Gray Processing"

class GrayScale(Config):
    name: Literal["GrayScale"] = "GrayScale"
    value: int = Field(default=50, ge=0, le=100)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Gray Scale Intensity"

class GrayContrast(Config):
    name: Literal["GrayContrast"] = "GrayContrast"
    value: float = Field(default=1.0, ge=0.1, le=3.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Gray Contrast"

class GrayProcessingAdvanced(Config):
    grayScale: GrayScale
    grayContrast: GrayContrast
    name: Literal["AdvancedProcessing"] = "AdvancedProcessing"
    value: Literal["AdvancedProcessing"] = "AdvancedProcessing"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Advanced Gray Processing"

class GrayProcessingType(Config):
    name: Literal["grayProcessingType"] = "grayProcessingType"
    value: Union[GrayProcessingBasic, GrayProcessingAdvanced]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Gray Processing Method"


# Flip  Configs
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
    name: Literal["flipCode"] = "flipCode"
    value: Union[FlipVertical, FlipHorizontal, FlipBoth]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Flip Mode"

class FlipBrightness(Config):
    name: Literal["Brightness"] = "Brightness"
    value: int = Field(default=0, ge=-100, le=100)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Brightness"

class FlipOperationSimple(Config):
    flipCode: FlipCode
    name: Literal["SimpleFlip"] = "SimpleFlip"
    value: Literal["SimpleFlip"] = "SimpleFlip"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Simple Flip Operation"

class FlipOperationAdvanced(Config):
    flipCode: FlipCode
    brightness: FlipBrightness
    name: Literal["AdvancedFlip"] = "AdvancedFlip"
    value: Literal["AdvancedFlip"] = "AdvancedFlip"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Advanced Flip Operation"

class FlipOperationType(Config):
    name: Literal["flipOperationType"] = "flipOperationType"
    value: Union[FlipOperationSimple, FlipOperationAdvanced]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Flip Operation Method"


# Executor Configs
class GrayInputs(Inputs):
    inputImageOne: InputImageOne

class GrayConfigs(Configs):
    grayProcessingType: GrayProcessingType

class GrayRequest(Request):
    inputs: Optional[GrayInputs]
    configs: GrayConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class GrayOutputs(Outputs):
    outputImageOne: OutputImageOne

class GrayResponse(Response):
    outputs: GrayOutputs

class Gray(Config):
    name: Literal["Gray"] = "Gray"
    value: Union[GrayRequest, GrayResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Gray"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }

class FlipInputs(Inputs):
    inputImageOne: InputImageOne
    inputImageTwo: InputImageTwo

class FlipConfigs(Configs):
    flipOperationType: FlipOperationType

class FlipRequest(Request):
    inputs: Optional[FlipInputs]
    configs: FlipConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class FlipOutputs(Outputs):
    outputImageOne: OutputImageOne
    outputImageTwo: OutputImageTwo

class FlipResponse(Response):
    outputs: FlipOutputs

class Flip(Config):
    name: Literal["Flip"] = "Flip"
    value: Union[FlipRequest, FlipResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Flip "
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }




class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[Gray, Flip]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"


class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["GrayZeynep"] = "GrayZeynep"