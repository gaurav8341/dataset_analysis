import os
import json

class KittiAnalysis:
    def __init__(self, datadir = None) -> None:
        '''
            :params datadir : directory for the label file
        '''
        self.imageDict = dict()
        self.criteriaDict = dict()
        self.KittiDict = dict()
        
        self.indexNameDict = {
            'Criteria': 0,
            'Truncation': 1,
            'Occlusion': 2,
            'Alpha': 3,
            'BBox': (4,8),
            '3d Dimensions': (8, 11),
            'Location': (11,14),
            'Rotation': 14
        }
        
        if datadir is not None:
            self.datadir = datadir
            self.generateDictionary()
        
    def generateDictionary(self):
        '''
            creates the necessary dictionaries for the dataset
        '''
        for a in os.listdir(self.datadir):
            with open(os.path.join(self.datadir, a), 'r') as f:
                fileinput = f.read().split('\n')
                fileinput = [f.split(' ') for f in fileinput if len(f.split(' ')) == 15]
                self.imageDict[a[0:-4]] = list()
                for i, f in enumerate(fileinput):
                    FileDict = dict()
                    for k, v in self.indexNameDict.items():
                        if type(v) is tuple:
                            FileDict[k] = f[v[0]: v[1]]
                        else:
                            FileDict[k] = f[v]
                            if k == 'Criteria':
                                if f[v] not in self.criteriaDict.keys():
                                    CriDict = dict()
                                    CriDict['id'] = len(self.criteriaDict)
                                    CriDict['annotations'] = [a[0:-4] + str(i)]
                                    CriDict['images'] = [a[0:-4]]
                                    self.criteriaDict[f[v]] = CriDict
                                else:
                                    self.criteriaDict[f[v]]['annotations'].append(a[0:-4] + str(i))
                                    self.criteriaDict[f[v]]['images'].append(a[0:-4])
                    FileDict['annotation_id'] = a[0:-4] + str(i)
                    self.imageDict[a[0:-4]].append(FileDict)
        
        self.KittiDict['images'] = self.imageDict
        self.KittiDict['criteria'] = self.criteriaDict
    
    def generateJson(self, filePath = 'Kitti.json'):
        '''
            creates and stores the dataset in json format
            :params filepath : the path where the json is stored 
        '''
        with open(filePath, 'w') as f:
            json.dump(self.KittiDict, f, indent = 4)
    
    def getImageIds(self, crtraNms = []):
        '''
            :params crtraNms : List of the criterias names
            :returns imgIds : list of all imageIds 
        '''
        pass
    