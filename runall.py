import clean
import TrainModel
import PreprocessData
import TestModel
#PreprocessData.main()
#clean.main()
#First do main_divider to test the dividers and choose the best one then use main_dropout to see with variations of 
#dropout and epoch
#TrainModel.main_divider()
TrainModel.main_dropout() 
TestModel.main()