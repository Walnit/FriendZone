#!/bin/sh


wget https://github.com/k2-fsa/sherpa-ncnn/releases/download/models/sherpa-ncnn-streaming-zipformer-20M-2023-02-17.tar.bz2
tar xvf sherpa-ncnn-streaming-zipformer-20M-2023-02-17.tar.bz2
rm sherpa-ncnn-streaming-zipformer-20M-2023-02-17.tar.bz2
mv sherpa-ncnn-streaming-zipformer-20M-2023-02-17 english-1

wget https://github.com/k2-fsa/sherpa-ncnn/releases/download/models/sherpa-ncnn-streaming-zipformer-en-2023-02-13.tar.bz2
tar xvf sherpa-ncnn-streaming-zipformer-en-2023-02-13.tar.bz2
rm sherpa-ncnn-streaming-zipformer-en-2023-02-13.tar.bz2
mv sherpa-ncnn-streaming-zipformer-en-2023-02-13 english-2

wget https://github.com/k2-fsa/sherpa-ncnn/releases/download/models/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13.tar.bz2
tar xvf sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13.tar.bz2
rm sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13.tar.bz2
mv sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13 bilingual-1

wget https://github.com/k2-fsa/sherpa-ncnn/releases/download/models/sherpa-ncnn-lstm-transducer-small-2023-02-13.tar.bz2
tar xvf sherpa-ncnn-lstm-transducer-small-2023-02-13.tar.bz2
rm sherpa-ncnn-lstm-transducer-small-2023-02-13.tar.bz2
mv sherpa-ncnn-lstm-transducer-small-2023-02-13 bilingual-2
