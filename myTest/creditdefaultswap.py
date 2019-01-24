from QuantLib import *
import math

class CreditDefaultSwapTest:
    def testCachedValue(self):

        print("Testing credit-default swap against cached values...")

        # Initialize curves
        today = Date(9,June,2006)
        Settings.instance().evaluationDate = today
        calendar = TARGET()

        hazardRate = QuoteHandle(SimpleQuote(0.01234))
        probabilityCurve = RelinkableDefaultProbabilityTermStructureHandle() 
        probabilityCurve.linkTo(FlatHazardRate(0, calendar, hazardRate, Actual360()))

        discountRate = QuoteHandle(SimpleQuote(0.06))
        discountCurve = YieldTermStructureHandle(FlatForward(today,discountRate,Actual360())) 
        
        
        # Build the schedule
        issueDate = calendar.advance(today, -1, Years)
        maturity = calendar.advance(issueDate, 10, Years)
        frequency = Semiannual
        convention = ModifiedFollowing

        schedule = Schedule(issueDate, maturity, Period(frequency), calendar,
                            convention, convention, DateGeneration.Forward, False)

        # Build the CDS
        fixedRate = 0.0120
        dayCount = Actual360()
        notional = 10000.0
        recoveryRate = 0.4

        cds = CreditDefaultSwap(Protection.Seller, notional, fixedRate,
                            schedule, convention, dayCount, True, True)
        cds.setPricingEngine(MidPointCdsEngine(probabilityCurve,recoveryRate,
                                               discountCurve))

        npv = 295.0153398
        fairRate = 0.007517539081

        calculatedNpv = cds.NPV()
        calculatedFairRate = cds.fairSpread()
        tolerance = 1.0e-7

        if ((calculatedNpv - npv) > tolerance):
            print("Failed to reproduce NPV with mid-point engine")
        print("mid-point engine")
        print("calculated NPV: ", calculatedNpv)
        print("expected NPV:   ", npv)

        if ((calculatedFairRate - fairRate) > tolerance):
            print("Failed to reproduce fair rate with mid-point engine")
        print("calculated fair rate: ", calculatedFairRate)
        print("expected fair rate:   ", fairRate)

        cds.setPricingEngine(IntegralCdsEngine(Period(1,Days),probabilityCurve,
                                                    recoveryRate,discountCurve))

        calculatedNpv = cds.NPV()
        calculatedFairRate = cds.fairSpread()
        tolerance = 1.0e-5

        if ((calculatedNpv - npv) > notional*tolerance*10):
            print("Failed to reproduce NPV with integral engine")
        print("integral engine (step = 1 day)")
        print("calculated NPV: ", calculatedNpv)
        print("expected NPV:   ", npv)

        if ((calculatedFairRate - fairRate) > tolerance):
            print("Failed to reproduce fair rate with integral engine")
        print("calculated fair rate: ", calculatedFairRate)
        print("expected fair rate:   ", fairRate)

        cds.setPricingEngine(IntegralCdsEngine(Period(1,Weeks),probabilityCurve,
                                                    recoveryRate,discountCurve))

        calculatedNpv = cds.NPV()
        calculatedFairRate = cds.fairSpread()
        tolerance = 1.0e-5

        if ((calculatedNpv - npv) > notional*tolerance*10):
            print("Failed to reproduce NPV with integral engine")
        print("integral engine (step = 1 week)")
        print("calculated NPV: ", calculatedNpv)
        print("expected NPV:   ", npv)

        if ((calculatedFairRate - fairRate) > tolerance):
            print("Failed to reproduce fair rate with integral engine")
        print("calculated fair rate: ", calculatedFairRate)
        print("expected fair rate:   ", fairRate)



    def testCachedMarketValue(self):

        print("Testing credit-default swap against cached market values...")

        evalDate = Date(9,June,2006)
        Settings.instance().evaluationDate = evalDate
        calendar = UnitedStates()

        discountDates = DateVector()
        discountDates.push_back(evalDate)
        discountDates.push_back(calendar.advance(evalDate, 1, Weeks,  ModifiedFollowing))
        discountDates.push_back(calendar.advance(evalDate, 1, Months, ModifiedFollowing))
        discountDates.push_back(calendar.advance(evalDate, 2, Months, ModifiedFollowing))
        discountDates.push_back(calendar.advance(evalDate, 3, Months, ModifiedFollowing))
        discountDates.push_back(calendar.advance(evalDate, 6, Months, ModifiedFollowing))
        discountDates.push_back(calendar.advance(evalDate,12, Months, ModifiedFollowing))
        discountDates.push_back(calendar.advance(evalDate, 2, Years, ModifiedFollowing))
        discountDates.push_back(calendar.advance(evalDate, 3, Years, ModifiedFollowing))
        discountDates.push_back(calendar.advance(evalDate, 4, Years, ModifiedFollowing))
        discountDates.push_back(calendar.advance(evalDate, 5, Years, ModifiedFollowing))
        discountDates.push_back(calendar.advance(evalDate, 6, Years, ModifiedFollowing))
        discountDates.push_back(calendar.advance(evalDate, 7, Years, ModifiedFollowing))
        discountDates.push_back(calendar.advance(evalDate, 8, Years, ModifiedFollowing))
        discountDates.push_back(calendar.advance(evalDate, 9, Years, ModifiedFollowing))
        discountDates.push_back(calendar.advance(evalDate,10, Years, ModifiedFollowing))
        discountDates.push_back(calendar.advance(evalDate,15, Years, ModifiedFollowing))

        dfs = DoubleVector()
        dfs.push_back(1.0)
        dfs.push_back(0.9990151375768731)
        dfs.push_back(0.99570502636871183)
        dfs.push_back(0.99118260474528685)
        dfs.push_back(0.98661167950906203)
        dfs.push_back(0.9732592953359388 )
        dfs.push_back(0.94724424481038083)
        dfs.push_back(0.89844996737120875  )
        dfs.push_back(0.85216647839921411  )
        dfs.push_back(0.80775477692556874  )
        dfs.push_back(0.76517289234200347  )
        dfs.push_back(0.72401019553182933  )
        dfs.push_back(0.68503909569219212  )
        dfs.push_back(0.64797499814013748  )
        dfs.push_back(0.61263171936255534  )
        dfs.push_back(0.5791942350748791   )
        dfs.push_back(0.43518868769953606  )

        curveDayCounter=Actual360()

        discountCurve = RelinkableYieldTermStructureHandle()
        discountCurve.linkTo(DiscountCurve(discountDates, dfs, curveDayCounter))

        dayCounter = Thirty360()
        dates = DateVector()
        dates.push_back(evalDate)
        dates.push_back(calendar.advance(evalDate, 6, Months, ModifiedFollowing))
        dates.push_back(calendar.advance(evalDate, 1, Years, ModifiedFollowing))
        dates.push_back(calendar.advance(evalDate, 2, Years, ModifiedFollowing))
        dates.push_back(calendar.advance(evalDate, 3, Years, ModifiedFollowing))
        dates.push_back(calendar.advance(evalDate, 4, Years, ModifiedFollowing))
        dates.push_back(calendar.advance(evalDate, 5, Years, ModifiedFollowing))
        dates.push_back(calendar.advance(evalDate, 7, Years, ModifiedFollowing))
        dates.push_back(calendar.advance(evalDate,10, Years, ModifiedFollowing))

        defaultProbabilities = DoubleVector()
        defaultProbabilities.push_back(0.0000)
        defaultProbabilities.push_back(0.0047)
        defaultProbabilities.push_back(0.0093)
        defaultProbabilities.push_back(0.0286)
        defaultProbabilities.push_back(0.0619)
        defaultProbabilities.push_back(0.0953)
        defaultProbabilities.push_back(0.1508)
        defaultProbabilities.push_back(0.2288)
        defaultProbabilities.push_back(0.3666)

        hazardRates = DoubleVector()
        hazardRates.push_back(0.0)
        for i in range(1, dates.size()):
            t1 = dayCounter.yearFraction(dates[0], dates[i-1])
            t2 = dayCounter.yearFraction(dates[0], dates[i])
            S1 = 1.0 - defaultProbabilities[i-1]
            S2 = 1.0 - defaultProbabilities[i]
            hazardRates.push_back(math.log(S1/S2)/(t2-t1))

        piecewiseFlatHazardRate = RelinkableDefaultProbabilityTermStructureHandle()
        piecewiseFlatHazardRate.linkTo(InterpolatedHazardRateCurve(dates,
                                                                hazardRates,
                                                               Thirty360()))

        # Testing credit default swap

        # Build the schedule
        issueDate = Date(20, March, 2006)
        maturity = Date(20, June, 2013)
        cdsFrequency = Semiannual
        cdsConvention = ModifiedFollowing

        schedule = Schedule(issueDate, maturity, Period(cdsFrequency), calendar,
                            cdsConvention, cdsConvention,
                            DateGeneration.Forward, False)

        # Build the CDS
        recoveryRate = 0.25
        fixedRate = 0.0224
        dayCount=Actual360()
        cdsNotional=100.0

        cds = CreditDefaultSwap(Protection.Seller, cdsNotional, fixedRate,
                            schedule, cdsConvention, dayCount, True, True)
        cds.setPricingEngine(MidPointCdsEngine(piecewiseFlatHazardRate,
                                               recoveryRate,discountCurve))

        calculatedNpv = cds.NPV()
        calculatedFairRate = cds.fairSpread()

        npv = -1.364048777        # from Bloomberg we have 98.15598868 - 100.00
        fairRate =  0.0248429452  # from Bloomberg we have 0.0258378

        tolerance = 1e-9

        if ((npv - calculatedNpv) > tolerance):
            print("Failed to reproduce the npv for the given credit-default swap")
        print("computed NPV:  ", calculatedNpv)
        print("Given NPV:     ", npv)

        if ((fairRate - calculatedFairRate) > tolerance):
            print("Failed to reproduce the fair rate for the given credit-default swap")
        print("computed fair rate:  ", calculatedFairRate)
        print("Given fair rate:     ", fairRate)


    def testImpliedHazardRate(self):

        print("Testing implied hazard-rate for credit-default swaps...")

        
        # Initialize curves
        calendar = TARGET()
        today = calendar.adjust(Date.todaysDate())
        Settings.instance().evaluationDate = today

        h1 = 0.30
        h2 = 0.40
        dayCounter = Actual365Fixed()

        dates = DateVector(3)
        hazardRates = DoubleVector(3)
        dates[0] = today
        hazardRates[0] = h1

        dates[1] = today + Period(5,Years)
        hazardRates[1] = h1

        dates[2] = today + Period(10,Years)
        hazardRates[2] = h2

        probabilityCurve = RelinkableDefaultProbabilityTermStructureHandle()
        probabilityCurve.linkTo(InterpolatedHazardRateCurve(dates,
                                                                    hazardRates,
                                                                    dayCounter))

        discountCurve = RelinkableYieldTermStructureHandle()
        discountCurve.linkTo(FlatForward(today,0.03,Actual360()))


        frequency = Semiannual
        convention = ModifiedFollowing

        issueDate = calendar.advance(today, -6, Months)
        fixedRate = 0.0120
        cdsDayCount = Actual360()
        notional = 10000.0
        recoveryRate = 0.4

        for n in range(6,11):

            
            maturity = calendar.advance(issueDate, n, Years)
            schedule = Schedule(issueDate, maturity, Period(frequency), calendar,
                                convention, convention,
                                DateGeneration.Forward, False)

            cds = CreditDefaultSwap(Protection.Seller, notional, fixedRate,
                                    schedule, convention, cdsDayCount,
                                    True, True)
            cds.setPricingEngine(MidPointCdsEngine(probabilityCurve,
                                                   recoveryRate, discountCurve))

            NPV = cds.NPV()
            flatRate = cds.impliedHazardRate(NPV, discountCurve,
                                             dayCounter,
                                             recoveryRate)
            latestRate = flatRate

            if (flatRate < h1 or flatRate > h2) :
                print("implied hazard rate outside expected range")
            print("maturity: ", n, " years")
            print("expected minimum: ", h1)
            print("expected maximum: ", h2)
            print("implied rate:     ", flatRate)
            

            if (n > 6 and flatRate < latestRate) :
                print("implied hazard rate decreasing with swap maturity")
                print("maturity: ", n, " years")
                print("previous rate: ", latestRate)
                print("implied rate:  ", flatRate)
            
            probability = RelinkableDefaultProbabilityTermStructureHandle()
            probability.linkTo(FlatHazardRate(today, 
                                              QuoteHandle(SimpleQuote(flatRate)),
                                              dayCounter))

            cds2 = CreditDefaultSwap(Protection.Seller, notional, fixedRate,
                                     schedule, convention, cdsDayCount,
                                     True, True)
            cds2.setPricingEngine(MidPointCdsEngine(probability,recoveryRate,
                                                        discountCurve))

            NPV2 = cds2.NPV()
            tolerance = 1.0
            if ((NPV-NPV2) > tolerance):
                print("failed to reproduce NPV with implied rate")
                print("expected:   ", NPV)
                print("calculated: ", NPV2)
            


    def testFairSpread(self):

        print("Testing fair-spread calculation for credit-default swaps...")

        
        # Initialize curves
        calendar = TARGET()
        today = calendar.adjust(Date.todaysDate())
        Settings.instance().evaluationDate = today

        hazardRate = QuoteHandle(SimpleQuote(0.01234))
        probabilityCurve = RelinkableDefaultProbabilityTermStructureHandle()
        probabilityCurve.linkTo(FlatHazardRate(0, calendar, hazardRate, Actual360()))

        discountCurve = RelinkableYieldTermStructureHandle()
        discountCurve.linkTo(FlatForward(today,0.06,Actual360()))

        # Build the schedule
        issueDate = calendar.advance(today, -1, Years)
        maturity = calendar.advance(issueDate, 10, Years)
        convention = Following

        schedule = Schedule(issueDate,
                            maturity,
                            Period(4, Months),
                            calendar,
                            convention,
                            convention,
                            DateGeneration.TwentiethIMM,
                            False)

        # Build the CDS
        fixedRate = 0.001
        dayCount = Actual360()
        notional = 10000.0
        recoveryRate = 0.4

        engine = MidPointCdsEngine(probabilityCurve,recoveryRate,discountCurve)

        cds = CreditDefaultSwap(Protection.Seller, notional, fixedRate,
                                schedule, convention, dayCount, True, True)
        cds.setPricingEngine(engine)

        fairRate = cds.fairSpread()

        fairCds = CreditDefaultSwap(Protection.Seller, notional, fairRate,
                                    schedule, convention, dayCount, True, True)
        fairCds.setPricingEngine(engine)

        fairNPV = fairCds.NPV()
        tolerance = 1e-10

        if ((fairNPV) > tolerance):
            print("Failed to reproduce null NPV with calculated fair spread")
            print("calculated spread: ", fairRate)
            print("calculated NPV:    ", fairNPV)

    def testFairUpfront(self):

        print("Testing fair-upfront calculation for credit-default swaps...")

        
        # Initialize curves
        calendar = TARGET()
        today = calendar.adjust(Date.todaysDate())
        Settings.instance().evaluationDate = today

        hazardRate = QuoteHandle(SimpleQuote(0.01234))
        probabilityCurve = RelinkableDefaultProbabilityTermStructureHandle()
        probabilityCurve.linkTo(FlatHazardRate(0, calendar, hazardRate, Actual360()))

        discountCurve = RelinkableYieldTermStructureHandle()
        discountCurve.linkTo(FlatForward(today,0.06,Actual360()))

        # Build the schedule
        issueDate = today
        maturity = calendar.advance(issueDate, 10, Years)
        convention = Following

        schedule = Schedule(issueDate,
                            maturity,
                            Period(4, Months),
                            calendar,
                            convention,
                            convention,
                            DateGeneration.TwentiethIMM,
                            False)
        # Build the CDS
        fixedRate = 0.05
        upfront = 0.001
        dayCount = Actual360()
        notional = 10000.0
        recoveryRate = 0.4

        engine = MidPointCdsEngine(probabilityCurve, recoveryRate, discountCurve)

        cds = CreditDefaultSwap(Protection.Seller, notional, upfront, fixedRate,
                                schedule, convention, dayCount, True, True)
        cds.setPricingEngine(engine)

        fairUpfront = cds.fairUpfront()

        fairCds = CreditDefaultSwap(Protection.Seller, notional,
                                    fairUpfront, fixedRate,
                                    schedule, convention, dayCount, True, True)
        fairCds.setPricingEngine(engine)

        fairNPV = fairCds.NPV()
        tolerance = 1e-10

        if ((fairNPV) > tolerance):
            print("Failed to reproduce null NPV with calculated fair upfront")
            print("calculated upfront: ", fairUpfront)
            print("calculated NPV:     ", fairNPV)

        # same with null upfront to begin with
        upfront = 0.0
        cds2 = CreditDefaultSwap(Protection.Seller, notional, upfront, fixedRate,
                                 schedule, convention, dayCount, True, True)
        cds2.setPricingEngine(engine)

        fairUpfront = cds2.fairUpfront()

        fairCds2 = CreditDefaultSwap(Protection.Seller, notional,
                                     fairUpfront, fixedRate,
                                     schedule, convention, dayCount, True, True)
        fairCds2.setPricingEngine(engine)

        fairNPV = fairCds2.NPV()

        if ((fairNPV) > tolerance):
            print("Failed to reproduce null NPV with calculated fair upfront")
            print("calculated upfront: ", fairUpfront)
            print("calculated NPV:     ", fairNPV)

    def testIsdaEngine(self):

        print("Testing ISDA engine calculations for credit-default swaps...")

        
        tradeDate = Date(21, May, 2009)
        Settings.instance().evaluationDate = tradeDate


        #build an ISDA compliant yield curve
        #data comes from Markit published rates
        isdaRateHelpers = RateHelperVector()
        dep_tenors = [1, 2, 3, 6, 9, 12]
        dep_quotes = [0.003081,
                      0.005525,
                      0.007163,
                      0.012413,
                      0.014,
                      0.015488]

        for t,q in zip(dep_tenors, dep_quotes):
            isdaRateHelpers.push_back(DepositRateHelper(q, Period(t, Months), 2,
                                      WeekendsOnly(), ModifiedFollowing,
                                      False, Actual360()))
        
        swap_tenors = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 25, 30]
        swap_quotes = [ 0.011907,
                        0.01699,
                        0.021198,
                        0.02444,
                        0.026937,
                        0.028967,
                        0.030504,
                        0.031719,
                        0.03279,
                        0.034535,
                        0.036217,
                        0.036981,
                        0.037246,
                        0.037605]

        isda_ibor = IborIndex("IsdaIbor", Period(3, Months), 2, USDCurrency(), WeekendsOnly(),
                              ModifiedFollowing, False, Actual360())
        for t,q in zip(swap_tenors, swap_quotes):
            isdaRateHelpers.push_back(SwapRateHelper(q, Period(t, Years),
                                                     WeekendsOnly(),
                                                     Semiannual,
                                                     ModifiedFollowing, Thirty360(), isda_ibor))
        

        discountCurve = RelinkableYieldTermStructureHandle()
        discountCurve.linkTo(PiecewiseLogCubicDiscount(0, 
                                                        WeekendsOnly(), 
                                                        isdaRateHelpers, 
                                                        Actual365Fixed()))


        probabilityCurve = RelinkableDefaultProbabilityTermStructureHandle()
        termDates = [Date(20, June, 2010),
                     Date(20, June, 2011),
                     Date(20, June, 2012),
                     Date(20, June, 2016),
                     Date(20, June, 2019)]
        spreads = [0.001, 0.1]
        recoveries = [0.2, 0.4]

        markitValues = [97798.29358, #0.001
                        97776.11889, #0.001
                        -914971.5977, #0.1
                        -894985.6298, #0.1
                        186921.3594, #0.001
                        186839.8148, #0.001
                        -1646623.672, #0.1
                        -1579803.626, #0.1
                        274298.9203,
                        274122.4725,
                        -2279730.93,
                        -2147972.527,
                        592420.2297,
                        591571.2294,
                        -3993550.206,
                        -3545843.418,
                        797501.1422,
                        795915.9787,
                        -4702034.688,
                        -4042340.999]
       
        # The risk-free curve is a bit off. We might skip the tests
        # altogether and rely on running them with indexed coupons
        # disabled, but leaving them can be useful anyway. 
        tolerance = 1.0e-3
        

        l = 0

        for d in termDates:
            for s in spreads:
                for r in recoveries:

                    schedule = Schedule(tradeDate+Period(1,Days), d, Period(3, Months), 
                            WeekendsOnly(), Following, Unadjusted, DateGeneration.CDS, 
                            False, Date(), Date())

                    quotedTrade = CreditDefaultSwap(Protection.Buyer, 10000000., 0.0, s,
                            schedule, Following, Actual360(), True, True)

                    h = quotedTrade.impliedHazardRate(0.,
                                                      discountCurve,
                                                      Actual365Fixed(),
                                                      r,
                                                      1e-10,
                                                      CreditDefaultSwap. .ISDA)

                    probabilityCurve.linkTo(FlatHazardRate(0, WeekendsOnly(), h, Actual365Fixed()))

                    engine = IsdaCdsEngine(probabilityCurve, r, discountCurve,
                                        None, IsdaCdsEngine.Taylor, IsdaCdsEngine.HalfDayBias,
                                        IsdaCdsEngine.Piecewise)

                    conventionalTrade = MakeCreditDefaultSwap(d, 0.01).withNominal(10000000.).withPricingEngine(engine)

                    BOOST_CHECK_CLOSE(conventionalTrade.notional() * conventionalTrade.fairUpfront(),
                                    markitValues[l],
                                    tolerance)

                    l+=1                



cdsTest = CreditDefaultSwapTest()
cdsTest.testCachedValue()
cdsTest.testCachedMarketValue()
cdsTest.testImpliedHazardRate()
cdsTest.testFairSpread()
cdsTest.testFairUpfront()
cdsTest.testIsdaEngine()
