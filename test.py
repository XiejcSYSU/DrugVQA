import torch
import argparse
from sklearn import metrics
import warnings
warnings.filterwarnings("ignore")
torch.cuda.set_device(1)
print('cuda size == 1')
from trainAndTest import *


parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, default='', help='input file root')
args = parser.parse_args()

def main():

    testFoldPath = args.input
    # testFoldPath = './data/DUDE/dataPre/DUDE-foldTest3'

    testProteinList = getTestProteinList(testFoldPath)
    dataDict = getDataDict(testProteinList,ACTIVE_PATH,DECOY_PATH,contactPath)

    model = DrugVQA(modelArgs,block = ResidualBlock)
    model.load_state_dict(torch.load('model_pkl/DUDE/DUDE30Res-fold3-50.pkl'))

    model.cuda()

    testArgs = {}
    testArgs['model'] = model

    testArgs['test_proteins'] = testProteinList
    testArgs['testDataDict'] = dataDict
    testArgs['seqContactDict'] = seqContactDict

    testArgs['criterion'] = torch.nn.BCELoss()
    testArgs['use_regularizer'] = False
    testArgs['penal_coeff'] = 0.03
    testArgs['clip'] = True

    testResult = testPerProtein(testArgs)
    print(testResult)
    
if __name__ == "__main__":
    main()