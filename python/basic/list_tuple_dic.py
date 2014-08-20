#! /usr/bin/env python
#coding=utf-8
#digit_alpha1=(0,'zero';1,'one';2,'two';3,'three';4,'four';5,'five';6,'six';7,'seven';8,'eight';9,'nine')
digit_alpha={'0':'zero','1':'one','2':'two','3':'three','4':'four','5':'five','6':'six','7':'seven','8':'eight','9':'nine'}

def convert(digits):
    digits_str=str(digits)
    alpha_num=[]
    for i in digits_str:
        alpha_num.append(digit_alpha[i])
 
    return '-'.join(alpha_num)

def test_convert():
    connum=convert(89)
    print connum

    connum=convert(8)
    print connum

def convert2(digits):
    digits_str=str(digits)
    dlen=len(digits_str)
    


def test_generator():
    for i in xrange(0,10):
        yield i


def test_generator_main():
    #print test_generator().next()
    for i in test_generator():
        print(i)


test_generator_main()