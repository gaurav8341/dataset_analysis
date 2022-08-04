import os
import json

class KittiDataset:
    def __init__(self, path) -> None:
        self.path = path
        self.images = list()
        self.annotations = list()
        self.criterias = list()
        self.indexNameDict = {
            'Truncation': 1,
            'Occlusion': 2,
            'Alpha': 3,
            'BBox': (4,8),
            '3d Dimensions': (8, 11),
            'Location': (11,14),
            'Rotation': 14
        }
        self.CriteriaIndexDict = {
            'Pedestrian' : 0, 
            'Truck' : 1, 
            'Car' : 2,  
            'Cyclist' : 3, 
            'DontCare' : 4, 
            'Misc' : 5 , 
            'Van' : 6, 
            'Tram' : 7, 
            'Person_sitting' : 8
        }
        self.dataset = dict()
        self.loadDataset()
    
    def loadDataset(self):
        '''
            loads the kitti dataset in coco format 
        '''
        for fileName in os.listdir(self.datadir):
            with open(os.path.join(self.datadir, fileName), 'r') as f:
                fileinput = f.read().split('\n')
                fileinput = [f.split(' ') for f in fileinput if len(f.split(' ')) == 15]
                # self.imageDict[fileName[0:-4]] = list()
                imageDict = dict()
                imageDict['id'] = len(self.images)
                imageDict['file_name'] = fileName
                self.images.append(imageDict)
                for i, annot in enumerate(fileinput):
                    annotDict = dict()
                    for k, v in self.indexNameDict.items():
                        if type(v) is tuple:
                            annotDict[k] = annot[v[0]: v[1]]
                        else:
                            annotDict[k] = annot[v]
                            
                    annotDict['annotation_id'] = len(self.annotations)
                    annotDict['image_id'] = len(self.images)
                    annotDict['criteria_id'] = self.CriteriaIndexDict[annot[0]]
                    self.annotations.append(annotDict)
        
        for k, v in self.CriteriaIndexDict.items():
            criteriaDict = dict()
            criteriaDict['id'] = v
            criteriaDict['name'] = k
            self.criterias.append(criteriaDict)
            
        self.dataset['images'] = self.images
        self.dataset['annotations'] = self.annotations
        self.dataset['criterias'] = self.criterias
        
    def saveDataset(self, filePath = 'KittiInCoco.json'):
        with open(filePath, 'w') as f:
            json.dump(self.dataset, f)
            
        
        
        