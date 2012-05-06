import unittest
import numpy as np
import pycmpfit


def print_results(mp_result, pars, act, test_name):
    print("===========================================")
    print("Test Name: \t %s" % test_name)
    print("Status: \t %i" % mp_result.status)
    print("Chi-square: \t %f" % mp_result.bestnorm)
    print("# of params: \t %i" % mp_result.npar)
    print("# of free: \t %i" % mp_result.nfree)
    print("# pegged: \t %i" % mp_result.npegged)
    print("# iterations: \t %i" % mp_result.niter)
    print("# func evals: \t %i\n" % mp_result.nfev)

    for i in range(mp_result.npar):
        print("P[%i]: %f +/- %f \t (Actual: %f)" % (i, 
                                                    pars[i], 
                                                    mp_result.xerror[i], 
                                                    act[i]))
    print("===========================================")
    
    
def linear_userfunc(m, n, x, private_data):
    # private data is a dict...
    devs = np.zeros((m), dtype=np.float64)
    user_dict = {"deviates": None}

    # f = b - m*x
    for i in range(m):
        f = x[0] - x[1]*private_data["x"][i]
        devs[i] = (private_data["y"][i] - f)/private_data["ey"][i]

    user_dict["deviates"] = devs

    return user_dict


class LinearTest(unittest.TestCase):

    def setUp(self):
        self.x = np.array([-1.7237128E+00,1.8712276E+00,-9.6608055E-01,
                           -2.8394297E-01,1.3416969E+00,1.3757038E+00,
                           -1.3703436E+00,4.2581975E-02,-1.4970151E-01,
                           8.2065094E-01], dtype = np.float64)

        self.y = np.array([1.9000429E-01,6.5807428E+00,1.4582725E+00,
                           2.7270851E+00,5.5969253E+00,5.6249280E+00,
                           0.787615,3.2599759E+00,2.9771762E+00,
                           4.5936475E+00], dtype = np.float64)
        
        self.ey = np.zeros((10), dtype = np.float64)
        self.ey[:] = 0.07
        
        self.user_d = {"x": self.x, "y": self.y, "ey": self.ey}
        
        self.m = 10
        self.n = 2
        self.pars = np.array([1.0, 1.0], dtype = np.float64)
        self.act = np.array([3.2, -1.78], dtype = np.float64)
        
        self.fit = pycmpfit.Mpfit(linear_userfunc, 
                                  self.m, 
                                  self.pars, 
                                  private_data = self.user_d)

    def test_fit(self):
        self.fit.mpfit()
        self.assertEqual(self.fit.result.status, 1)
        self.assertTrue(self.fit.result.bestnorm <= 2.756285 and 
                        self.fit.result.bestnorm >= 2.756284)
        print_results(self.fit.result, self.pars, self.act, "Linear Function")

if __name__ == '__main__':
    unittest.main()
    