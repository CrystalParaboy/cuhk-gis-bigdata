import torch 
from torchvision import transforms, datasets 
import torch.nn as nn 
import torch.optim as optim 
import torch.nn.functional as F 
from matplotlib import pyplot as plt 
import time
#pip install ipywidgets

transform = transforms.ToTensor() 
train_data = datasets.MNIST(root='raw_data', train=True, download=True, transform=transform) 
test_data = datasets.MNIST(root='raw_data', train=False, download=True, transform=transform) 
#print("number of image in train_data:{} | no. of image in test_data: {}\n".format(len(train_data)))

#mini batch(each batch contain 60 images) 
train_batch_size = 600 
#each batch contain 6000 images 
test_batch_size =100 
trainset_loader = torch.utils.data.DataLoader(train_data, batch_size=train_batch_size, shuffle=True)
testset_loader = torch.utils.data.DataLoader(test_data, batch_size=test_batch_size, shuffle=False)

#print("number of image in train_data:{} | no. of image in test_data: {}\n".format(len(train_data)))
print("batch_size:", train_batch_size, "\n") 
n_epoch =1 
print("number of image in each batch: ") 
for epoch in range(n_epoch):
	print("epoch:", epoch) 
	for i, data in enumerate(trainset_loader,0): 
		images, labels = data
		print (i, "no. input image:", len(images), ",lables", len(labels))

print(images.shape) 
print(images[10].shape) 
print(images[10][0].shape)
#plot the image print('lable value:', labels[10])
plt.imshow(images[10][0].numpy(), cmap='gray_r');

figure = plt.figure() 
num_of_images = 20 
for index in range(1, num_of_images + 1): 
	plt.subplot(5, 10, index) 
	plt.axis('off')
	plt.imshow(images[index].numpy().squeeze(), cmap='gray_r')

#define modle class 
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

def get_device(): 
	device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') 
	return device
device = get_device()
#make an instance/object of the model_class 
model = MLP_Net() 
model.to(device)
# define loss and optimizer 
criterion = nn.CrossEntropyLoss() 
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5)
#optimizer = optim.Adam(model.parameters(), lr=0.001)

def train(): 
	model.train() 
	for batch_idx, (data, target) in enumerate(trainset_loader): 
		data, target = data.to(device), target.to(device) 
		optimizer.zero_grad() 
		output = model(data) 
		loss = criterion(output, target) 
		loss.backward() 
		optimizer.step() #update w 
		if batch_idx % 10 == 0:
			#print("---------- batch: ", batch_idx, ", lose: ", loss.item()) 
			hist_train_loss_detail.append(loss.item())
	print("----- Train loss:", loss.item())
	hist_train_loss.append(loss.item()) #append loss value to list

#understand torch.max() 
a = torch.randn(3,3) 
#i = torch.max(a,1) 
i= a.max(1, keepdim=True) 
print(a) 
print ('\nmax result:', i)
print ('\nindex of max:', i[1])

#validation function 
def test(): 
	model.eval() 
	test_loss = 0 
	correct = 0 
	for data, target in testset_loader: 
		data, target = data.to(device), target.to(device) 
		output = model(data) 
		test_loss += criterion(output, target).item() 
		pred = output.data.max(1, keepdim=True)[1] 
		#print('pred:', pred.shape)
		#print('output 0:', output.data.shape)
		correct += pred.eq(target.data.view_as(pred)).cpu().sum() 
		hist_test_accuracy_detail.append(correct.item() / len(testset_loader.dataset))
	test_loss /= len(testset_loader.dataset) 
	accuracy = correct.item() / len(testset_loader.dataset) #whole batches accuracy 
	print("----- Test accuracy:", accuracy) 
	hist_test_loss.append(test_loss)
	hist_test_accuracy.append(accuracy)

hist_train_loss= [] 
hist_train_loss_detail=[] 
hist_test_loss=[] 
hist_test_accuracy = [] 
hist_test_accuracy_detail=[]
#n_epoch =2 #loop of training 
n_epoch =20 #loop of training 
#Start train model 
start = time.time() 
for epoch in range(n_epoch): 
	print("Epoch :", epoch) 
	train() 
	test()

#after above loop, well train module paramters 
#save that model to file,

stop = time.time() 
train_time = stop - start 
print("Training time:{} s".format(train_time))

#save_result()
#plot_result()

def plot_result(): 
	#Plot the result 
	plt.figure(figsize=(14,6)) 
	plt.subplot(121) 
	plt.plot(hist_train_loss) 
	plt.title('Loss') 
	plt.subplot(122) 
	plt.plot(hist_test_accuracy) 
	# plotting by columns 
	plt.title('Accuracy') 
	plt.show()
plot_result()

def save_result(): 
	import pandas as pd
	pd.DataFrame(hist_train_loss).to_csv("hist_train_loss_nb.csv", header=None, index=None) 
	pd.DataFrame(hist_train_loss_detail).to_csv("hist_train_loss_detail_nb.csv", header=None, index=None)
	pd.DataFrame(hist_test_accuracy).to_csv("hist_test_accuracy_nb.csv", header=None, index=None) 
	pd.DataFrame(hist_test_accuracy_detail).to_csv("hist_test_accuracy_detail_nb.csv", header=None, index=None)
	#save train time f = open('train_time_nb.txt', 'w') f.write(str(train_time)) f.close()
	#Save Model parameters 
	torch.save(model.state_dict(), 'mnist_model_nb.pt')
save_result()