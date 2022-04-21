import click
import os
import torch
from multiprocessing import cpu_count

cpu_num = cpu_count() # 自动获取最大核心数目
os.environ ['OMP_NUM_THREADS'] = str(cpu_num)
os.environ ['OPENBLAS_NUM_THREADS'] = str(cpu_num)
os.environ ['MKL_NUM_THREADS'] = str(cpu_num)
os.environ ['VECLIB_MAXIMUM_THREADS'] = str(cpu_num)
os.environ ['NUMEXPR_NUM_THREADS'] = str(cpu_num)
torch.set_num_threads(cpu_num)

from ml.utils import train_application_classification_cnn_model, train_traffic_classification_cnn_model
from ml.utils import load_application_classification_cnn_model,load_traffic_classification_cnn_model
from ml.metrics import confusion_matrix,get_classification_report
from utils import ID_TO_APP,ID_TO_TRAFFIC
@click.command()
@click.option('-d', '--data_path', default='./', help='training data dir path containing parquet files', required=True)
@click.option('-m', '--model_path', default='models/', help='output model path', required=True)
@click.option('-t', '--task', default='app', help='classification task. Option: "app" or "traffic"', required=True)
@click.option('--gpu', help='whether to use gpu', default=True, type=bool)
def main(data_path, model_path, task, gpu):
    if gpu:
        gpu = 0
        print('gpu')
    else:
        gpu = None
    if task == 'app':
        model_path=model_path+'application_classification.cnn.model'
        print(model_path)
        # train
        # train_application_classification_cnn_model(data_path, model_path, gpu)
        # load_model
        model=load_application_classification_cnn_model(model_path, gpu)

        # result for train_dataset
        print("app train precision and recall:")
        cm=confusion_matrix(data_path + '/processed_train_data',model,num_class=12)
        print(get_classification_report(cm,labels=ID_TO_APP))

        # result for test_dataset
        # print("app test precision and recall:")
        # cm=confusion_matrix(data_path + '/processed_test_data',model,num_class=12)
        # print(get_classification_report(cm,labels=ID_TO_APP))

    elif task == 'traffic':
        model_path=model_path+'traffic_classification.cnn.model'
        print(model_path)
        # train_traffic_classification_cnn_model(data_path, model_path, gpu)
        model=load_application_classification_cnn_model(model_path, gpu)
        # print("traffic train precision and recall:")
        # cm=confusion_matrix(data_path + '/processed_train_data',model,num_class=6)
        # print(get_classification_report(cm,labels=ID_TO_TRAFFIC))
        print("traffic test precision and recall:")
        cm=confusion_matrix(data_path + '/processed_test_data',model,num_class=6)
        print(get_classification_report(cm,labels=ID_TO_TRAFFIC))
    else:
        exit('Not Support')


if __name__ == '__main__':
    main()
#重装lightning