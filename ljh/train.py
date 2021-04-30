import torch
import torch.nn as nn
from utils import save_model
from utils import validation
from tqdm import tqdm
from dataset import get_datasets
import segmentation_models_pytorch as smp

def train(num_epochs, model, data_loader, val_loader, criterion, optimizer, saved_dir, val_every, device, file_name):
    print('Start training..')
    best_mIoU = 0
    for epoch in range(num_epochs):
        model.train()
        for step, (images, masks, _) in tqdm(enumerate(data_loader)):
            images = torch.stack(images)  # (batch, channel, height, width)
            masks = torch.stack(masks).long()  # (batch, channel, height, width)

            # gpu 연산을 위해 device 할당
            images, masks = images.to(device), masks.to(device)

            # inference
            if images.size()[0] == 1:
                model.eval()
                outputs = model(images)
                model.train()
            else:
                outputs = model(images)

            # loss 계산 (cross entropy loss)
            loss = criterion(outputs, masks)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # step 주기에 따른 loss 출력
            if (step + 1) % 25 == 0:
                print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'.format(
                    epoch + 1, num_epochs, step + 1, len(data_loader), loss.item()))

        # validation 주기에 따른 loss 출력 및 best model 저장
        if (epoch + 1) % val_every == 0:
            avrg_loss, avrg_mIoU = validation(epoch + 1, model, val_loader, criterion, device)
            if avrg_mIoU > best_mIoU:
                print('Best performance at epoch: {}'.format(epoch + 1))
                print('Save model in', saved_dir)
                best_mIoU = avrg_loss
                save_model(model, saved_dir, file_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
val_every = 1
batch_size = 8   # Mini-batch size
num_epochs = 40
learning_rate = 0.0001
encoder_name = "efficientnet-b3"
saved_dir = "./saved/"+"DeepLabV3Plus/"+encoder_name
train_loader, val_loader, test_loader = get_datasets(batch_size)

model = smp.DeepLabV3Plus(encoder_name=encoder_name, classes=12, encoder_weights="imagenet", activation=None)
model = model.to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(params = model.parameters(), lr = learning_rate, weight_decay=1e-6)
file_name = f"batch_size_{batch_size}_lr_{learning_rate}_crossentropy_adam_wd1e-6"

train(num_epochs, model, train_loader, val_loader, criterion, optimizer, saved_dir, val_every, device, file_name)