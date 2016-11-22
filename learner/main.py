from driver import Driver
import sys, getopt

def main(argv):
   if '-h' in argv:
       print('python main.py -c (use cluster) -p (use polynomial features) -n (bust cache) -f (feature selection)')
       exit(0)

   use_hpc = True if '-c' in argv else False
   use_polynomial = True if '-p' in argv else True
   use_force_no_caching = True if '-n' in argv else False
   use_feature_selection = True if '-f' in argv else False

   return {
       'use_hpc': use_hpc,
       'use_polynomial': use_polynomial,
       'use_force_no_caching': use_force_no_caching,
       'use_feature_selection': use_feature_selection
   }

if __name__ == '__main__':
    params = main(sys.argv[1:])
    print(params)
    Driver(verbosity=0,
           hpc=params['use_hpc'],
           polynomial_features=params['use_polynomial'],
           normalize=False,
           scale=True,
           force_no_caching=params['use_force_no_caching'],
           feature_selection=params['use_feature_selection'])
