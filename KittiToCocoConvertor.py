import os
import json

class KittiToCocoConvertor:
    def __init__(self, path) -> None:
        self.path = path
        self.images = list()
        self.annotations = list()
        self.criterias = list()
        self.bbox = (4,8)
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
        for fileName in os.listdir(self.path):
            with open(os.path.join(self.path, fileName), 'r') as f:
                fileinput = f.read().split('\n')
                fileinput = [f.split(' ') for f in fileinput if len(f.split(' ')) == 15]
                # self.imageDict[fileName[0:-4]] = list()
                imageDict = dict()
                imageDict['id'] = len(self.images)
                imageDict['file_name'] = fileName
                imageDict['width'] = ''
                imageDict['height'] = ''
                imageDict['coco_url'] = ''
                imageDict['date_captured'] = ''
                imageDict['flickr_url'] = ''
                imageDict['license'] = ''
                self.images.append(imageDict)
                for i, annot in enumerate(fileinput):
                    annotDict = dict()
                    annotDict['bbox'] = self.convertToCoco(annot[self.bbox[0]:self.bbox[1]])
                    annotDict['segmentation'] = list()
                    annotDict['area'] = ''
                    annotDict['iscrowd'] = ''
                    annotDict['id'] = len(self.annotations)
                    annotDict['image_id'] = len(self.images) - 1
                    annotDict['category_id'] = self.CriteriaIndexDict[annot[0]]
                    self.annotations.append(annotDict)
        
        for k, v in self.CriteriaIndexDict.items():
            criteriaDict = dict()
            criteriaDict['id'] = v
            criteriaDict['name'] = k
            criteriaDict['supercategory'] = ''
            self.criterias.append(criteriaDict)
            
        self.dataset['images'] = self.images
        self.dataset['annotations'] = self.annotations
        self.dataset['criterias'] = self.criterias
        self.dataset['licenses'] = list()
        infoDict = dict()
        infoDict['description'] = 'Kitti Dataset'
        infoDict['contributor'] = 'Kitti'
        infoDict['date_created'] = '2020-01-01'
        infoDict['url'] = ''
        infoDict['version'] = ''
        infoDict['year'] = 2020
        self.dataset['info'] = infoDict
        
        
    def saveDataset(self, filePath = 'KittiInCoco.json'):
        with open(filePath, 'w') as f:
            json.dump(self.dataset, f, indent = 4)
            
    def convertToCoco(self, bbox):
        '''
            converts the Kitti bbox to Coco format
        '''
        xmin = float(bbox[0])
        ymin = float(bbox[1])
        xmax = float(bbox[2])
        ymax = float(bbox[3])
        return [xmin, ymin, xmax - xmin, ymax - ymin]