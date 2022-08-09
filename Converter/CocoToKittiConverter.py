import pycocotools.coco as coco
import os
import sys
import cv2

class CocoToKittiConverter:
    def __init__(self, jsonPath, imagePath , kittiPath = '/CocoKittiDataset/', height = None, width = None ) -> None:
        '''
            initializes the converter
            path = 'path to the coco dataset json'
            imagePath = 'path to the coco dataset images\' directory'
            kititPath = 'path where resultant datset is stored'
            height = 'resized height of the image'
            width = 'resized width of the image'
        '''
        self.idCriteriaDict = dict()
        self.jsonPath = jsonPath
        self.imagePath = imagePath
        self.dataset = coco.COCO(jsonPath)
        self.kittiPath = sys.path[0] + kittiPath
        self.annotationsPath = self.kittiPath + '\\annotations\\'
        self.kittiImgPath = self.kittiPath + '\\images\\'
        
        self.height, self.width = None, None
        
        if height is not None and width is not None:
            self.height = height
            self.width = width
        
        # self.imgToBBoxDict = dict()

        print('kitti dataset directory location ' + self.kittiPath)        
        if not os.path.exists(self.kittiPath):
            print('Making up the kitti dataset directory at location ' + self.kittiPath)
            os.makedirs(self.kittiPath)
        
            
        if not os.path.exists(self.annotationsPath):
            print('Making up the kitti dataset annotation directory at location ' + self.annotationsPath)
            os.makedirs(self.annotationsPath)
            
                    
        if not os.path.exists(self.kittiImgPath):
            print('Making up the kitti dataset images directory at location ' + self.kittiImgPath)
            os.makedirs(self.kittiImgPath)
                
        for i, cat in enumerate(self.dataset.dataset['categories']):
            self.idCriteriaDict[cat['id']] = cat['name']
            
        self.convert()
            
    def convert(self):
        '''
            converts the coco dataset to yolo format
        '''
        imageToAnns = dict()
        imgids = self.dataset.getImgIds()
        
        for imgid in imgids:
            imageToAnns[imgid] = self.dataset.loadAnns(self.dataset.getAnnIds(imgid))
            
        # in case height and width is not provided
        x_scaled = 1.0
        y_scaled = 1.0
        
        for imgid  in imgids:
            fileinput = ''
            img = self.dataset.loadImgs(imgid)[0]
            imgHeight = img['height']
            imgWidth = img['width']
            
            image = cv2.imread(os.path.join(self.imagePath, img['file_name']))

            if self.height is not None and self.width is not None:
                image = cv2.resize(image, (self.width, self.height))
                x_scaled = self.width /  imgWidth 
                y_scaled = self.height / imgHeight 
            
            cv2.imwrite(os.path.join(self.kittiImgPath, img['file_name']), image)                
            
            for ann in imageToAnns[imgid]:
                fileinput += self.idCriteriaDict[ann['category_id']] + ' '
                fileinput += '_ _ _ '
                fileinput += ' '.join([str(elem) for elem in self.convertToKitti(ann['bbox'], x_scaled, y_scaled)]) + ' '
                fileinput +=  '_ _ _ _ _ _ _\n'
        
            with open(os.path.join(self.annotationsPath, str(img['file_name'][:-4]) + '.txt'), 'w') as f:
                f.write(fileinput)

    def convertToKitti(self, bbox, x_scaled, y_scaled):
        '''
            converts the coco bbox to kitti bbox
        '''
        xmin = float(bbox[0] * x_scaled)
        ymin = float(bbox[1] * y_scaled)
        xmax = float(bbox[2] * x_scaled)
        ymax = float(bbox[3] * y_scaled)
        return [xmin, ymin, xmax + xmin, ymax + ymin]