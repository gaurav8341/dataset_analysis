import os
import sys

class KittiToYoloConverter:
    def __init__(self, path, yoloPath = '\\yoloDataset\\') -> None:
        self.path = path
        self.yoloPath = sys.path[0] + yoloPath
        self.criteriaindexdict = {
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
        
    def convert(self):
        bbox = (4,8)
        
        if not os.path.exists(self.yoloPath):
            os.makedirs(self.yoloPath)
        
        if not os.path.exists(self.yoloPath + 'annotations/'):
            os.makedirs(self.yoloPath + 'annotations/')

        for filename in os.listdir(self.path):
            with open(os.path.join(self.path, filename), 'r') as f:
                fileinput = f.read().split('\n')
                fileinput = [f.split(' ') for f in fileinput if len(f.split(' ')) == 15]
                fileoutput = ''
                for annot in fileinput:
                    fileoutput += str(self.criteriaindexdict[annot[0]]) + ' ' + self.convertToYolo(annot[bbox[0]: bbox[1]]) + '\n'
                    
                with open(os.path.join(self.yoloPath + 'annotations/', filename[0:-4] + '.txt'), 'w') as f:
                    f.write(fileoutput)
        
        labels = ''
        for k in self.criteriaindexdict.keys():
            labels += k + '\n'
        
        with open(os.path.join(self.yoloPath, 'labels.txt'), 'w') as f:
            f.write(labels)
            
    def convertToYolo(self, bbox):
        '''
            converts the Kitti bbox to Coco format
        '''
        xmin = float(bbox[0])
        ymin = float(bbox[1])
        xmax = float(bbox[2])
        ymax = float(bbox[3])
        return str(xmin) + ' ' + str(ymin) + ' ' + str(xmax - xmin) +' '+ str(ymax - ymin)