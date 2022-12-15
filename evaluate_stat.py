import argparse
import itertools
from pathlib import Path
import json
import pandas as pd
from pandas.api.types import CategoricalDtype
import base64
from io import BytesIO
from PIL import Image, ImageFile
from torchvision import transforms
from image_visualization import *

ImageFile.LOAD_TRUNCATED_IMAGES = True
ImageFile.MAX_IMAGE_PIXELS = None
ImageFile.MAX_IMAGE_PIXELS = None

plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams["savefig.bbox"] = 'tight'
plt.rcParams["savefig.pad_inches"] = 0.


def bstr_to_image(bstr):
    return Image.open(BytesIO(base64.urlsafe_b64decode(bstr)))


def evaluate_stat(results, save_path, sample_n=100, n_cols=5, seed=0):
    results = pd.DataFrame(results)

    class_label_type = CategoricalDtype(
        categories=["yes/no", "number", "other"], ordered=True)
    results['class_label'] = results['class_label'].astype(class_label_type)

    subset_masks = {'all': [True] * len(results)}
    for label in class_label_type.categories:
        subset_masks[label] = results['class_label'] == label

    for subset_name, subset_mask in subset_masks.items():
        scores = results['score'][subset_mask]
        score_sum = scores.sum()
        score_cnt = len(scores)
        score_mean = score_sum / score_cnt
        print(f"{subset_name} score mean: {score_sum:.1f} / {score_cnt} = {score_mean:.4f}")

        esc_subset_name = subset_name.replace('/', '-')
        path = save_path / esc_subset_name
        path.mkdir(parents=True, exist_ok=True)
        error_results = results[subset_mask & (results['score'] == 0)]
        error_results_samples = error_results.sample(sample_n, random_state=seed).sort_values('question_id')

        for sample_idx, sample in error_results_samples.iterrows():
            image = bstr_to_image(sample['image'])
            image.save(path / f"{sample['question_id']}.png")

        n_rows = get_n_rows(len(error_results_samples), n_cols)
        fig, axs, image_width = image_subplots(n_rows, n_cols)
        for ax in itertools.chain.from_iterable(axs):
            ax.axis("off")
        all_axs = itertools.chain.from_iterable(axs)
        for (sample_idx, sample), ax in zip(error_results_samples.iterrows(), all_axs):
            image = bstr_to_image(sample['image'])
            ax.imshow(image)
            ref_dict = sample['ref_dict']
            ref_str = ' '.join((
                ref if conf == 1 else f'{ref}:{conf}'
                for ref, conf in sorted(
                    ref_dict.items(),
                    key = lambda item: (-item[1], item[0]))))
            caption = [
                f"{bf('question')}: {sample['question']}",
                f"{bf('reference answer')}: {ref_str}",
                f"{bf('model prediction')}: {sample['answer']}",
            ]
            add_caption(ax, caption, image_width=image_width)

        plt.savefig(path / f"figure_{esc_subset_name}.png")
        plt.clf()


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--result', type=Path,
        default=Path('results/vqa_val_beam/val_predict.json'),
        help='path to the json file of evaluation results')
    argparser.add_argument(
        '--sample_n', type=int,
        default=8)
    argparser.add_argument(
        '--n_cols', type=int,
        default=4)
    argparser.add_argument(
        '--seed', type=int,
        default=0)
    args = argparser.parse_args()
    with open(args.result, 'r') as f:
        results = json.load(f)
    evaluate_stat(
        results, args.result.parent / 'errors',
        sample_n=args.sample_n, n_cols=args.n_cols,
        seed=args.seed)
