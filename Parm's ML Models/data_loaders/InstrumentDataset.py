import random
import torch
from PIL import Image
import torchvision.transforms as T

class InstrumentDataset(torch.utils.data.Dataset):
    def __init__(self, dataframe, apply_occlusion=False):
        self.df = dataframe
        self.apply_occlusion = apply_occlusion

        self.transform = T.Compose([
            T.Resize((224, 224)),
            T.ToTensor(),
            T.Normalize(
                mean=(0.485, 0.456, 0.406),
                std=(0.229, 0.224, 0.225)
            )
        ])

    def occlude(self, image):
        # image = tensor [C, H, W]
        _, H, W = image.shape

        # random square size (10–30% of image)
        size = random.randint(int(0.1 * W), int(0.3 * W))

        x = random.randint(0, W - size)
        y = random.randint(0, H - size)

        image[:, y:y+size, x:x+size] = 0  # black patch

        return image

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]

        image = Image.open(row["image_path"]).convert("RGB")
        image = self.transform(image)

        if self.apply_occlusion:
            image = self.occlude(image)

        label = row["label"]

        return image, label