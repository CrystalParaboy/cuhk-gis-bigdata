import torch 
from torchvision import transforms, datasets 
import torch.nn as nn 
import torch.optim as optim 
import torch.nn.functional as F 
from matplotlib import pyplot as plt 
import time

class MLP_Net (nn.Module): 
	def __init__(self): 
		super().__init__() 
		self.l1 = nn.Linear(28*28, 520) 
		self.l2 = nn.Linear(520, 320) 
		self.l3 = nn.Linear(320, 240) 
		self.l4 = nn.Linear(240, 120) 
		self.l5 = nn.Linear(120, 10)

	def forward(self, x): 
		x = x.view(-1, 784) #flatten the data from(n,1,28,28) -> (n, 784) 
		x1 = F.relu(self.l1(x)) 
		x2 = F.relu(self.l2(x1)) 
		x3 = F.relu(self.l3(x2)) 
		x4 = F.relu(self.l4(x3)) 
		x5 = self.l5(x4)
		return(x5)

test_batch_size =500 
transform = transforms.ToTensor() 
test_data = datasets.MNIST(root='raw_data', train=False, download=True, transform=transform)
test_loader = torch.utils.data.DataLoader(dataset=test_data, batch_size=test_batch_size, shuffle=False)
model = MLP_Net() 
model.load_state_dict(torch.load('mnist_model_nb.pt')) 
def get_device(): 
	device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') 
	return device
device = get_device()
model = model.to(device)
model.eval()



#dataiter = iter(trainset_loader) 
#images, labels = dataiter.next() 
print (type(test_data[0][0])) 
print (test_data[0][0].shape)
plt.imshow(test_data[0][0].numpy().squeeze(), cmap='gray_r');
i=20 #image data 
image = test_data[i][0]
image = image.to(device) 
#do prediction: 
p = model(image.view(-1, 28*28))
print('\nPredict result is :\n', p)
pred_max = p.data.max(1, keepdim=True) 
print("\nPred_max:", pred_max) 
print ('\nThe index of max value is : ', pred_max[1].item()) 
#print ('\nThe index of max value is : ', torch.argmax(p).item()) 
print('\nThe label of of the image is: {} \n'.format(test_data[i][1]))
plt.imshow(image.cpu().numpy()[0], cmap='gray')

def cal_accuracy(): 
	total_count=0 
	correct_count =0 
	for image,label in test_data: 
		image = image.to(device) 
		p = model(image.view(-1, 28*28)) 
		pred_value = torch.argmax(p) 
		if (pred_value == label): 
			correct_count +=1 
		total_count+=1
	print("Total= {0}, Correct = {1}".format(total_count, correct_count)) 
	print("Accuracy ={0}".format(correct_count/total_count))

cal_accuracy()