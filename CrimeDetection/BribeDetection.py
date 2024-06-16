import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import gradio as gr
from transformers import pipeline

def classifier(inputs):
  device = "cuda:0" if torch.cuda.is_available() else "cpu"
  torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

  model_id = "openai/whisper-large"

  model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
  model.to(device)

  processor = AutoProcessor.from_pretrained(model_id)

  pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=16,
    return_timestamps=True,
    torch_dtype=torch_dtype,
    device=device,
)


  result = pipe(inputs)
  text = result["text"]


  pipe = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
  class_names = ["Giving Bribe", "Asking for bribe", "Planning escape","Abuse","Normal Conversation","Threatening Officer"]
  # speech = transcriber(result["text"])
  return pipe(text, class_names, hypothesis_template="The sentiment of this text is {}.")

iface = gr.Interface(
    fn=classifier,
    inputs= gr.Audio(type="filepath"),
    outputs="text",
    live=True,
    title="Dialogue LLM"
)

iface.launch(debug=True)
