import torch.nn as nn

# in this file we're creating the neural network with 3 linear fully connected layers:
class DeepQNetwork(nn.Module):
    def __init__(self):
        super(DeepQNetwork, self).__init__()
        # sizing the layers to have 128 neurons
        self.fc1 = nn.Sequential(nn.Linear(4, 128), nn.ReLU(inplace=True))
        self.fc2 = nn.Sequential(nn.Linear(128, 128), nn.ReLU(inplace=True))
        self.fc3 = nn.Sequential(nn.Linear(128, 1))


        # this method is called to initialize the weights of the network.
        # which is crucial for training stability and performance.
        self._create_weights()

    def _create_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                # xavier initialization is used to set weights that helps the network train more efficiently from the beginning.
                # by setting the weights to values that are neither too small nor too large at the start of the training.
                nn.init.xavier_uniform_(m.weight)
                # setting the bias to 0 which gonna be adjusted during the trainings.
                nn.init.constant_(m.bias, 0)

    # this method defines the forward pass of the neural network, which is
    # how the input data flows through the layer to produce an output.
    def forward(self, x):
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)

        return x