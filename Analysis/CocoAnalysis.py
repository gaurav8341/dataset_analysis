import pycocotools.coco as coco
import matplotlib.pyplot as plt

class Dataset:
    def __init__(self, annfile) -> None:
        '''
            :param annfile : path of the annotation file
        '''
        self.dataset = dict()
        if annfile is not None:
            self.dataset = coco.COCO(annfile)
            #self.createIndex()
        self.categoryIdtoNames = dict() # list of dict of 
        self.CategoryImagesDict = dict() # category name : list of images id dict
        self.supercategoryNames = set()
        self.supCatCatDict = dict() # supercategory name : list of category names dict
        self.catToNoBbox = dict() # category name : list of annotation ids
        self.imgToNoBbox = dict() # img id : no of bboxes in the id
        self.catToMinMaxArea = dict() # category id : tuple(min size of area of bbox, max size of area of bbox)
        
    def createIndex(self):
        # here I will consolidate every code in below functions and will optimize the below functions
        pass
    
    def getCategoryNames(self) -> list:
        '''
            :returns list of all the category names
        '''
        if type(self.dataset).__name__ == 'COCO':
            categories = self.dataset.loadCats(self.dataset.getCatIds())
            self.categoryIdtoNames = {cat['id'] : cat['name'] for cat in categories}

        return self.categoryIdtoNames.values()
    
    def getSuperCategoryNames(self) -> set:
        '''
            :returns self.supercategoryNames : list of all the names
        '''
        if type(self.dataset).__name__ == 'COCO':
            categories = self.dataset.loadCats(self.dataset.getCatIds())
            self.supercategoryNames = set(cat['supercategory'] for cat in categories)
        
        return self.supercategoryNames
    
    def getCategoryImagesDict(self) -> dict:
        '''
            :returns categoryImagesDict : dict( "categoryName" : list(imageIds))
        '''
        for id, name in self.categoryIdtoNames.items():
            self.CategoryImagesDict[name] = self.dataset.getImgIds(catIds = [id])
        
        return self.CategoryImagesDict
    
    def getSupCatDict(self):
        pass
    
    def getMinMaxBBox(self):
        '''
            :returns tuple : minimum no. of bbox in any image in dataset, maximum no. of bbox in any image in dataset
        '''
        if type(self.dataset).__name__ == 'COCO':
            for imgId in self.dataset.imgToAnns.keys():
                self.imgToNoBbox[imgId] = len(self.dataset.imgToAnns[imgId])
                
        return min(self.imgToNoBbox.values()), max(self.imgToNoBbox.values())
    
    def getCatToNoBbox(self):
        '''
            :returns catToNoBbox : dict(category to no of bboxes)
        '''
        if type(self.dataset).__name__ == 'COCO':
            for id, name in self.categoryIdtoNames.items():
                annIds = self.dataset.getAnnIds(catIds = [id])
                self.catToNoBbox[name] = len(annIds)
        
        return self.catToNoBbox      
    
    def getCatMinMaxArea(self):
        '''
            : returns catToMinMaxArea : category id : tuple(min size of area of bbox, max size of area of bbox)
        '''
        if type(self.dataset).__name__ == 'COCO':
            for id, name in self.categoryIdtoNames.items():
                annIds = self.dataset.getAnnIds(catIds = [id])
                self.catToMinMaxArea[name] = self.getMinMaxArea(annIds)
        
        return self.catToMinMaxArea    
    
    def getMinMaxArea(self, ids = []):
        '''
            :params ids : list of annotations
            :returns tuple of min , max area of bbox from specified ids
        '''
        anns = self.dataset.loadAnns(ids)
        maxArea = 0.0
        minArea = 9999999.99
        for a in anns:
            bbox = a['bbox']
            area = bbox[2] * bbox[3]
            minArea = min(minArea, area)
            maxArea = max(maxArea, area)
        
        return minArea, maxArea
            
        
        
     
if __name__ == '__main__':
    dataset = Dataset('D:\\Paralaxiom Tutorials\\dataset_analysis\\annotations\\instances_val2017.json')
    
    print('The Dataset has {} categorie(s)'.format(len(dataset.getCategoryNames())))
    
    print('The dataset has {} supercategorie(s)'.format(len(dataset.getSuperCategoryNames())))
    
    minBbox, maxBbox = dataset.getMinMaxBBox()
    print('In dataset, this is the min count of bbox in any image : {}, this is the max count of bbox in any image : {}'.format(minBbox, maxBbox))
          
    # names = dataset.getCategoryImagesDict().keys()
    # values = [len(value) for value in dataset.getCategoryImagesDict().values()]
    
    # plt.bar(range(len(names)), values, tick_label = names)
    # plt.title(label = 'Count of images WRT Category Names')
    # plt.show()
    print(dataset.getCatMinMaxArea())
    
    names = dataset.getCatToNoBbox().keys()
    values = dataset.getCatToNoBbox().values()
    
    plt.bar(range(len(names)), values, tick_label = names)
    plt.title(label = 'Count of Bboxes WRT Category Names')
    plt.show()
    