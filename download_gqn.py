import os
import sys
import collections

from argparse import ArgumentParser

DatasetInfo = collections.namedtuple(
    'DatasetInfo',
    ['basepath', 'train_size', 'test_size', 'frame_size', 'sequence_size']
)


DATASETS_INFO = dict(
    jaco=DatasetInfo(
        basepath='jaco',
        train_size=3600,
        test_size=400,
        frame_size=64,
        sequence_size=11),

    mazes=DatasetInfo(
        basepath='mazes',
        train_size=1080,
        test_size=120,
        frame_size=84,
        sequence_size=300),

    rooms_free_camera_with_object_rotations=DatasetInfo(
        basepath='rooms_free_camera_with_object_rotations',
        train_size=2034,
        test_size=226,
        frame_size=128,
        sequence_size=10),

    rooms_ring_camera=DatasetInfo(
        basepath='rooms_ring_camera',
        train_size=2160,
        test_size=240,
        frame_size=64,
        sequence_size=10),

    rooms_free_camera_no_object_rotations=DatasetInfo(
        basepath='rooms_free_camera_no_object_rotations',
        train_size=2160,
        test_size=240,
        frame_size=64,
        sequence_size=10),

    shepard_metzler_5_parts=DatasetInfo(
        basepath='shepard_metzler_5_parts',
        train_size=900,
        test_size=100,
        frame_size=64,
        sequence_size=15),

    shepard_metzler_7_parts=DatasetInfo(
        basepath='shepard_metzler_7_parts',
        train_size=900,
        test_size=100,
        frame_size=64,
        sequence_size=15)
)


def download_proportion(datasetName: str, proportion: float, location: str):
    dataset_info = DATASETS_INFO[datasetName]

    top_path = location
    train_path = os.path.join(top_path, 'train')
    test_path = os.path.join(top_path, 'test')

    os.mkdir(top_path)
    os.mkdir(train_path)
    os.mkdir(test_path)

    train_nb = int(proportion * dataset_info.train_size)
    test_nb = int(proportion * dataset_info.test_size)

    train_length = len(str(dataset_info.train_size))
    train_template = '{:0%d}-of-{:0%d}.tfrecord' % (train_length, train_length)

    test_length = len(str(dataset_info.test_size))
    test_template = '{:0%d}-of-{:0%d}.tfrecord' % (test_length, test_length)

    header = 'gsutil -m cp gs://gqn-dataset/{}'.format(datasetName)

    ## train copy
    for i in range(train_nb):
        file = train_template.format(i+1, dataset_info.train_size)
        command = '{0}/train/{1} {2}/{1}'.format(header, file, train_path)
        # print(command)
        os.system(command)

    ## test copy
    for i in range(test_nb):
        file = test_template.format(i+1, dataset_info.test_size)
        command = '{0}/test/{1} {2}/{1}'.format(header, file, test_path)
        # print(command)
        os.system(command)


def download_whole(datasetName: str, location: str):
    header = 'gsutil cp -r gs://gqn-dataset/{}'.format(datasetName) 
    command = '{0}/ {1}/'.format(header, location)
    os.system(command)


if __name__ == '__main__':
    datasetNames = list(DATASETS_INFO.keys())
    parser = ArgumentParser(description='Download GQN datasets.')
                        
    parser.add_argument('dataset', metavar='dataset', nargs=1, type=str, choices=datasetNames,
                        help=f'The name of the dataset to download, options: {datasetNames}')
    parser.add_argument('-p', '--proportion', type=float, default=[1.0], nargs=1,
                        help='The proportion of the dataset to download (value between 0 and 1)')
    parser.add_argument('-l', '--location', type=str, default=None, nargs=1,
                        help='Location of folder to save files to')
    args = parser.parse_args()

    PROP = args.proportion[0]
    DATASET = args.dataset[0]
    LOCATION = args.location[0] if args.location != None else f'{DATASET}'

    assert 0 <= PROP <= 1, "Proportion must be a value in range [0, 1]"

    if PROP < 1:
        print(f'Downloading {PROP*100:.0f}% of the following dataset: {DATASET}')
        # download_proportion(DATASET, PROP, LOCATION)
    else:
        print(f'Downloading all of the following dataset: {DATASET}')
        # download_whole(DATASET, LOCATION)

