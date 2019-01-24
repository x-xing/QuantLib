from QuantLib import *

class CreditRiskPlusTest:
    def testReferenceValues(self):
        print("Testing extended credit risk plus model against reference values...")

        tol = 1E-8; 

        # Reference Values are taken from [1] Integrating Correlations, Risk,
        # July 1999, table A, table B and figure 1 

        sector1Exposure = DoubleVector(1000, 1.0)
        sector1Pd = DoubleVector(1000, 0.04)
        sector1Sector = DoubleVector(1000, 0)

        sector2Exposure = DoubleVector(1000, 2.0)
        sector2Pd = DoubleVector(1000, 0.02)
        sector2Sector = DoubleVector(1000, 1)

        exposure = DoubleVector()
        exposure.insert(exposure.end(), sector1Exposure.begin(),
                        sector1Exposure.end())
        exposure.insert(exposure.end(), sector2Exposure.begin(),
                        sector2Exposure.end())

        pd =  DoubleVector()
        pd.insert(pd.end(), sector1Pd.begin(), sector1Pd.end())
        pd.insert(pd.end(), sector2Pd.begin(), sector2Pd.end())

        sector = DoubleVector()
        sector.insert(sector.end(), sector1Sector.begin(), sector1Sector.end())
        sector.insert(sector.end(), sector2Sector.begin(), sector2Sector.end())

        relativeDefaultVariance = DoubleVector()
        relativeDefaultVariance.push_back(0.75 * 0.75)
        relativeDefaultVariance.push_back(0.75 * 0.75)

        rho = Matrix(2, 2)
        rho = [[1,0.5], [0.5, 1]]
        
        unit = 0.1

        cr = CreditRiskPlus(exposure, pd, sector, relativeDefaultVariance, rho, unit)

        if ( std::fabs(cr.sectorExposures()[0] - 1000.0) > tol )
            BOOST_FAIL("failed to reproduce sector 1 exposure ("
                    << cr.sectorExposures()[0] << ", should be 1000)");

        if ( std::fabs(cr.sectorExposures()[1] - 2000.0) > tol )
            BOOST_FAIL("failed to reproduce sector 2 exposure ("
                    << cr.sectorExposures()[1] << ", should be 2000)");

        if ( std::fabs(cr.sectorExpectedLoss()[0] - 40.0) > tol )
            BOOST_FAIL("failed to reproduce sector 1 expected loss ("
                    << cr.sectorExpectedLoss()[0] << ", should be 40)");

        if ( std::fabs(cr.sectorExpectedLoss()[1] - 40.0) > tol )
            BOOST_FAIL("failed to reproduce sector 2 expected loss ("
                    << cr.sectorExpectedLoss()[1] << ", should be 40)");

        if ( std::fabs(cr.sectorUnexpectedLoss()[0] - 30.7) > 0.05 )
            BOOST_FAIL("failed to reproduce sector 1 unexpected loss ("
                    << cr.sectorUnexpectedLoss()[0] << ", should be 30.7)");

        if ( std::fabs(cr.sectorUnexpectedLoss()[1] - 31.3) > 0.05 )
            BOOST_FAIL("failed to reproduce sector 2 unexpected loss ("
                    << cr.sectorUnexpectedLoss()[1] << ", should be 31.3)");

        if ( std::fabs(cr.exposure() - 3000.0) > tol )
            BOOST_FAIL("failed to reproduce overall exposure ("
                    << cr.exposure() << ", should be 3000)");

        if ( std::fabs(cr.expectedLoss() - 80.0) > tol )
            BOOST_FAIL("failed to reproduce overall expected loss ("
                    << cr.expectedLoss() << ", should be 80)");

        if ( std::fabs(cr.unexpectedLoss() - 53.1) > 0.01 )
            BOOST_FAIL("failed to reproduce overall unexpected loss ("
                    << cr.unexpectedLoss() << ", should be 53.1)");

        // the overall relative default variance in the paper seems generously rounded,
        // but since EL and UL is matching closely and the former is retrieved
        // as a simple expression in the latter, we do not suspect a problem in our
        // calculation

        if ( std::fabs(cr.relativeDefaultVariance() - 0.65 * 0.65) > 0.001 )
            BOOST_FAIL("failed to reproduce overall relative default variance ("
                    << cr.relativeDefaultVariance() << ", should be 0.4225)");

        if ( std::fabs(cr.lossQuantile(0.99) - 250) > 0.5 )
            BOOST_FAIL("failed to reproduce overall 99 percentile ("
                    << cr.lossQuantile(0.99) << ", should be 250)");
    }

test_suite *CreditRiskPlusTest::suite() {
    test_suite *suite = BOOST_TEST_SUITE("Credit risk plus tests");
    suite->add(QUANTLIB_TEST_CASE(&CreditRiskPlusTest::testReferenceValues));
    return suite;
}