
from sdks.novavision.src.helper.package import PackageHelper
from components.Package.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, GrayZeynepExecutorOutputs, GrayZeynepExecutorResponse, GrayZeynepExecutor, OutputImage


def build_response(context):
    outputImage = OutputImage(value=context.image)
    grayZeynepExecutorOutputs= GrayZeynepExecutorOutputs(outputImage=outputImage)
    grayZeynepExecutorResponse = GrayZeynepExecutorResponse(outputs=grayZeynepExecutorOutputs)
    grayZeynepExecutor=GrayZeynepExecutor(value=grayZeynepExecutorResponse)
    configexecutor = ConfigExecutor(value=grayZeynepExecutor)
    packageConfigs = PackageConfigs(executor=configexecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel