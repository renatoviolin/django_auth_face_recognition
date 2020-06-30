from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
mtcnn = MTCNN(device=device, keep_all=True)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
print(f'running on {device}')


def generate_emb(file):
    img = Image.open(file)
    x_aligned, prob = mtcnn(img, return_prob=True)
    if len(prob) == 1 and prob > 0.9:  # only one person
        e = resnet(torch.Tensor(x_aligned[0]).unsqueeze(0)).detach().cpu().numpy()
        return e
    return None


def get_similarity(source, target_array):
    if len(target_array) > 0:
        img = Image.open(source)
        x_aligned, prob = mtcnn(img, return_prob=True)
        if len(prob) == 1:  # only one person
            e = resnet(torch.Tensor(x_aligned[0]).unsqueeze(0)).detach().cpu().numpy()
            _scores, _idx = torch.tensor(cosine_similarity(e, target_array)).topk(1)
            score = _scores.item()
            idx = _idx.item()
            if score >= 0.9:
                return score, idx
    return None, None
