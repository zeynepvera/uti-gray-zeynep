from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config
##
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


# GrayZeynep Executor Configs
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
    name: Literal["KeepSide"] = "KeepSide"
    value: Union[KeepSideTrue, KeepSideFalse]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Keep Sides"

class Degree(Config):
    name: Literal["Degree"] = "Degree"
    value: int = Field(ge=-359.0, le=359.0, default=0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Angleee"

class GrayBasicConfig(Config):
    name: Literal["grayBasicConfig"] = "grayBasicConfig"
    value: Union[Degree, KeepSideBBox]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Basic Configuration"

class GrayProcessingBasic(Config):
    degree: Degree
    keepSide: KeepSideBBox
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

class GrayAdvancedConfig(Config):
    name: Literal["grayAdvancedConfig"] = "grayAdvancedConfig"
    value: Union[GrayScale, GrayContrast]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Advanced Configuration"

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


# Flip Executor Configs
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

class FlipRotationAngle(Config):
    name: Literal["FlipRotationAngle"] = "FlipRotationAngle"
    value: int = Field(default=90, ge=0, le=360)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Rotation Angle"

class FlipQuality(Config):
    name: Literal["FlipQuality"] = "FlipQuality"
    value: bool = Field(default=True)
    type: Literal["bool"] = "bool"
    field: Literal["checkbox"] = "checkbox"

    class Config:
        title = "High Quality Processing"

class FlipSimpleConfig(Config):
    name: Literal["flipSimpleConfig"] = "flipSimpleConfig"
    value: FlipCode
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Simple Configuration"

class FlipAdvancedConfig(Config):
    name: Literal["flipAdvancedConfig"] = "flipAdvancedConfig"
    value: Union[FlipBrightness, FlipRotationAngle, FlipQuality]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Advanced Configuration"

class FlipOperationSimple(Config):
    flipSimpleConfig: FlipSimpleConfig
    name: Literal["SimpleFlip"] = "SimpleFlip"
    value: Literal["SimpleFlip"] = "SimpleFlip"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Simple Flip Operation"

class FlipOperationAdvanced(Config):
    flipAdvancedConfig: FlipAdvancedConfig
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
class GrayZeynepExecutorInputs(Inputs):
    inputImageOne: InputImageOne

class GrayZeynepExecutorConfigs(Configs):
    grayProcessingType: GrayProcessingType

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
        title = "Gray Zeynep Executor"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }

class FlipExecutorInputs(Inputs):
    inputImageOne: InputImageOne
    inputImageTwo: InputImageTwo

class FlipExecutorConfigs(Configs):
    flipOperationType: FlipOperationType
    flipSimpleConfig: Optional[FlipSimpleConfig]
    flipAdvancedConfig: Optional[FlipAdvancedConfig]

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
        title = "Flip Executor"
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
        title = "Task"

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["GrayZeynep"] = "GrayZeynep"
