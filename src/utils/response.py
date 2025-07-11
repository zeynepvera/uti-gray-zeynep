
from sdks.novavision.src.helper.package import PackageHelper
from components.GrayZeynep.src.models.PackageModel import ConfigExecutor, OutputImageOne, OutputImageTwo,  PackageModel,PackageConfigs
from components.GrayZeynep.src.models.PackageModel import GrayZeynepExecutorOutputs, GrayZeynepExecutorResponse, GrayZeynepExecutor
from components.GrayZeynep.src.models.PackageModel import FlipExecutorOutputs, FlipExecutorResponse, FlipExecutor

def build_response(context):
    outputImage = OutputImageOne(value=context.image)
    grayZeynepExecutorOutputs= GrayZeynepExecutorOutputs(outputImage=outputImage)
    grayZeynepExecutorResponse = GrayZeynepExecutorResponse(outputs=grayZeynepExecutorOutputs)
    grayZeynepExecutor=GrayZeynepExecutor(value=grayZeynepExecutorResponse)
    configexecutor = ConfigExecutor(value=grayZeynepExecutor)
    packageConfigs = PackageConfigs(executor=configexecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel


def build_response_flip(context):
    outputImageOne = OutputImageOne(value=context.image)
    outputImagetwo = OutputImageTwo(value=context.image)
    flipExecutorOutputs= FlipExecutorOutputs(outputImageOne=outputImageOne, outputImageTwo=outputImagetwo)
    flipExecutorResponse = FlipExecutorResponse(outputs=flipExecutorOutputs)
    flipExecutor=FlipExecutor(value=flipExecutorResponse)
    configexecutor = ConfigExecutor(value=flipExecutor)
    packageConfigs = PackageConfigs(executor=configexecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel
