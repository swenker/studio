__author__ = 'wenjusun'

def main():
    # suite = additional_tests()
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
    pass

if __name__ == '__main__':
    import os
    import sys
    cms_p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print cms_p
    sys.path.insert(0, cms_p)
    main()
