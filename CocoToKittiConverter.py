import pycocotools.coco as coco
import os
import sys

class CocoToKittiConverter:
    def __init__(self, path, kittiPath = '/CocoKittiDataset/') -> None:
        self.idCriteriaDict = dict()
        self.path = path
        self.dataset = coco.COCO(path)
        self.kittiPath = sys.path[0] + kittiPath
        # self.imgToBBoxDict = dict()
        print('Making up the yolo dataset directory at location ' + self.kittiPath)

        if not os.path.exists(self.kittiPath):
            os.makedirs(self.kittiPath)
                
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
            
        for imgid  in imgids:
            fileinput = ''
            img = self.dataset.loadImgs(imgid)[0]
            for ann in imageToAnns[imgid]:
                fileinput += self.idCriteriaDict[ann['category_id']] + ' '
                fileinput += '_ _ _ '
                fileinput += ' '.join([str(elem) for elem in self.convertToKitti(ann['bbox'])]) + ' '
                fileinput +=  '_ _ _ _ _ _ _\n'
        
            with open(os.path.join(self.kittiPath, str(img['file_name'][:-4]) + '.txt'), 'w') as f:
                f.write(fileinput)

    def convertToKitti(self, bbox):
        '''
            converts the coco bbox to kitti bbox
        '''
        xmin = float(bbox[0])
        ymin = float(bbox[1])
        xmax = float(bbox[2])
        ymax = float(bbox[3])
        return [xmin, ymin, xmax + xmin, ymax + ymin]