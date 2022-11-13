# gqn_datasets_translator

With major contributions from [versatran01](https://github.com/versatran01).

### Data downloader and data converter for DeepMind GQN dataset https://github.com/deepmind/gqn-datasets to use with other libraries than TensorFlow

Don't hesitate to make a pull request. 

**Dependencies**

You need to install:

- TensorFlow [here](https://www.tensorflow.org/install/)
- gsutil [here](https://cloud.google.com/storage/docs/gsutil_install) *Note that gsutil works in python 2.\* only*


**Download the tfrecord dataset**

If you want to download the entire dataset:
```shell
gsutil -m cp -R gs://gqn-dataset/<dataset> .
```

If you want to download a proportion of the dataset only:
```shell
python download_gqn.py <dataset> <proportion>
```

Command line options:
```
usage: download_gqn.py [-h] [-p PROPORTION] [-l LOCATION] dataset

Download GQN datasets.

positional arguments:
  dataset               The name of the dataset to download, options: ['jaco', 'mazes', 'rooms_free_camera_with_object_rotations',
                        'rooms_ring_camera', 'rooms_free_camera_no_object_rotations', 'shepard_metzler_5_parts',
                        'shepard_metzler_7_parts']

optional arguments:
  -h, --help            show this help message and exit
  -p PROPORTION, --proportion PROPORTION
                        The proportion of the dataset to download (value between 0 and 1. Default=1)
  -l LOCATION, --location LOCATION  
                        Location of folder to save files to. If the location doesn't exist, it is created. If the location contains a "train" or "test" folder, the download will be terminated. The default location is the location of the script with a folder the same name as the given dataset.
```

**Convert the raw dataset**

Command line options:
```shell
usage: convert2file.py [-h] [-b BATCH_SIZE] [-n FIRST_N] [-m MODE]
                       base_dir dataset

Convert gqn tfrecords to gzip files.

positional arguments:
  base_dir              base directory of gqn dataset
  dataset               datasets to convert, eg. shepard_metzler_5_parts

optional arguments:
  -h, --help            show this help message and exit
  -b BATCH_SIZE, --batch-size BATCH_SIZE
                        number of sequences in each output file
  -n FIRST_N, --first-n FIRST_N
                        convert only the first n tfrecords if given
  -m MODE, --mode MODE  whether to convert train or test
```

Convert all records with all sequences in sm5 train (400 records, 2000 seq each):
```shell
python convert2file.py ~/gqn_dataset shepard_metzler_5_parts
```

Convert first 20 records with batch size of 128 in sm5 test:
```shell
python convert2file.py ~/gqn_dataset shepard_metzler_5_parts -n 20 -b 128 -m test
```

**Size of the datasets:**

| Names        | Sizes           |
| ------------- |:-------------:|
| _total_ | 1.45 Tb |
| ------------- | --------------|
| jaco      | 198.97 Gb |
| mazes      | 136.23 Gb |
| rooms\_free\_camera\_no\_object\_rotations | 255.75 Gb |
| rooms\_free\_camera\_with\_object\_rotations | 598.75 Gb |
| rooms\_ring\_camera | 250.89 Gb |
| shepard\_metzler\_5\_parts | 21.09 Gb |
| shepard\_metzler\_7\_parts | 23.68 Gb |
