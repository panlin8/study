SOURCE = main.c
HEADER = 
CFLAGSD = -O0 -ggdb -g3 -gdwarf-2
CFLAGSR = -O3
LIB = 
DEFINE = 

TARGET = test

all:debug

debug:
	gcc -o $(TARGET) $(SOURCE) $(CFLAGSD) 

release:
	gcc -o $(TARGET) $(SOURCE) $(CFLAGSR) 


clean:
	rm -rf $(TARGET)
