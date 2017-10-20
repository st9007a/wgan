import pickle
import numpy as np

from nn.gan import DCGAN
from data.dataset import mnist
from data.util import get_noise_sample

batch_size = 100
sample_size = 100

dataset = mnist()

model = DCGAN(noise_shape = (sample_size, ))
model.build()

for step in range(1, 5001):
    for _ in range(1):
        data = None
        y = None
        if step % 1 == 0:
            noise = get_noise_sample(batch_size, sample_size)

            data = model.generator().predict(noise)
            y = np.array([0] * batch_size)

        else:
            data, _ = dataset.get_batch2D(batch_size)
            y = np.ones([batch_size, 1])

        d_loss = model.discriminator().train_on_batch(data, y)

    noise = get_noise_sample(batch_size, sample_size)
    y = np.ones([batch_size, 1])
    g_loss = model.gan().train_on_batch(noise, y)

    if step % 100 == 0:
        print("step " + str(step) + " d_loss: " + str(d_loss) + " g_loss: " + str(g_loss))

model.generator().save('./models/dcgan-keras-' + str(d_loss) + '-' + str(g_loss))

print('Generate fake data')
noise = get_noise_sample(100, sample_size)
mnist_fake = model.generator().predict(np.array(noise))

print(mnist_fake)

with open('./fake_data/dcgan-keras-' + str(d_loss) + '-' + str(g_loss) + '.pkl', 'wb') as p:
    pickle.dump(mnist_fake, p, protocol = pickle.HIGHEST_PROTOCOL)
