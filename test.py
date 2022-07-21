import torch
import argparse
from sklearn import metrics
import warnings
warnings.filterwarnings("ignore")
torch.cuda.set_device(0)
# print('cuda size == 1')
from trainAndTest import *


parser = argparse.ArgumentParser()
# parser.add_argument('--input', type=str, default='', help='input file root')
parser.add_argument('--ligand', type=str, default='', help='input file root')
parser.add_argument('--protein', type=str, default='', help='input file root')
args = parser.parse_args()

def IsPro(str):
    if 'contact_map' not in str:
        return True
    else:
        return False

def main():
    if IsPro(args.protein):
        if args.protein not in seqContactDict.keys():
            print('Contact map not found. Please input contact map file.')
            exit()
        else:
            contact_map = seqContactDict[args.protein]
    else:
        proteins = open(args.protein).readlines()        
        proteins = readLinesStrip(proteins)
        contact_map = []
        for i in range(0,len(proteins)):
            contact_map.append(proteins[i])
        contactmap_np = [list(map(float, x.strip(' ').split(' '))) for x in contact_map]
        feature2D = np.expand_dims(contactmap_np, axis=0)
        contact_map = torch.FloatTensor(feature2D)

    model = DrugVQA(modelArgs,block = ResidualBlock)
    model.load_state_dict(torch.load('model_pkl/DUDE/DUDE30Res-fold3-50.pkl', map_location='cuda:0'))
    model.cuda()

    testArgs = {}
    testArgs['model'] = model

    testArgs['smiles'] = np.array(args.ligand.split(','))
    testArgs['contact_map'] = contact_map

    testArgs['criterion'] = torch.nn.BCELoss()
    testArgs['use_regularizer'] = False
    testArgs['penal_coeff'] = 0.03
    testArgs['clip'] = True

    testResult = test2(testArgs)
    for i in range(len(testArgs['smiles'])):
        print('protein:', args.protein[:20]+'...')
        print('ligand:', testArgs['smiles'][i])
        print(testResult[i])
    
if __name__ == "__main__":
    main()