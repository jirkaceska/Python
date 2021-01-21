def compare(string1, string2):
    if string1 == string2:
        print("HOOORAY!")
    else:
        print("ERORR!!!!")

aisa_out = open('../../pb071/hw02/aisa-test-out.txt')
aisa_out_r = open('../../pb071/hw02/r_out_reduced.txt')
my_out = open('../../pb071/build-hw02-Desktop_Qt_5_10_1_MinGW_32bit-Default/test_output.txt')
my_out_r = open('../../pb071/build-hw02-Desktop_Qt_5_10_1_MinGW_32bit-Default/reduced_out_r.txt')

test = open('../../pb071/build-hw02-Desktop_Qt_5_10_1_MinGW_32bit-Default/aisa-test.txt').readlines()
test_r = open('../../pb071/hw02/aisa_test_r_reduced.txt').readlines()

i = 0
err = 0

def normal_test():
    global i, err
    for line in aisa_out.readlines():
        sec_line = my_out.readline()
        if (line != sec_line):
            print("ERROR: \n", "\t should be: ", line, "\t instead found: ",sec_line, end="")
            print("TEST")
            err += 1

            for j in range(3):
                print(test[int(i + j)], end="")
        i += 3

def r_test():
    i = 0
    global err
    for line in aisa_out_r.readlines():
        sec_line = my_out_r.readline()
        if (line != sec_line):
            print("ERROR: \n", "\t should be: ", line, "\t instead found: ",sec_line, end="")
            print("TEST")
            err += 1

            for j in range(2):
                print(test_r[int(i + j)], end="")
        i += 2
    

r_test()
print("Number of errors: ", err)
# compare(string1, string2)
