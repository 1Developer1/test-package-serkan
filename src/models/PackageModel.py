
from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
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
        title = "Image"


class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image],Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


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
    # Parametreyi executorda çekerken name parametresi kullanılır.
    name: Literal["KeepSide"] = "KeepSide"
    value: Union[KeepSideTrue, KeepSideFalse]
    #value parametresinin typini belirtmek için kullanılır.
    type: Literal["object"] = "object"
    #Varsayılan dropdownlist bu şekilde ayarlanır.
    field: Literal["dropdownlist"] = "dropdownlist"
    #Dropdownlistin her elementi için ayrı ayrı class oluşturulur.
    class Config:
        title = "Keep Sides"

# Kullanıcının gireceği parametreleri yapılandırmak için kullanılır.
class Degree(Config):
    #parametrenin yorumu burada açıklanma satırı olarak yazılır.
    """
        Positive angles specify counterclockwise rotation while negative angles indicate clockwise rotation.
    """
    name: Literal["Degree"] = "Degree"
    value: int = Field(ge=-359.0, le=359.0,default=0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[-359, 359]"] = "[-359, 359]"
# burada title parametresi girdilerin başlığını belirler.
    class Config:
        title = "Angle"

# başka paketlerden gelen verileri almak için kullanılır.
# yine aynı şekilde kaç tane input varsa o kadar input yazılır.
class TestPackageSerkanExecutorInputs(Inputs):
    inputImage: InputImage

#kullanıcının gireceği parametrelerini belirlemek için kullanılır.
class TestPackageSerkanExecutorConfigs(Configs):
    degree: Degree
    drawBBox: KeepSideBBox

# modelin UIda kaç tane çıktısı olduğunu belirlemek için kullanılır.
#outpuların keylerinin ilk harfleri küçük olmalıdır. karşılarına gelen valueler de nesnedir
#burada belirttiğimiz outputların yapılandırma classlarını yukarıda tanımlıyoruz.
#burada value objesini tanımlarken name parametresiyle buradaki key ismi aynı olmalıdır.
class TestPackageSerkanExecutorOutputs(Outputs):
    outputImage: OutputImage

# requestler ve responseler her executor için özel olarak oluşturulur.
class TestPackageSerkanExecutorRequest(Request):
    inputs: Optional[TestPackageSerkanExecutorInputs]
    configs: TestPackageSerkanExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class TestPackageSerkanExecutorResponse(Response):
    outputs: TestPackageSerkanExecutorOutputs

# her executor için requestlerini ve responselerini belirlemek için ayrı ayrı executor classı oluşturulur.
class TestPackageSerkanExecutor(Config):
    name: Literal["TestPackageSerkanExecutor"] = "TestPackageSerkanExecutor"
    value: Union[TestPackageSerkanExecutorRequest, TestPackageSerkanExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Package"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }

#package içindeki executor sayısını belirlemek için kullanılır.
class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[TestPackageSerkanExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
# tek executor için schema kullanılır. Eğer birden fazla executor varsa schema yazılmaz.
    class Config:
        title = "Task"
        json_schema_extra = {
            "target": "value"
        }


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["TestPackageSerkan"] = "TestPackageSerkan"
