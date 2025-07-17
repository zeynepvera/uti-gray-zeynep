
from sdks.novavision.src.helper.package import PackageHelper
from components.GrayZeynep.src.models.PackageModel import ConfigExecutor, OutputImageOne, OutputImageTwo,  PackageModel,PackageConfigs
from components.GrayZeynep.src.models.PackageModel import GrayOutputs, GrayResponse, Gray
from components.GrayZeynep.src.models.PackageModel import FlipOutputs, FlipResponse, Flip

def build_response(context):
    outputImageOne = OutputImageOne(value=context.image)
    grayOutputs = GrayOutputs(outputImageOne=outputImageOne)
    grayResponse = GrayResponse(outputs=grayOutputs)
    gray=Gray(value=grayResponse)
    configexecutor = ConfigExecutor(value=gray)
    packageConfigs = PackageConfigs(executor=configexecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel


def build_response_flip(context):
    outputImageOne = OutputImageOne(value=context.imageOne)
    outputImagetwo = OutputImageTwo(value=context.imageTwo)
    flipOutputs= Flip(outputImageOne=outputImageOne, outputImageTwo=outputImagetwo)
    flipResponse = Flip(outputs=flipOutputs)
    flip=Flip(value=flipResponse)
    configexecutor = ConfigExecutor(value=flip)
    packageConfigs = PackageConfigs(executor=configexecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel
