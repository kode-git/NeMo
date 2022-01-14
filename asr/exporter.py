
import nemo.collections.asr as nemo_asr
from omegaconf import OmegaConf
from asr import ASR


QUARTZNET_MODEL = "QuartzNet15x5Base-En"
neMo_file = f'{QUARTZNET_MODEL}.nemo'
onnx_file = f'{QUARTZNET_MODEL}.onnx'
config_yaml = f'{QUARTZNET_MODEL}.yaml'


asr_model = ASR()
asr_model.downloadModel(asr_model.model_name)
asr_model.model.save_to(neMo_file)
modelReco = nemo_asr.models.ASRModel.restore_from(restore_path=neMo_file)
modelReco.export(onnx_file, onnx_opset_version=12)

modelReco = nemo_asr.models.ASRModel.restore_from(restore_path=neMo_file, return_config = True) # restore config is set to True
textfile = open(config_yaml, "w")
textfile.write(str(OmegaConf.to_yaml(modelReco)))
textfile.close()