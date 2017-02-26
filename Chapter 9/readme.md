# Chapter 9

## The Kernel Tick
1. 采用google map api 计算距离，单位mi
2. 由于api访问限制，计算的数据存成csv然后读取。


## Using LIBSVM

1. the test code does not work because the version above the 3.12 
2. here is the solution from [stackoverflow](http://stackoverflow.com/questions/10343893/python-libsvm-typeerror-init-got-an-unexpected-keyword-argument-kernel)
3. use brew install LIBSVM in the Macos
4. add the files svm.py and svmutil.py to the project. 