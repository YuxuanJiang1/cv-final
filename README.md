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
        To get a fast but not that accuracy:
    </p>
<pre>
cd run_scripts/vqa
bash evaluate_vqa_beam.sh val # specify 'val' or 'test'
</pre>
    <p>
        For the best evaluation result at the cost of much slower speed:
    </p>
<pre>
# run on each worker after the distributed configs have been correctly set following the guide in evaluate_vqa_allcand_distributed.sh
cd run_scripts/vqa
bash evaluate_vqa_allcand_distributed.sh val # specify 'val' or 'test'
</pre>
</details>

<br></br>
