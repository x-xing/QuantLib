
#%%
from QuantLib import *

class ShortRateModelTest:
    def testSwaps(self):
        print("Testing Hull-White swap pricing against known values...")
        
        calendar = TARGET()
        today = Date.todaysDate()
        Settings.instance().evaluationDate = calendar.adjust(today)
        settlement = calendar.advance(today, 2, Days)


        dates = [settlement,
                calendar.advance(settlement,1,Weeks),
                calendar.advance(settlement,1,Months),
                calendar.advance(settlement,3,Months),
                calendar.advance(settlement,6,Months),
                calendar.advance(settlement,9,Months),
                calendar.advance(settlement,1,Years),
                calendar.advance(settlement,2,Years),
                calendar.advance(settlement,3,Years),
                calendar.advance(settlement,5,Years),
                calendar.advance(settlement,10,Years),
                calendar.advance(settlement,15,Years)]
        
        discountFactors = [ 1.0, 0.999258, 0.996704, 0.990809, 0.981798, 
                            0.972570, 0.963430, 0.929532, 0.889267,
                            0.803693, 0.596903, 0.433022]
    
        termStructure = YieldTermStructureHandle(DiscountCurve( dates, 
                                                                discountFactors,
                                                                Actual365Fixed()))
        model = HullWhite(termStructure)

        start = [ -3, 0, 3 ]
        length = [ 2, 5, 10 ]
        rates = [ 0.02, 0.04, 0.06 ]
        euribor = Euribor6M(termStructure)
        engine = TreeVanillaSwapEngine(model, 120)

        tolerance = 1e-8

        for s in start:
            startDate = calendar.advance(settlement,s,Months)
            if startDate < today:
                fixingDate = calendar.advance(startDate,-2,Days)
            pastFixings = RealTimeSeries([fixingDate], [0.03])
            IndexManager.instance().setHistory(euribor.name(),
                                               pastFixings)
        
        for l in length:
            maturity = calendar.advance(startDate,l,Years)
            fixedSchedule = Schedule(startDate, maturity, Period(Annual),
                                     calendar, Unadjusted, Unadjusted,
                                     DateGeneration.Forward, False)
            floatSchedule = Schedule(startDate, maturity, Period(Semiannual),
                                     calendar, Following, Following,
                                     DateGeneration.Forward, False)
            for r in rates:
                swap = VanillaSwap(VanillaSwap.Payer, 1000000.0,
                                   fixedSchedule, r, Thirty360(),
                                   floatSchedule, euribor, 0.0, Actual360())

                swap.setPricingEngine(DiscountingSwapEngine(termStructure))
                expected = swap.NPV()
                swap.setPricingEngine(engine)
                calculated = swap.NPV()

                error = (expected-calculated)/expected
                print('Error=%.8f for r=%.2f' % (error, r))

    def testCachedHullWhite(self):
        print("Testing Hull-White calibration against cached values using swaptions with start delay...")

        today = Date(15, February, 2002)
        settlement = Date(19, February, 2002)
        Settings.instance().evaluationDate = today
        termStructure = YieldTermStructureHandle(FlatForward(settlement,0.04875825, Actual365Fixed()))
        model = HullWhite(termStructure)
        #data element: [start, length, vol]
        data = [[1, 5, 0.1148 ],
                [2, 4, 0.1108 ],
                [3, 3, 0.1070 ],
                [4, 2, 0.1021 ],
                [5, 1, 0.1000 ]] 
        index = Euribor6M(termStructure)

        engine = JamshidianSwaptionEngine(model)

        swaptions = CalibrationHelperVector()
        for row in data:
            vol = SimpleQuote(row[2])
            helper = SwaptionHelper(Period(row[0], Years),
                                    Period(row[1], Years),
                                    QuoteHandle(vol),
                                    index,
                                    Period(1, Years), Thirty360(),
                                    Actual360(), termStructure)
            helper.setPricingEngine(engine)
            swaptions.push_back(helper)        

        # Set up the optimization problem
        # Real simplexLambda = 0.1
        # Simplex optimizationMethod(simplexLambda)
        optimizationMethod = LevenbergMarquardt(1.0e-8,1.0e-8,1.0e-8)
        endCriteria = EndCriteria(10000, 100, 1e-6, 1e-8, 1e-8)

        #Optimize
        model.calibrate(swaptions, optimizationMethod, endCriteria)
        ecType = model.endCriteria()

        # Check and print out results
        cachedA = 0.0464041
        cachedSigma = 0.00579912
        tolerance = 1.0e-5
        xMinCalculated = model.params()
        yMinCalculated = model.value(xMinCalculated, swaptions)
        xMinExpected= [cachedA, cachedSigma]
        yMinExpected = model.value(xMinExpected, swaptions)
        if ((xMinCalculated[0]-cachedA) > tolerance) or ((xMinCalculated[1]-cachedSigma) > tolerance):
            print(  "Failed to reproduce cached calibration results:\n")
        print(  "calculated: a = ", xMinCalculated[0], ", "
                "sigma = ", xMinCalculated[1], ", "
                "f(a) = ", yMinCalculated, ",\n"
                "expected:   a = ", xMinExpected[0], ", "
                "sigma = ", xMinExpected[1], ", "
                "f(a) = ", yMinExpected, ",\n"
                "difference: a = ", xMinCalculated[0]-xMinExpected[0], ", "
                "sigma = ", xMinCalculated[1]-xMinExpected[1], ", "
                "f(a) = ", yMinCalculated - yMinExpected, ",\n"
                "end criteria = ", ecType )
    
    def testCachedHullWhiteFixedReversion(self):
        print("Testing Hull-White calibration with fixed reversion against cached values...")

        today = Date(15, February, 2002)
        settlement = Date(19, February, 2002)
        Settings.instance().evaluationDate = today
        termStructure = YieldTermStructureHandle(FlatForward(settlement,0.04875825, Actual365Fixed()))
        model = HullWhite(termStructure,0.05,0.01)
        data = [[1, 5, 0.1148],
                [2, 4, 0.1108],
                [3, 3, 0.1070],
                [4, 2, 0.1021],
                [5, 1, 0.1000]]
        index = Euribor6M(termStructure)

        engine = JamshidianSwaptionEngine(model)

        swaptions = CalibrationHelperVector()
        for row in data:
            vol = SimpleQuote(row[2])
            helper = SwaptionHelper(Period(row[0], Years),
                                    Period(row[1], Years),
                                    QuoteHandle(vol),
                                    index,
                                    Period(1, Years), 
                                    Thirty360(),
                                    Actual360(), termStructure)
            helper.setPricingEngine(engine)
            swaptions.push_back(helper)

        # Set up the optimization problem
        #Real simplexLambda = 0.1
        #Simplex optimizationMethod(simplexLambda)
        optimizationMethod = LevenbergMarquardt()
        endCriteria = EndCriteria(1000,500,1E-8,1E-8,1E-8)

        #Optimize
        model.calibrate(swaptions, optimizationMethod, endCriteria, Constraint(), DoubleVector(), HullWhite.FixedReversion())
        ecType = model.endCriteria()
        
        # Check and print out results
        cachedA = 0.05
        cachedSigma = 0.00585858
        tolerance = 1.0e-5
        xMinCalculated = model.params()
        yMinCalculated = model.value(xMinCalculated, swaptions)
        xMinExpected= [cachedA, cachedSigma]
        yMinExpected = model.value(xMinExpected, swaptions)
        if ((xMinCalculated[0]-cachedA) > tolerance) or ((xMinCalculated[1]-cachedSigma) > tolerance):
            print("Failed to reproduce cached calibration results:\n")
        print(  "calculated: a = ", xMinCalculated[0], ", "
                "sigma = ", xMinCalculated[1], ", "
                "f(a) = ", yMinCalculated, ",\n"
                "expected:   a = ", xMinExpected[0], ", "
                "sigma = ", xMinExpected[1], ", "
                "f(a) = ", yMinExpected, ",\n"
                "difference: a = ", xMinCalculated[0]-xMinExpected[0], ", "
                "sigma = ", xMinCalculated[1]-xMinExpected[1], ", "
                "f(a) = ", yMinCalculated - yMinExpected, ",\n"
                "end criteria = ", ecType )

    def testFuturesConvexityBias(self):
        print("Testing Hull-White futures convexity bias...")

        # G. Kirikos, D. Novak, "Convexity Conundrums", Risk Magazine, March 1997
        futureQuote = 94.0
        a = 0.03
        sigma = 0.015
        t = 5.0
        T = 5.25

        expectedForward = 0.0573037
        tolerance       = 0.0000001

        futureImpliedRate = (100.0-futureQuote)/100.0
        calculatedForward = futureImpliedRate - HullWhite.convexityBias(futureQuote,t,T,sigma,a)

        error = calculatedForward-expectedForward

        if (error > tolerance):
            print("Failed to reproduce convexity bias:")

        print("calculated: %.4f \texpected: %.4f" % (calculatedForward, expectedForward))
        print("error: %e \tolerance: %e" % (error, tolerance))
        

    def testExtendedCoxIngersollRossDiscountFactor(self):
        print("Testing zero-bond pricing for extended CIR model...")

        today = Settings.instance().evaluationDate

        rate = 0.1
        rTS = YieldTermStructureHandle(FlatForward(today, rate, Actual365Fixed()))

        now = 1.5
        maturity = 2.5

        cirModel = ExtendedCoxIngersollRoss(rTS, rate, 1.0, 1e-4, rate)

        expected = rTS.discount(maturity)/rTS.discount(now)
        calculated = cirModel.discountBond(now, maturity, rate)

        tol = 1e-6
        diff = (expected-calculated)

        if (diff > tol) :
            print("Failed to reproduce zero bound price:")
        print("calculated: %.4f \texpected: %.4f" % (calculated, expected))
        print("difference: %.4f \ttolerance: %.4f" % (diff, tol))

    
    def testCachedHullWhite2(self): 
        print("Testing Hull-White calibration against cached ",
            "values using swaptions without start delay...")

        today = Date(15, February, 2002)
        settlement = Date(19, February, 2002)
        Settings.instance().evaluationDate = today
        termStructure = YieldTermStructureHandle(FlatForward(settlement,0.04875825,
                                                            Actual365Fixed()))
        model = HullWhite(termStructure)
        data = [[1, 5, 0.1148 ],
                [2, 4, 0.1108 ],
                [3, 3, 0.1070 ],
                [4, 2, 0.1021 ],
                [5, 1, 0.1000 ]]
        index = Euribor6M(termStructure)
        # Euribor 6m with zero fixing days
        index0 = IborIndex(
            index.familyName(),index.tenor(),0,index.currency(),index.fixingCalendar(),
            index.businessDayConvention(),index.endOfMonth(),index.dayCounter(),termStructure) 

        engine = JamshidianSwaptionEngine(model)

        swaptions = CalibrationHelperVector()
        for ele in data:
            vol = SimpleQuote(ele[2])
            helper = SwaptionHelper(Period(ele[0], Years),
                                    Period(ele[1], Years),
                                    QuoteHandle(vol),
                                    index0,
                                    Period(1, Years), Thirty360(),
                                    Actual360(), termStructure)
            helper.setPricingEngine(engine)
            swaptions.push_back(helper)
        

        # Set up the optimization problem
        # Real simplexLambda = 0.1;
        # Simplex optimizationMethod(simplexLambda);
        optimizationMethod = LevenbergMarquardt(1.0e-8,1.0e-8,1.0e-8)
        endCriteria = EndCriteria(10000, 100, 1e-6, 1e-8, 1e-8)

        #Optimize
        model.calibrate(swaptions, optimizationMethod, endCriteria)
        ecType = model.endCriteria()

        # Check and print out results
        # The cached values were produced with an older version of the
        # JamshidianEngine not accounting for the delay between option
        # expiry and underlying start
        
        cachedA = 0.0482063
        cachedSigma = 0.00582687
        
        tolerance = 5.0e-6
        xMinCalculated = model.params()
        yMinCalculated = model.value(xMinCalculated, swaptions)
        xMinExpected= [cachedA, cachedSigma]
        yMinExpected = model.value(xMinExpected, swaptions)
        if ((xMinCalculated[0]-cachedA) > tolerance) or ((xMinCalculated[1]-cachedSigma) > tolerance):
            print("Failed to reproduce cached calibration results:\n")
        print(  "calculated: a = ", xMinCalculated[0], ", "
                "sigma = ", xMinCalculated[1], ", "
                "f(a) = ", yMinCalculated, ",\n"
                "expected:   a = ", xMinExpected[0], ", "
                "sigma = ", xMinExpected[1], ", "
                "f(a) = ", yMinExpected, ",\n"
                "difference: a = ", xMinCalculated[0]-xMinExpected[0], ", "
                "sigma = ", xMinCalculated[1]-xMinExpected[1], ", "
                "f(a) = ", yMinCalculated - yMinExpected, ",\n"
                "end criteria = ", ecType )


srt = ShortRateModelTest()
srt.testSwaps()
srt.testCachedHullWhite()
srt.testCachedHullWhiteFixedReversion()
srt.testFuturesConvexityBias()
srt.testCachedHullWhite2()
srt.testExtendedCoxIngersollRossDiscountFactor()


#%%
