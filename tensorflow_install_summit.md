### Installation Instructions for `tensorflow-gpu` on `Summit`

* module load and append to `~/.bashrc`
    * module load python/2.7.15-anaconda2-5.3.0
    * module load cuda/9.1.85
    * module load gcc/6.4.0

* `conda create --name <venv>`
* `conda activate` or `source activate <venv>`
* `conda install tensorflow-gpu=1.2.1=py27cuda8.0cudnn6.0_0`
* `touch device.cu`
```#include <stdio.h>

int main() {
  int nDevices;

  cudaGetDeviceCount(&nDevices);
  for (int i = 0; i < nDevices; i++) {
    cudaDeviceProp prop;
    cudaGetDeviceProperties(&prop, i);
    printf("Device Number: %d\n", i);
    printf("  Device name: %s\n", prop.name);
    printf("  Memory Clock Rate (KHz): %d\n",
           prop.memoryClockRate);
    printf("  Memory Bus Width (bits): %d\n",
           prop.memoryBusWidth);
    printf("  Peak Memory Bandwidth (GB/s): %f\n\n",
           2.0*prop.memoryClockRate*(prop.memoryBusWidth/8)/1.0e6);
  }
}
```
* Run: `nvcc -o device device.cu`

### Test benchmark:

* `touch tf.py` 

```
import tensorflow as tf
sess = tf.Session()

class SquareTest(tf.test.TestCase):
        def testSquare(self):
                with self.test_session():
                        x = tf.square([2, 3])
                        self.assertAllEqual(x.eval(), [4, 9])


if __name__ == '__main__':
        tf.test.main()
```

### Output:

```
(snakes) [jdakka@login3.summit ~]$ python tf.py 
2019-02-20 14:37:01.705492: I tensorflow/core/common_runtime/gpu/gpu_device.cc:940] Found device 0 with properties: 
name: Tesla V100-SXM2-16GB
major: 7 minor: 0 memoryClockRate (GHz) 1.53
pciBusID 0004:04:00.0
Total memory: 15.75GiB
Free memory: 15.34GiB
2019-02-20 14:37:02.139714: W tensorflow/stream_executor/cuda/cuda_driver.cc:523] A non-primary context 0x15160c7e0 exists before initializing the StreamExecutor. We haven't verified StreamExecutor works with that.
2019-02-20 14:37:02.141286: I tensorflow/core/common_runtime/gpu/gpu_device.cc:940] Found device 1 with properties: 
name: Tesla V100-SXM2-16GB
major: 7 minor: 0 memoryClockRate (GHz) 1.53
pciBusID 0004:05:00.0
Total memory: 15.75GiB
Free memory: 15.34GiB
2019-02-20 14:37:02.510169: W tensorflow/stream_executor/cuda/cuda_driver.cc:523] A non-primary context 0x151610a00 exists before initializing the StreamExecutor. We haven't verified StreamExecutor works with that.
2019-02-20 14:37:02.511720: I tensorflow/core/common_runtime/gpu/gpu_device.cc:940] Found device 2 with properties: 
name: Tesla V100-SXM2-16GB
major: 7 minor: 0 memoryClockRate (GHz) 1.53
pciBusID 0035:03:00.0
Total memory: 15.75GiB
Free memory: 15.34GiB
2019-02-20 14:37:02.895419: W tensorflow/stream_executor/cuda/cuda_driver.cc:523] A non-primary context 0x151614c20 exists before initializing the StreamExecutor. We haven't verified StreamExecutor works with that.
2019-02-20 14:37:02.896978: I tensorflow/core/common_runtime/gpu/gpu_device.cc:940] Found device 3 with properties: 
name: Tesla V100-SXM2-16GB
major: 7 minor: 0 memoryClockRate (GHz) 1.53
pciBusID 0035:04:00.0
Total memory: 15.75GiB
Free memory: 15.34GiB
2019-02-20 14:37:02.897065: I tensorflow/core/common_runtime/gpu/gpu_device.cc:961] DMA: 0 1 2 3 
2019-02-20 14:37:02.897077: I tensorflow/core/common_runtime/gpu/gpu_device.cc:971] 0:   Y Y Y Y 
2019-02-20 14:37:02.897085: I tensorflow/core/common_runtime/gpu/gpu_device.cc:971] 1:   Y Y Y Y 
2019-02-20 14:37:02.897094: I tensorflow/core/common_runtime/gpu/gpu_device.cc:971] 2:   Y Y Y Y 
2019-02-20 14:37:02.897101: I tensorflow/core/common_runtime/gpu/gpu_device.cc:971] 3:   Y Y Y Y 
2019-02-20 14:37:02.897121: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1030] Creating TensorFlow device (/gpu:0) -> (device: 0, name: Tesla V100-SXM2-16GB, pci bus id: 0004:04:00.0)
2019-02-20 14:37:02.897132: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1030] Creating TensorFlow device (/gpu:1) -> (device: 1, name: Tesla V100-SXM2-16GB, pci bus id: 0004:05:00.0)
2019-02-20 14:37:02.897140: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1030] Creating TensorFlow device (/gpu:2) -> (device: 2, name: Tesla V100-SXM2-16GB, pci bus id: 0035:03:00.0)
2019-02-20 14:37:02.897149: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1030] Creating TensorFlow device (/gpu:3) -> (device: 3, name: Tesla V100-SXM2-16GB, pci bus id: 0035:04:00.0)
2019-02-20 14:37:03.928769: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1030] Creating TensorFlow device (/gpu:0) -> (device: 0, name: Tesla V100-SXM2-16GB, pci bus id: 0004:04:00.0)
2019-02-20 14:37:03.928810: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1030] Creating TensorFlow device (/gpu:1) -> (device: 1, name: Tesla V100-SXM2-16GB, pci bus id: 0004:05:00.0)
2019-02-20 14:37:03.928821: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1030] Creating TensorFlow device (/gpu:2) -> (device: 2, name: Tesla V100-SXM2-16GB, pci bus id: 0035:03:00.0)
2019-02-20 14:37:03.928831: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1030] Creating TensorFlow device (/gpu:3) -> (device: 3, name: Tesla V100-SXM2-16GB, pci bus id: 0035:04:00.0)
..
----------------------------------------------------------------------
Ran 2 tests in 0.033s

OK

```
