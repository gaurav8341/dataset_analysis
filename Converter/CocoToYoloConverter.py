import pycocotools.coco as coco
import os
import sys
import cv2

class CocoToYoloConverter:
    def __init__(self, jsonpath, imagePath, yoloPath = '/CocoYoloDataset/', height = None, width = None) -> None:
        '''
            initializes the converter
            jsonPath = 'path to the coco dataset json'
            imagePath = 'path to the coco dataset images\' directory'
            yoloPath = 'path where resultant datset is stored'
            height = 'resized height of the image'
            width = 'resized width of the image'
        '''
        self.criteriaIndexDict = dict()
        self.jsonpath = jsonpath
        self.dataset = coco.COCO(jsonpath)
        self.yoloPath = sys.path[0] + yoloPath
        self.imagePath = imagePath
        # self.imgToBBoxDict = dict()
        print('Making up the yolo dataset directory at location ' + self.yoloPath)

        self.height = height if height is not None else None
        self.width = width if width is not None else None

        if not os.path.exists(self.yoloPath):
            os.makedirs(self.yoloPath)
        
        if not os.path.exists(self.yoloPath + 'annotations/'):
            os.makedirs(self.yoloPath + 'annotations/')
            
        if not os.path.exists(self.yoloPath + 'images/'):
            os.makedirs(self.yoloPath + 'images/')
        
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
        x_scale, y_scale = 1, 1
        
        for imgid in imgids:
            imageToAnns[imgid] = self.dataset.loadAnns(self.dataset.getAnnIds(imgid))
            
        for imgid  in imgids:
            fileinput = ''
            img = self.dataset.loadImgs(imgid)[0]
            
            image = cv2.imread(os.path.join(self.imagePath, img['file_name']))
            
            if self.height is not None and self.width is not None:
                x_scale = self.width / img['width']
                y_scale = self.height / img['height']
                image = cv2.resize(image, (self.width, self.height))
                
            cv2.imwrite(os.path.join(self.yoloPath + 'images/', img['file_name']), image)

            
            for ann in imageToAnns[imgid]:
                fileinput += str(self.criteriaIndexDict[self.dataset.loadCats(ann['category_id'])[0]['name']]) + ' ' + self.convertBBox(ann['bbox'], x_scale, y_scale) + '\n'
        
            with open(os.path.join(self.yoloPath + 'annotations/', str(img['file_name'][:-4]) + '.txt'), 'w') as f:
                f.write(fileinput)
                
    def convertBBox(self, bbox , x_scale, y_scale):
        '''
            scale the bboxes
        '''
        bbox[0] = bbox[0] * x_scale
        bbox[1] = bbox[1] * y_scale
        bbox[2] = bbox[2] * x_scale
        bbox[3] = bbox[3] * y_scale
            
        return ' '.join([str(elem) for elem in bbox])
        
        
        
