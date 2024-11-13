### github Link:

[GitHub - zzx135790/FFW](https://github.com/zzx135790/FFW)



### System Architecture


![](https://cdn.nlark.com/yuque/0/2024/png/42460983/1731482079570-bc07442c-9e7e-4064-96ff-85eb27ae37cd.png)



### System layer

![](https://cdn.nlark.com/yuque/0/2024/png/42460983/1731482059599-15706df2-d449-4158-b8c7-f4ae3527ee93.png)

### Data layer

![](https://cdn.nlark.com/yuque/0/2024/png/42460983/1731482096906-6aa51e14-1eea-42c1-b989-aeb2d0188c56.png)



### model layer

#### classification model

![](https://cdn.nlark.com/yuque/0/2024/png/42460983/1731482147770-6005a24e-6512-47ba-a76e-7ed6a3ad2bb8.png)

#### Detection model

![](https://cdn.nlark.com/yuque/0/2024/png/42460983/1731482165787-6e003d79-8adf-4b02-a35b-fd58f6eeb735.png)

#### MMF(Independent construction)

![](https://cdn.nlark.com/yuque/0/2024/png/42460983/1731482180512-aa323884-fb42-4ea9-a940-a4bdb92d735b.png)

### Web layer

![](https://cdn.nlark.com/yuque/0/2024/png/42460983/1731482294585-9d792561-5acd-4f5a-877d-127af4c103e1.png)



###  Technical Innovations  

+ **Single Model Optimization**
+ **Data Augmentation and Cleaning**: Enhances data quality by generating a high-quality dataset.
+ **K-means Clustering + Genetic Algorithm**: Used to determine multi-scale and anchor parameters.
+ **Comparative Experiments**: Employed to establish the learning rate decay strategy.
+ **Deformable Pooling Layer**: Allows the model to better capture manhole cover features of various shapes.
+ **Online Hard Example Mining (OHEM)**: Increases training intensity for images with similar features or difficult-to-recognize images.
+ **Coarse-to-Fine Approach**: Refines target positioning and detection for better accuracy.
+ **Global Context**: Allows the model to consider the global environment when identifying targets.
+ **Custom MMF Model**: A self-developed Multi-Model Fusion model that accounts for the accuracy differences of each detection model across categories and sensitivity to varying manhole cover sizes, resulting in a more accurate fusion output.
+ **New Bounding Box Fusion Algorithm**: Instead of simply retaining the highest scoring bounding box, this method first collects individual model scores, converts them to a unified multi-model scoring system, and then fuses boxes based on these scores. This approach more comprehensively considers the complex scoring landscape of multiple models, producing a more effective final fusion box.
+ **Distributed Computing Pool:** We specifically designed a distributed computing pool. This system flexibly allocates computational resources and automatically distributes images awaiting recognition to available resources. This measure improves system performance and effectively addresses the "long-tail" problem.

