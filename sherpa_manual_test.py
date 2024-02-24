import sys

try:
    import sounddevice as sd
except ImportError as e:
    print("Please install sounddevice first. You can use")
    print()
    print("pip install sounddevice")
    print()
    print("to install it")
    sys.exit(-1)

import sherpa_ncnn
from openai import OpenAI
client = OpenAI()

def askChatGPT(transcript: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Read the below transcript of a call. Check for any instance of a caller trying to make the other guess their identity. Strictly answer 'yes' if you think so, and 'no' otherwise"},
            {"role": "user", "content": transcript},
        ]
    )


def create_recognizer():
    # Please replace the model files if needed.
    # See https://k2-fsa.github.io/sherpa/ncnn/pretrained_models/index.html
    # for download links.
    model_type = 'bilingual'
    model_version = 1
    recognizer = sherpa_ncnn.Recognizer(
        tokens=f"./{model_type}-{model_version}/tokens.txt",
        encoder_param=f"./{model_type}-{model_version}/encoder_jit_trace-pnnx.ncnn.param",
        encoder_bin=f"./{model_type}-{model_version}/encoder_jit_trace-pnnx.ncnn.bin",
        decoder_param=f"./{model_type}-{model_version}/decoder_jit_trace-pnnx.ncnn.param",
        decoder_bin=f"./{model_type}-{model_version}/decoder_jit_trace-pnnx.ncnn.bin",
        joiner_param=f"./{model_type}-{model_version}/joiner_jit_trace-pnnx.ncnn.param",
        joiner_bin=f"./{model_type}-{model_version}/joiner_jit_trace-pnnx.ncnn.bin",
        num_threads=4,
    )
    return recognizer


def main():
    recognizer = create_recognizer()
    sample_rate = recognizer.sample_rate
    samples_per_read = int(0.1 * sample_rate)  # 0.1 second = 100 ms
    last_result = ""
    with sd.InputStream(
        channels=1, dtype="float32", samplerate=sample_rate
    ) as s:
        print("Started! Please speak")
        while True:
            samples, _ = s.read(samples_per_read)  # a blocking read
            samples = samples.reshape(-1)
            recognizer.accept_waveform(sample_rate, samples)
            result = recognizer.text
            if last_result != result:
                last_result = result
                print(result)


if __name__ == "__main__":
    devices = sd.query_devices()
    print(devices)
    default_input_device_idx = sd.default.device[0]
    print(f'Use default device: {devices[default_input_device_idx]["name"]}')

    try:
        main()
    except:
        pass
