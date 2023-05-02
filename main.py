import numpy as np
from ezc3d import c3d

def readCSVasFloat(filename, with_key=True):
    """
    Borrowed from SRNN code. Reads a csv and returns a float matrix.
    https://github.com/asheshjain399/NeuralModels/blob/master/neuralmodels/utils.py#L34
    Args
      filename: string. Path to the csv file
    Returns
      returnArray: the read data in a float32 matrix
    """
    labels = []
    returnArray = []
    lines = open(filename).readlines()
    if with_key: # skip first line
        labels = lines[0].strip().split(',')
        lines = lines[1:]
    for line in lines:
        line = line.strip().split(',')
        if len(line) > 0:
            returnArray.append(np.array([np.float32(x) for x in line]))

    returnArray = np.array(returnArray)
    return returnArray, labels


def c3d_generation(csv_array, labels, c3d_output_dir):
    frame_numbers = csv_array.shape[0]
    c_point = csv_array.shape[1]

    a_c3d= c3d()
    a_c3d['parameters']['POINT']['RATE']['value'] = [frame_numbers]
    a_c3d['parameters']['POINT']['LABELS']['value'] = labels
    a_c3d['data']['points'] = np.ones((4, len(labels), frame_numbers))

    for frame in range(frame_numbers):
        for p in range(int(c_point / 2)):
            m = p % 3
            t = int(c_point / (2 * p))
            a_c3d['data']['points'][m, t, frame] = csv_array[frame, p]

    return c3d
def c3d_generation_split(csv_array, labels, c3d_output_dir):
    frame_numbers = csv_array.shape[0]
    c_point = csv_array.shape[1]

    m_labels = labels[0:18]
    f_labels = labels[18:36]
    print(m_labels)
    print(len(m_labels))

    m_array = csv_array[0:, 0:int(c_point/2)].copy()
    f_array = csv_array[0:, int(c_point/2):c_point].copy()

    m_c3d = c3d()
    f_c3d = c3d()
    m_c3d['parameters']['POINT']['RATE']['value'] = [frame_numbers]
    m_c3d['parameters']['POINT']['LABELS']['value'] = m_labels
    m_c3d['data']['points'] = np.ones((4, len(m_labels), frame_numbers))

    f_c3d['parameters']['POINT']['RATE']['value'] = [frame_numbers]
    f_c3d['parameters']['POINT']['LABELS']['value'] = m_labels
    f_c3d['data']['points'] = np.ones((4, len(f_labels), frame_numbers))

    for frame in range(frame_numbers):

         for p in range(int(c_point/2)):
             m = p % 3
             t = int(p/6)
             print(t)
             print(m_array[frame, p])
             m_c3d['data']['points'][m, t, frame] = m_array[frame, p]

    for frame in range(frame_numbers):

         for p in range(int(c_point/2)):
             m = p % 3
             t = int(p/6)
             f_c3d['data']['points'][m, t, frame] = f_array[frame, p]

    return m_c3d, f_c3d



if __name__ == '__main__':
    tvs_dir = './mocap_cleaned.tsv'
    c3d_path = './HDM_bd_02-01_01_120.c3d'
    tvs_array, tvs_label = readCSVasFloat(tvs_dir)
    print(tvs_array.shape)
    print(tvs_label)
    mc3d, fc3d=c3d_generation_split(tvs_array, tvs_label, c3d_path)
    mc3d.write('f_test.c3d')
    fc3d.write('m_test.c3d')
    #c3d_data = c3d(c3d_path)
    #print(c3d_data['parameters']['POINT']['USED']['value'][0])
    #print(c3d_data['parameters']['POINT']['LABELS']['value'])

