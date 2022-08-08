import pycocotools.coco as coco
import os
import sys

class CocoToYoloConverter:
    def __init__(self, path, yoloPath = '/CocoYoloDataset/') -> None:
        self.criteriaIndexDict = dict()
        self.path = path
        self.dataset = coco.COCO(path)
        self.yoloPath = sys.path[0] + yoloPath
        # self.imgToBBoxDict = dict()
        print('Making up the yolo dataset directory at location ' + self.yoloPath)

        if not os.path.exists(self.yoloPath):
            os.makedirs(self.yoloPath)
        
        if not os.path.exists(self.yoloPath + 'annotations/'):
            os.makedirs(self.yoloPath + 'annotations/')
        
        self.createLabelFile()
        self.convert()

        
    def createLabelFile(self) -> str:
        '''
            creates the label file for the yolo dataset
        '''
        labels = ''
        for i, cat in enumerate(self.dataset.dataset['categories']):
            self.criteriaIndexDict[cat['name']] = i
            labels += cat['name'] + '\n'
        
        with open(os.path.join(self.yoloPath, 'labels.txt'), 'w') as f:
            f.write(labels) 
            
    def convert(self):
        '''
            converts the coco dataset to yolo format
        '''
        imageToAnns = dict()
        imgids = self.dataset.getImgIds()
        
        for imgid in imgids:
            imageToAnns[imgid] = self.dataset.loadAnns(self.dataset.getAnnIds(imgid))
            
        for imgid  in imgids:
            fileinput = ''
            img = self.dataset.loadImgs(imgid)[0]
            for ann in imageToAnns[imgid]:
                fileinput += str(self.criteriaIndexDict[self.dataset.loadCats(ann['category_id'])[0]['name']]) + ' '+' '.join([str(elem) for elem in ann['bbox']]) + '\n'
        
            with open(os.path.join(self.yoloPath + 'annotations/', str(img['file_name'][:-4]) + '.txt'), 'w') as f:
                f.write(fileinput)
