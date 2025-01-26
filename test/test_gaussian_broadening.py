import unittest
from Spectral_vis.gaussian_broadening import Spectrum


class TestSpectrum(unittest.TestCase):

    TEST_CSV = '''OSC_1,E_1,OSC_2,E_2
2.324731387024224,535.2334033024443,0.1338582039901939,339.7921275832706
2.3254202650073044,534.5721631011123,0.1324517867983956,344.2004446092342
2.3256904245881542,534.1585204900409,0.1287782387852872,348.0928495923811
2.32347169021592,534.5190654229943,0.124632261404815,351.9002460125527
2.317546857557376,535.6570497138649,0.1217992646471306,355.2102598840962
2.313759333957095,537.3553305381198,0.1153079160838235,357.3967318752584
2.306754813200932,539.153330731818,0.1124660798121597,358.6130159939975
2.304996100213973,541.3104229076746,0.10904854015541,358.5564589757017
2.3049469830742444,542.3183699158157,0.1088292762912912,357.5717211186889
2.312748332557095,543.7815997207333,0.1076025081457869,355.43091251634974
'''

    def setUp(self):
        self.sigma_1 = 0.2
        self.sigma_2 = 0.5
        self.fname = 'test_energy.csv'
        with open(self.fname, 'w') as f:
            f.write(self.TEST_CSV)
        self.spectrum = Spectrum(self.fname)

    def test_calculate_spectrum_eV(self):
        self.spectrum.calculate_spectrum(unit='eV', sigma=self.sigma_1)
        self.assertIsNotNone(self.spectrum.spectrum_eV)
        self.assertEqual(len(self.spectrum.spectrum_eV), 1000)

    def test_calculate_spectrum_nm(self):
        self.spectrum.calculate_spectrum(unit='nm', sigma=self.sigma_1)
        self.assertIsNotNone(self.spectrum.spectrum_nm)
        self.assertEqual(len(self.spectrum.spectrum_nm), 1000)

    def test_plot_spectrum_eV(self):
        self.spectrum.calculate_spectrum(unit='eV', sigma=self.sigma_1)
        self.spectrum.plot_spectrum(unit='eV')
        # No assertion, just ensure no exceptions are raised

    def test_plot_spectrum_nm(self):
        self.spectrum.calculate_spectrum(unit='nm', sigma=self.sigma_1)
        self.spectrum.plot_spectrum(unit='nm')
        # No assertion, just ensure no exceptions are raised

    def tearDown(self):
        import os
        os.remove(self.fname)


if __name__ == '__main__':
    unittest.main()
