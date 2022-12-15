<!---
Copyright 2022 The OFA-Sys Team. 
All rights reserved.
This source code is licensed under the Apache 2.0 license found in the LICENSE file in the root directory.
-->


# Requirements
* python 3.7.4
* pytorch 1.8.1
* torchvision 0.9.1
* JAVA 1.8 (for COCO evaluation)
<br></br>

# Installation
```bash
pip install -r requirements.txt
```
<br></br>


## Evaluate on Visual Question Answering
Data are released [here] (https://ood.hpc.nyu.edu/pun/sys/files/fs/home/ww2135/OFA/)

Here we provide the finetuning and inference codes to reproduce the VQAv2 result reported in our paper (**test-std 80.02**). We believe much improvement on accuracy can still be achieved based on this codebase :)
<details>
    <summary><b>1. Prepare the Dataset & Checkpoints</b></summary>
    <p>
        Download data (see <a href="datasets.md">datasets.md</a>) and models (see <a href="checkpoints.md">checkpoints.md</a>) and put them in the correct directory. The dataset zipfile <code>vqa_data.zip</code> is around 100G and the decompressed data costs around 135G disk storage, which contains the training, validation and testing samples together with other necessary data resources. (Since <code>vqa_data.zip</code> is large in size, we have also provided chunked parts of the dataset files for more convenient and stable downloading. Please refer to <a href="https://github.com/OFA-Sys/OFA/issues/68#issuecomment-1096837349">issue #68</a>.) Following common practice, VG-QA samples are also included in the training data. To adapt to the seq2seq paradigm of OFA, we transform original VQA training questions with multiple golden answers into multiple training samples. For the original VQA validation set, we keep around 10k samples for our validation and utilize the other samples for training. Each line of the dataset represents a VQA sample with the following format. The information of question-id, image-id, question, answer (with confidence), predicted object labels (taken from <a href="https://github.com/pzzhang/VinVL">VinVL</a>, slightly brings around +0.1 accuracy improvement), image base64 string are separated by tabs. 
    </p>
<pre>
79459   79459   is this person wearing shorts?  0.6|!+no    house&&short&&...&&sky  /9j/4AAQS...tigZ/9k=
</pre>
    <p>
        For fine-tuning on customed VQA-formulated tasks, please refer to issue <a href="https://github.com/OFA-Sys/OFA/issues/76">#76</a>, <a href="https://github.com/OFA-Sys/OFA/issues/105">#105</a> and <a href="https://github.com/OFA-Sys/OFA/issues/73">#73</a> for more information.
    </p>
</details>
<details>
    <summary><b>2. Shuffle the Training Data</b></summary>
    <p>
        (Optional, but achieves better finetuning accuracy): If the disk storage is sufficient, we recommend to prepare the shuffled training data for each epoch in advance. In our experiments, we use shuffling which brings around <b>+0.3</b> improvement on VQA accuracy.
    </p>
<pre>
cd dataset/vqa_data
ln vqa_train.tsv vqa_train_1.tsv
for idx in `seq 1 9`;do shuf vqa_train_${idx}.tsv > vqa_train_$[${idx}+1].tsv;done # each file is used for an epoch
</pre>
</details>
<details>
    <summary><b>3. Finetuning</b></summary>
    <p>
        In our experiments, the VQA finetuning is performed on 4 8-A100-GPU servers (<i>with RDMA</i>). Here provides the finetuning script <code>train_vqa_distributed.sh</code>, which supports multi-server distributed training (as well as single-server training). Please refer to the comments in the beginning of the script and set the configs correctly according to your distribution environment. If you have shuffled the training data in the previous step, please correctly specify the training data path following the guide in the script comments. <b>The command should be run on each worker.</b> 
    </p>
<pre>
# run on each worker after the distributed and data configs have been correctly set following the guide in train_vqa_distributed.sh 
cd run_scripts/vqa
bash train_vqa_distributed.sh 
</pre>
    <p>
        In our experiments, the finetuning costs around 36 hours (for 12 epochs). After each epoch, an evaluation on validation set is performed. The best validation accuracy during finetuning will be around 80.8. The log is saved in <code>${log_dir}</code>.
    </p>
    <p>
        <i>(Update on validation time-cost)</i> As will be mentioned in the <i>4. Inference</i> section, we prepare 2 types of inference: beam-search and all-candidate inference. By default, all-candidate inference is used for validation during fine-tuning, which achieves better accuracy but costs much time. Now we have added a new option in the training scripts called <code>--val-inference-type</code> to switch the validation inference type during fine-tuning. If you feel the validation takes too long, you can refer to <a href="https://github.com/OFA-Sys/OFA/pull/79">PR #79</a> to activate beam-search validation, which significantly takes much less time, with around 0.5-0.6 validation score degradation compared with all-candidate validation.
    </p>
</details>
<details>
    <summary><b>4. Inference</b></summary>
    <p>
        We provide 2 types of inference, <b>beam-search</b> (much faster but gets sub-optimal accuracy) and <b>all-candidate evaluation</b> (slower but best accuracy). <br></br>
        For beam-search inference, use the script <code>evaluate_vqa_beam.sh</code>. Refer to the command below. The inference on test set costs around 16 GPU hours. After inference on test set, the result JSON file will be dumped in the <code>${result_path}</code> defined in the shell script. You can submit the result <code>test_predict.json</code> to <a href="https://eval.ai/web/challenges/challenge-page/830/overview">EvalAI</a>. Using our released finetuned checkpoint, beam-search inference will get 80.15 validation accuracy, 79.36 test-dev accuracy and 79.48 test-std accuracy (around 0.6 lower than all-candidate evaluation).
    </p>
<pre>
cd run_scripts/vqa
bash evaluate_vqa_beam.sh val # specify 'val' or 'test'
</pre>
    <p>
        For all-candidate evaluation, we recommend to use the distributed script <code>evaluate_vqa_allcand_distributed.sh</code>. Please refer to the guide in the script to set the distributed configs before running. The result JSON file will be dumped in the <code>${result_path}</code> defined in the shell script of rank-0 server. All-candidate evaluation computes scores on all the candidate answers in the VQA dataset, which achieves <b>80.82</b> validation accuracy, <b>79.87</b> test-dev accuracy and <b>80.02</b> test-std accuracy, reproducing our reported results in the paper. However, the inference on test set costs around 1k GPU hours, which is much slower.
    </p>
<pre>
# run on each worker after the distributed configs have been correctly set following the guide in evaluate_vqa_allcand_distributed.sh
cd run_scripts/vqa
bash evaluate_vqa_allcand_distributed.sh val # specify 'val' or 'test'
</pre>
</details>

<br></br>
