# Timeline


## 3일차(4/29)

- HRNet 사용 위해 코드 뜯어보고 적용시키기 시작.. 
  - https://github.com/HRNet/HRNet-Semantic-Segmentation
  - CONFIG 등 파라미터 수정 위해 구조 파악이 시급

- object detection augmentation 방법 논문 대충 읽음 https://arxiv.org/abs/2102.00221 
  - 일반 image augmentatioon 보다 심화된 augmentation 가능(모델 구조 이용)
  ![image](https://user-images.githubusercontent.com/43736669/116516294-6ab4d300-a908-11eb-822c-39705ad3c0a6.png)

## 4일차(4/30 금)
- HRNet 포기(Pretrain 사용하기 위해 써야 하는 모델이 너무 무거움)
 - pretrained X, 최대한 가볍게 돌린 모델 20ep 기준 Valid mIoU 0.2xx대 나옴
- DeeplabV3+기반 코드 재작성
- 모듈화 완료

## 5일차(5/1 토)
- wandb 버전관리 시작
- DeeplabV3+(EfficientNet-b3 Encoder) 학습 시작(모델은 우선 이걸로 고정할듯)
- 대회의 leaderboard 산출 방식에 맞는 loss를 찾아보자..
 - 영성님의 TverskyLoss?
 - Weighted CE?