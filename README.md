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
Data are released [here](https://ood.hpc.nyu.edu/pun/sys/files/fs/home/ww2135/OFA/)

To run the evaluate code of inference:
   
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
