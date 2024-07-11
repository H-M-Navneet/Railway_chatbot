import torch

print("Torch version:",torch.__version__)

print("Is CUDA enabled?",torch.cuda.is_available())

import torchvision

print("Torchvision version:",torchvision.__version__)